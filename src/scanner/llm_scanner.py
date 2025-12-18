"""
LLM-based security scanning module
Uses Google Gemini 2.5 Flash to analyze codebases for security issues
"""

import os
import json
import sys
from typing import List, Dict, Optional
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from src.scanner.file_scanner import FileScanner


class LLMScanner:
    """Uses Gemini LLM to analyze code for security vulnerabilities"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM scanner
        
        Args:
            api_key: Gemini API key (if None, tries: CLI arg -> env var -> config file)
        """
        self.file_scanner = FileScanner()
        self.api_key = api_key or self._get_api_key_from_config()
        # Using Gemini 2.5 Flash for security analysis
        self.model_name = 'gemini-2.5-flash'
        
        if GEMINI_AVAILABLE and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            self.model = None
    
    def _get_api_key_from_config(self) -> Optional[str]:
        """
        Try to get API key from various sources in order of preference:
        1. Environment variable GEMINI_API_KEY
        2. Config file ~/.security-scanner/config.json
        3. Config file .security-scanner.json in current directory
        
        Returns:
            API key string or None if not found
        """
        # Try environment variable first
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            return api_key
        
        # Try config file in home directory
        home_config = os.path.join(os.path.expanduser('~'), '.security-scanner', 'config.json')
        if os.path.exists(home_config):
            try:
                with open(home_config, 'r') as f:
                    config = json.load(f)
                    if 'gemini_api_key' in config:
                        return config['gemini_api_key']
            except (json.JSONDecodeError, IOError):
                pass
        
        # Try config file in current directory
        local_config = '.security-scanner.json'
        if os.path.exists(local_config):
            try:
                with open(local_config, 'r') as f:
                    config = json.load(f)
                    if 'gemini_api_key' in config:
                        return config['gemini_api_key']
            except (json.JSONDecodeError, IOError):
                pass
        
        return None
    
    def _collect_repository_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        Collect all code files from the repository
        
        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of file paths
        """
        if not os.path.isdir(directory):
            if os.path.isfile(directory) and self.file_scanner.is_code_file(directory):
                return [directory]
            return []
        
        return self.file_scanner.get_code_files(directory, recursive)
    
    def _prepare_context(self, files: List[str], max_files: int = 50) -> str:
        """
        Prepare code context for LLM analysis
        
        Args:
            files: List of file paths to include
            max_files: Maximum number of files to include (to avoid token limits)
            
        Returns:
            Formatted string with code context
        """
        context_parts = []
        
        # Limit number of files to avoid token limits
        files_to_analyze = files[:max_files]
        
        if len(files) > max_files:
            context_parts.append(f"Note: Analyzing {max_files} of {len(files)} files due to size limits.\n\n")
        
        for file_path in files_to_analyze:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    
                # Add file header
                context_parts.append(f"\n{'='*80}\n")
                context_parts.append(f"File: {file_path}\n")
                context_parts.append(f"{'='*80}\n")
                
                # Add file content with line numbers
                for line_num, line in enumerate(lines, start=1):
                    context_parts.append(f"{line_num:4d} | {line}")
                    
            except Exception:
                # Skip files that can't be read
                continue
        
        return ''.join(context_parts)
    
    def _create_security_prompt(self, code_context: str) -> str:
        """
        Create security analysis prompt for Gemini
        
        Args:
            code_context: Formatted code context
            
        Returns:
            Complete prompt string
        """
        prompt = """You are a security expert analyzing a codebase for security vulnerabilities. Analyze the provided code and identify security issues.

Focus on these areas:
1. **API Endpoints**: Look for endpoints (REST, GraphQL, etc.) that lack authentication or authorization checks
2. **Authentication & Authorization**: Missing or weak authentication, improper authorization checks, session management issues
3. **Input Validation**: Missing input validation, improper sanitization, injection vulnerabilities (SQL, XSS, command injection)
4. **Data Exposure**: Sensitive data in logs, exposed credentials, improper error messages revealing system info
5. **General Security**: Insecure configurations, weak cryptography, missing security headers, CORS misconfigurations

For each issue found, provide:
- **name**: Brief descriptive name of the issue
- **severity**: "critical", "high", "medium", or "low"
- **description**: Detailed explanation of the security issue
- **file**: Full file path where the issue was found
- **line**: Line number where the issue occurs (or approximate if spanning multiple lines)
- **recommendation**: Specific advice on how to fix the issue

