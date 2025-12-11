"""
File scanning utilities
Handles directory traversal and file filtering
"""

import os
from pathlib import Path
from typing import List, Set
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from src.patterns.rules import CODE_FILE_EXTENSIONS, CONFIG_FILE_EXTENSIONS, IGNORE_PATTERNS


class FileScanner:
    """Handles file system traversal and filtering"""
    
    def __init__(self):
        self.code_extensions = CODE_FILE_EXTENSIONS
        self.config_extensions = CONFIG_FILE_EXTENSIONS
        self.ignore_patterns = IGNORE_PATTERNS
    
    def should_ignore(self, path: str) -> bool:
        """Check if a path should be ignored"""
        path_parts = Path(path).parts
        for part in path_parts:
            if part in self.ignore_patterns:
                return True
        return False
    
    def is_code_file(self, file_path: str) -> bool:
        """Check if file is a code file"""
        ext = Path(file_path).suffix.lower()
        return ext in self.code_extensions
    
    def is_config_file(self, file_path: str) -> bool:
        """Check if file is a config file"""
        ext = Path(file_path).suffix.lower()
        return ext in self.config_extensions
    
    def get_scannable_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        Get all files that should be scanned (code + config files)
        
        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of file paths
        """
        files = []
        
        if not os.path.isdir(directory):
            if os.path.isfile(directory):
                return [directory]
            return []
        
        if recursive:
            for root, dirs, filenames in os.walk(directory):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
                
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if self.should_ignore(file_path):
                        continue
                    
                    ext = Path(file_path).suffix.lower()
                    if ext in self.code_extensions or ext in self.config_extensions:
                        files.append(file_path)
        else:
            for item in os.listdir(directory):
                file_path = os.path.join(directory, item)
                if os.path.isfile(file_path) and not self.should_ignore(file_path):
                    ext = Path(file_path).suffix.lower()
                    if ext in self.code_extensions or ext in self.config_extensions:
                        files.append(file_path)
        
        return files
    
    def get_code_files(self, directory: str, recursive: bool = True) -> List[str]:
        """
        Get only code files (not config files)
        
        Args:
            directory: Directory to scan
            recursive: Whether to scan subdirectories
            
        Returns:
            List of code file paths
        """
        files = []
        
        if not os.path.isdir(directory):
            if os.path.isfile(directory) and self.is_code_file(directory):
                return [directory]
            return []
        
        if recursive:
            for root, dirs, filenames in os.walk(directory):
                # Filter out ignored directories
                dirs[:] = [d for d in dirs if not self.should_ignore(os.path.join(root, d))]
                
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if self.should_ignore(file_path):
                        continue
                    
                    if self.is_code_file(file_path):
                        files.append(file_path)
        else:
            for item in os.listdir(directory):
                file_path = os.path.join(directory, item)
                if os.path.isfile(file_path) and not self.should_ignore(file_path):
                    if self.is_code_file(file_path):
                        files.append(file_path)
        
        return files

