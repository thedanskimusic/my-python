#!/usr/bin/env python3
"""
Security Scanner CLI
Command-line interface for the security scanner
"""

import click
import sys
from pathlib import Path
import os

# Add project root to path
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from src.scanner.secret_detector import SecretDetector
from src.scanner.vulnerability_scanner import VulnerabilityScanner
from src.scanner.reporter import Reporter


@click.command()
@click.argument('target', type=click.Path(exists=True))
@click.option('--secrets/--no-secrets', default=True, help='Scan for secrets')
@click.option('--vulns/--no-vulns', default=True, help='Scan for vulnerabilities')
@click.option('--output', '-o', type=click.Choice(['console', 'json']), default='console', help='Output format')
@click.option('--recursive/--no-recursive', default=True, help='Scan subdirectories')
@click.option('--severity', type=click.Choice(['critical', 'high', 'medium', 'low', 'all']), 
              default='all', help='Minimum severity to report')
def scan(target, secrets, vulns, output, recursive, severity):
    """
    Scan a file or directory for security issues.
    
    TARGET: File or directory to scan
    """
    click.echo(f"🔍 Scanning: {target}")
    click.echo(f"   Secrets: {'✓' if secrets else '✗'}, Vulnerabilities: {'✓' if vulns else '✗'}")
    click.echo()
    
    all_findings = []
    
    # Scan for secrets
    if secrets:
        click.echo("Scanning for secrets...", nl=False)
        secret_detector = SecretDetector()
        secret_findings = secret_detector.scan_directory(target, recursive)
        all_findings.extend(secret_findings)
        click.echo(f" Found {len(secret_findings)} potential secrets")
    
    # Scan for vulnerabilities
    if vulns:
        click.echo("Scanning for vulnerabilities...", nl=False)
        vuln_scanner = VulnerabilityScanner()
        vuln_findings = vuln_scanner.scan_directory(target, recursive)
        all_findings.extend(vuln_findings)
        click.echo(f" Found {len(vuln_findings)} potential vulnerabilities")
    
    # Filter by severity
    if severity != 'all':
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        min_severity = severity_order.get(severity, 99)
        all_findings = [
            f for f in all_findings 
            if severity_order.get(f['severity'], 99) <= min_severity
        ]
    
    # Report results
    reporter = Reporter()
    
    if output == 'json':
        click.echo(reporter.format_json(all_findings))
    else:
        click.echo(reporter.format_console(all_findings))
    
    # Exit with error code if critical or high severity issues found
    critical_high = [f for f in all_findings if f['severity'] in ['critical', 'high']]
    if critical_high:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    scan()

