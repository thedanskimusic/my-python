"""
Dependency vulnerability scanning module
Checks packages against OSV (Open Source Vulnerabilities) database
"""

import requests
import re
import os
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class DependencyScanner:
    """Scans dependencies for known vulnerabilities using OSV API"""
    
    def __init__(self):
        self.osv_api = "https://api.osv.dev/v1/query"
        self.timeout = 10  # API request timeout
    
    def parse_requirements_txt(self, file_path: str) -> List[Dict[str, str]]:
        """
        Parse requirements.txt file
        
        Returns:
            List of dicts with 'name' and 'version' keys
        """
        packages = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Remove inline comments
                    if '#' in line:
                        line = line.split('#')[0].strip()
                    
                    # Parse different formats: package==version, package>=version, etc.
                    # Match: package==1.2.3, package>=1.2.3, package~=1.2.3, etc.
                    match = re.match(r'^([a-zA-Z0-9_-]+[a-zA-Z0-9._-]*)(==|>=|<=|>|<|~=)(.+)$', line)
                    if match:
                        name = match.group(1).lower()
                        version = match.group(3).strip()
                        packages.append({'name': name, 'version': version, 'file': file_path})
                    # Also handle just package name (no version specified)
                    elif re.match(r'^[a-zA-Z0-9_-]+[a-zA-Z0-9._-]*$', line):
                        packages.append({'name': line.lower(), 'version': None, 'file': file_path})
                        
        except Exception as e:
            # Skip files that can't be read
            pass
            
        return packages
    
    def parse_package_json(self, file_path: str) -> List[Dict[str, str]]:
        """
        Parse package.json file (Node.js)
        
        Returns:
            List of dicts with 'name' and 'version' keys
        """
        packages = []
        
        try:
            import json
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Check dependencies and devDependencies
            for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
                if dep_type in data:
                    for name, version in data[dep_type].items():
                        # Remove version prefixes like ^, ~, >=, etc.
                        clean_version = re.sub(r'^[\^~>=<]+', '', version)
                        clean_version = clean_version.strip()
                        packages.append({
                            'name': name.lower(),
                            'version': clean_version if clean_version else None,
                            'file': file_path
                        })
                        
        except Exception as e:
            # Skip files that can't be read or parsed
            pass
            
        return packages
    
    def find_dependency_files(self, directory: str) -> List[str]:
        """
        Find dependency files in a directory
        
        Returns:
            List of file paths
        """
        files = []
        dependency_files = [
            'requirements.txt',
            'package.json',
            'go.mod',
            'Cargo.toml',
            'pom.xml',
            'composer.json',
            'Gemfile'
        ]
        
        for root, dirs, filenames in os.walk(directory):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'venv', 'env', '__pycache__']]
            
            for filename in filenames:
                if filename in dependency_files:
                    files.append(os.path.join(root, filename))
                    
        return files
    
    def check_vulnerability(self, package: str, version: Optional[str], ecosystem: str = "PyPI") -> Tuple[List[Dict], bool]:
        """
        Query OSV API for vulnerabilities in a package
        
        Args:
            package: Package name
            version: Package version (optional)
            ecosystem: Package ecosystem (PyPI, npm, etc.)
            
        Returns:
            Tuple of (vulnerabilities list, success boolean)
        """
        if not version:
            # Can't check without version
            return [], False
            
        payload = {
            "version": version,
            "package": {
                "name": package,
                "ecosystem": ecosystem
            }
        }
        
        try:
            response = requests.post(self.osv_api, json=payload, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            vulns = data.get("vulns", [])
            return vulns, True
            
        except requests.exceptions.RequestException:
            # API error - return empty list
            return [], False
        except Exception:
            return [], False
    
    def scan_directory(self, directory: str) -> Tuple[List[Dict], Dict]:
        """
        Scan a directory for dependency vulnerabilities
        
        Args:
            directory: Directory to scan
            
        Returns:
            Tuple of (findings list, statistics dict)
        """
        all_findings = []
        stats = {
            'files_found': 0,
            'packages_parsed': 0,
            'packages_checked': 0,
            'vulnerabilities_found': 0
        }
        
        # Find dependency files
        dep_files = self.find_dependency_files(directory)
        stats['files_found'] = len(dep_files)
        
        if not dep_files:
            return all_findings, stats
        
        # Parse each dependency file
        all_packages = []
        for dep_file in dep_files:
            if dep_file.endswith('requirements.txt'):
                packages = self.parse_requirements_txt(dep_file)
                ecosystem = "PyPI"
            elif dep_file.endswith('package.json'):
                packages = self.parse_package_json(dep_file)
                ecosystem = "npm"
            else:
                # Skip unsupported files for now
                continue
            
            # Add ecosystem info
            for pkg in packages:
                pkg['ecosystem'] = ecosystem
            all_packages.extend(packages)
        
        stats['packages_parsed'] = len(all_packages)
        
        # Check each package for vulnerabilities
        for pkg in all_packages:
            if not pkg.get('version'):
                continue  # Skip packages without versions
            
            stats['packages_checked'] += 1
                
            vulns, success = self.check_vulnerability(
                pkg['name'],
                pkg['version'],
                pkg.get('ecosystem', 'PyPI')
            )
            
            if vulns:
                stats['vulnerabilities_found'] += len(vulns)
                for vuln in vulns:
                    finding = {
                        'type': 'dependency',
                        'name': f"Vulnerable {pkg['name']}",
                        'severity': self._determine_severity(vuln),
                        'description': vuln.get('summary', 'No description available'),
                        'package': pkg['name'],
                        'version': pkg['version'],
                        'ecosystem': pkg.get('ecosystem', 'PyPI'),
                        'file': pkg['file'],
                        'vuln_id': vuln.get('id', 'Unknown'),
                        'details': vuln.get('details', ''),
                        'references': vuln.get('references', [])
                    }
                    all_findings.append(finding)
        
        return all_findings, stats
    
    def _determine_severity(self, vuln: Dict) -> str:
        """
        Determine severity from vulnerability data
        
        Args:
            vuln: Vulnerability data from OSV
            
        Returns:
            Severity level (critical, high, medium, low)
        """
        # Check database_specific for severity info
        db_specific = vuln.get('database_specific', {})
        
        # Check for CVSS score
        if 'cvss_score' in db_specific:
            score = db_specific['cvss_score']
            if score >= 9.0:
                return 'critical'
            elif score >= 7.0:
                return 'high'
            elif score >= 4.0:
                return 'medium'
            else:
                return 'low'
        
        # Check for severity field
        if 'severity' in db_specific:
            sev = db_specific['severity'].lower()
            if 'critical' in sev:
                return 'critical'
            elif 'high' in sev:
                return 'high'
            elif 'medium' in sev:
                return 'medium'
            else:
                return 'low'
        
        # Default to high if no severity info
        return 'high'

