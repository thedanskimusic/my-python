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
from src.scanner.dependency_scanner import DependencyScanner
from src.scanner.llm_scanner import LLMScanner
from src.scanner.reporter import Reporter


@click.command()
@click.argument('target', type=click.Path(exists=True))
@click.option('--secrets/--no-secrets', default=True, help='Scan for secrets')
@click.option('--vulns/--no-vulns', default=True, help='Scan for vulnerabilities')
@click.option('--dependencies/--no-dependencies', default=False, help='Scan dependencies for known vulnerabilities')
@click.option('--llm/--no-llm', default=False, help='Use LLM (Gemini) to analyze code for security issues (requires GEMINI_API_KEY)')
@click.option('--api-key', default=None, help='Gemini API key (overrides GEMINI_API_KEY env var)')
@click.option('--output', '-o', type=click.Choice(['console', 'json']), default='console', help='Output format')
@click.option('--recursive/--no-recursive', default=True, help='Scan subdirectories')
@click.option('--severity', type=click.Choice(['critical', 'high', 'medium', 'low', 'all']), 
              default='all', help='Minimum severity to report')
def scan(target, secrets, vulns, dependencies, llm, api_key, output, recursive, severity):
    """
    Scan a file or directory for security issues.
    
    TARGET: File or directory to scan
    """
    click.echo(f"🔍 Scanning: {target}")
    click.echo(f"   Secrets: {'✓' if secrets else '✗'}, Vulnerabilities: {'✓' if vulns else '✗'}, Dependencies: {'✓' if dependencies else '✗'}, LLM: {'✓' if llm else '✗'}")
    click.echo()
    
    all_findings = []
    
    # Scan for secrets
    if secrets:
        click.echo("Scanning for secrets...", nl=False)
        secret_detector = SecretDetector()
        secret_findings = secret_detector.scan_directory(target, recursive)
        all_findings.extend(secret_findings)
        # Count files that were actually scanned (not just files with findings)
        file_scanner = secret_detector.file_scanner
        files_scanned = len(file_scanner.get_scannable_files(target, recursive))
        click.echo(f" Scanned {files_scanned} file(s), found {len(secret_findings)} potential secrets")
    
    # Scan for vulnerabilities
    if vulns:
        click.echo("Scanning for vulnerabilities...", nl=False)
        vuln_scanner = VulnerabilityScanner()
        vuln_findings = vuln_scanner.scan_directory(target, recursive)
        all_findings.extend(vuln_findings)
        # Count files that were actually scanned (not just files with findings)
        file_scanner = vuln_scanner.file_scanner
        files_scanned = len(file_scanner.get_code_files(target, recursive))
        click.echo(f" Scanned {files_scanned} file(s), found {len(vuln_findings)} potential vulnerabilities")
    
    # Scan dependencies for known vulnerabilities
    if dependencies:
        click.echo("Scanning dependencies for known vulnerabilities...")
        dep_scanner = DependencyScanner()
        # Only scan directories (not individual files)
        if os.path.isdir(target):
            dep_findings, dep_stats = dep_scanner.scan_directory(target)
            all_findings.extend(dep_findings)
            if dep_stats['files_found'] > 0:
                click.echo(f"✓ Scanned {dep_stats['packages_checked']} packages from {dep_stats['files_found']} file(s), found {len(dep_findings)} vulnerable dependencies")
            else:
                click.echo(f"  No dependency files found")
        else:
            click.echo("  (skipped - dependency scanning requires a directory)")
    
    # LLM-based security analysis
    if llm:
        click.echo("Analyzing code with LLM (Gemini)...", nl=False)
        try:
            llm_scanner = LLMScanner(api_key=api_key)
            
            # Check if API key is available
            if not llm_scanner.api_key:
                click.echo(" ✗ (skipped - GEMINI_API_KEY not set. Set environment variable or use --api-key)")
            else:
                llm_findings = llm_scanner.scan_directory(target, recursive)
                all_findings.extend(llm_findings)
                click.echo(f" Found {len(llm_findings)} potential security issues")
        except Exception as e:
            click.echo(f" ✗ (error: {str(e)})")
    
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

