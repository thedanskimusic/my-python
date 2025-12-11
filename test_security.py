#!/usr/bin/env python3
"""
Test file with intentional security issues for demonstration
DO NOT USE THIS CODE IN PRODUCTION!
"""

# This is a test file to demonstrate the security scanner

# SECRET DETECTION EXAMPLES (These should be flagged)
api_key = "sk_live_1234567890abcdefghijklmnopqrstuvwxyz"
password = "super_secret_password_123"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Database connection string with credentials
db_url = "postgres://user:password123@localhost:5432/mydb"

# VULNERABILITY EXAMPLES (These should be flagged)

# SQL Injection risk
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id  # Dangerous!
    # execute(query)

# Eval usage (dangerous)
def calculate(expression):
    result = eval(expression)  # Can execute arbitrary code!
    return result

# Exec usage (dangerous)
def run_code(code_string):
    exec(code_string)  # Can execute arbitrary code!

# Shell command injection risk
import os
def run_command(user_input):
    os.system("ls " + user_input)  # Dangerous string concatenation!

# Insecure random
import random
def generate_token():
    return random.randint(1000, 9999)  # Not cryptographically secure!

# Hardcoded IP
server_ip = "192.168.1.100"

