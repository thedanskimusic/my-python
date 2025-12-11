"""
Reporting module
Formats and outputs scan results
"""

from typing import List, Dict
from collections import defaultdict
import json


class Reporter:
    """Handles formatting and output of scan results"""
    
    def __init__(self):
        self.severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    
    def format_console(self, findings: List[Dict]) -> str:
        """
        Format findings for console output
        
        Args:
            findings: List of finding dictionaries
            
        Returns:
            Formatted string
        """
        if not findings:
            return "✅ No security issues found!\n"
        
        output = []
        output.append(f"\n🔍 Security Scan Results\n")
        output.append("=" * 70 + "\n")
        
        # Group by severity
        by_severity = defaultdict(list)
        for finding in findings:
            by_severity[finding['severity']].append(finding)
        
        # Sort by severity
        sorted_severities = sorted(by_severity.keys(), key=lambda x: self.severity_order.get(x, 99))
        
        for severity in sorted_severities:
            severity_findings = by_severity[severity]
            severity_emoji = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'low': '🔵'
            }.get(severity, '⚪')
            
            output.append(f"\n{severity_emoji} {severity.upper()} ({len(severity_findings)} findings)\n")
            output.append("-" * 70 + "\n")
            
            for finding in severity_findings:
                output.append(f"  [{finding['type']}] {finding['name']}\n")
                output.append(f"  File: {finding['file']}:{finding['line']}\n")
                output.append(f"  Description: {finding['description']}\n")
                output.append(f"  Match: {finding['match']}\n")
                output.append(f"  Context:\n")
                # Indent context lines
                for line in finding['context'].split('\n'):
                    output.append(f"    {line}\n")
                output.append("\n")
        
        # Summary
        output.append("=" * 70 + "\n")
        output.append("Summary:\n")
        for severity in sorted_severities:
            count = len(by_severity[severity])
            output.append(f"  {severity.upper()}: {count}\n")
        output.append(f"  Total: {len(findings)}\n")
        
        return ''.join(output)
    
    def format_json(self, findings: List[Dict]) -> str:
        """
        Format findings as JSON
        
        Args:
            findings: List of finding dictionaries
            
        Returns:
            JSON string
        """
        return json.dumps({
            'total': len(findings),
            'findings': findings
        }, indent=2)
    
    def format_summary(self, findings: List[Dict]) -> str:
        """
        Get a brief summary of findings
        
        Args:
            findings: List of finding dictionaries
            
        Returns:
            Summary string
        """
        if not findings:
            return "✅ No issues found"
        
        by_severity = defaultdict(int)
        by_type = defaultdict(int)
        
        for finding in findings:
            by_severity[finding['severity']] += 1
            by_type[finding['type']] += 1
        
        summary = []
        summary.append(f"Total findings: {len(findings)}\n")
        summary.append("By severity:\n")
        for severity in ['critical', 'high', 'medium', 'low']:
            if severity in by_severity:
                summary.append(f"  {severity}: {by_severity[severity]}\n")
        summary.append("By type:\n")
        for type_name, count in by_type.items():
            summary.append(f"  {type_name}: {count}\n")
        
        return ''.join(summary)