Return your findings as a JSON object with this exact structure:
{
  "findings": [
    {
      "type": "llm_analysis",
      "name": "Issue name",
      "severity": "high",
      "description": "Detailed description of the security issue",
      "file": "path/to/file.py",
      "line": 42,
      "recommendation": "How to fix this issue"
    }
  ]
}

Only report real security issues. Do not flag false positives or minor code quality issues that don't have security implications.

Code to analyze:
"""
        prompt += code_context
        prompt += "\n\nProvide your security analysis as JSON:"
        
        return prompt
    
    def _call_gemini_api(self, prompt: str) -> Optional[Dict]:
        """
        Call Gemini API with the security analysis prompt
        
        Args:
            prompt: Complete prompt string
            
        Returns:
            Parsed JSON response or None if error
        """
        if not self.model:
            return None
        
        try:
            # Estimate token usage (rough approximation: 1 token ≈ 4 characters)
            estimated_tokens = len(prompt) // 4
            if estimated_tokens > 1000000:  # Warn if very large
                print(f"Warning: Large repository detected (~{estimated_tokens:,} tokens). Analysis may be incomplete.")
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.1,  # Low temperature for more focused analysis
                    'max_output_tokens': 8192,  # Allow detailed findings
                }
            )
            
            # Extract text from response
            response_text = response.text.strip()
            
            # Try to extract JSON from response (might have markdown code blocks)
            if '```json' in response_text:
                # Extract JSON from markdown code block
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                if end > start:
                    response_text = response_text[start:end].strip()
            elif '```' in response_text:
                # Extract from generic code block
                start = response_text.find('```') + 3
                end = response_text.find('```', start)
                if end > start:
                    response_text = response_text[start:end].strip()
            
            # Parse JSON
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            print(f"Warning: Failed to parse LLM response as JSON: {e}")
            try:
                print(f"Response preview: {response_text[:200]}...")
            except NameError:
                pass  # response_text not defined yet
            return None
        except Exception as e:
            print(f"Warning: LLM API error: {e}")
            return None
    
    def _parse_findings(self, api_response: Optional[Dict]) -> List[Dict]:
        """
        Parse API response into standard finding format
        
        Args:
            api_response: Parsed JSON response from API
            
        Returns:
            List of findings in standard format
        """
        findings = []
        
        if not api_response:
            return findings
        
        # Extract findings from response
        response_findings = api_response.get('findings', [])
        
        for finding in response_findings:
            # Ensure all required fields are present
            standard_finding = {
                'type': finding.get('type', 'llm_analysis'),
                'name': finding.get('name', 'Security Issue'),
                'severity': finding.get('severity', 'medium'),
                'description': finding.get('description', 'No description provided'),
                'file': finding.get('file', 'Unknown'),
                'line': finding.get('line', 0),
                'recommendation': finding.get('recommendation', 'No recommendation provided')
            }
            
            # Validate severity
            if standard_finding['severity'] not in ['critical', 'high', 'medium', 'low']:
                standard_finding['severity'] = 'medium'
            
            findings.append(standard_finding)
        
        return findings
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        """
        Scan a directory using LLM analysis
        
        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of security findings
        """
        # Check if API key is available
        if not self.api_key:
            return []
        
        if not GEMINI_AVAILABLE:
            return []
        
        # Collect files
        files = self._collect_repository_files(directory, recursive)
        
        if not files:
            return []
        
        # Prepare context
        code_context = self._prepare_context(files)
        
        # Create prompt
        prompt = self._create_security_prompt(code_context)
        
        # Call API
        api_response = self._call_gemini_api(prompt)
        
        # Parse findings
        findings = self._parse_findings(api_response)
        
        return findings
    
    def scan_file(self, file_path: str) -> List[Dict]:
        """
        Scan a single file (for consistency with other scanners)
        Note: LLM scanner analyzes entire repo, so this just calls scan_directory
        
        Args:
            file_path: File to scan
            
        Returns:
            List of security findings
        """
        if os.path.isfile(file_path):
            directory = os.path.dirname(file_path) or '.'
            return self.scan_directory(directory, recursive=False)
        return []

