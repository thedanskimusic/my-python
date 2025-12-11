"""
Secret detection module
Scans code for exposed secrets, API keys, passwords, etc.
"""

from typing import List, Dict, Tuple
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.scanner.file_scanner import FileScanner
from src.patterns.rules import SECRET_PATTERNS


class SecretDetector:
    """Detects secrets and credentials in code files"""
    
    def __init__(self):
        self.file_scanner = FileScanner()
        self.patterns = SECRET_PATTERNS
    
    def scan_file(self, file_path: str) -> List[Dict]:
        """
        Scan a single file for secrets
        
        Args:
            file_path: Path to the file to scan
            
        Returns:
            List of findings with line numbers and context
        """
        findings = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line_num, line in enumerate(lines, start=1):
                for pattern_info in self.patterns:
                    pattern = pattern_info['pattern']
                    matches = pattern.finditer(line)
                    
                    for match in matches:
                        # Get context (surrounding lines)
                        context_start = max(0, line_num - 2)
                        context_end = min(len(lines), line_num + 1)
                        context = ''.join(lines[context_start:context_end])
                        
                        finding = {
                            'type': 'secret',
                            'name': pattern_info['name'],
                            'severity': pattern_info['severity'],
                            'description': pattern_info['description'],
                            'file': file_path,
                            'line': line_num,
                            'match': match.group(0)[:50] + '...' if len(match.group(0)) > 50 else match.group(0),
                            'context': context.strip()
                        }
                        findings.append(finding)
                        
        except Exception as e:
            # Skip files that can't be read (binary, permissions, etc.)
            pass
            
        return findings
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[Dict]:
        """
        Scan a directory for secrets
        
        Args:
            directory: Directory path to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of all findings
        """
        all_findings = []
        files = self.file_scanner.get_scannable_files(directory, recursive)
        
        for file_path in files:
            findings = self.scan_file(file_path)
            all_findings.extend(findings)
            
        return all_findings

