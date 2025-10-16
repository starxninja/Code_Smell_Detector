#!/usr/bin/env python3
"""
Code Smell Detection Application
Main entry point for the code smell detector
"""

import argparse
import sys
import os
from typing import List, Dict, Any

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from detectors import (
    LongMethodDetector, GodClassDetector, DuplicatedCodeDetector,
    LargeParameterListDetector, MagicNumbersDetector, FeatureEnvyDetector
)
from utils import (
    read_file, is_python_file, find_python_files,
    load_config, get_active_detectors, generate_report, save_report, print_summary
)


class CodeSmellDetector:
    """Main code smell detection application"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = load_config(config_path)
        self.detectors = self._initialize_detectors()
    
    def _initialize_detectors(self) -> List[Any]:
        """Initialize all available detectors"""
        return [
            LongMethodDetector(self.config),
            GodClassDetector(self.config),
            DuplicatedCodeDetector(self.config),
            LargeParameterListDetector(self.config),
            MagicNumbersDetector(self.config),
            FeatureEnvyDetector(self.config)
        ]
    
    def detect_smells(self, file_paths: List[str], 
                     only_detectors: List[str] = None,
                     exclude_detectors: List[str] = None) -> List[Dict[str, Any]]:
        """Detect code smells in the given files"""
        all_smells = []
        processed_files = []
        
        # Filter detectors based on CLI arguments
        active_detectors = self._filter_detectors(only_detectors, exclude_detectors)
        
        print(f"Analyzing files with detectors: {', '.join(active_detectors)}")
        
        for file_path in file_paths:
            if not is_python_file(file_path):
                print(f"Skipping non-Python file: {file_path}")
                continue
            
            print(f"Analyzing: {file_path}")
            source_code = read_file(file_path)
            if not source_code:
                continue
            
            processed_files.append(file_path)
            file_smells = []
            
            # Run each active detector
            for detector in self.detectors:
                if detector.smell_name in active_detectors:
                    smells = detector.detect(file_path, source_code)
                    file_smells.extend(smells)
            
            all_smells.extend(file_smells)
            print(f"  Found {len(file_smells)} smells")
        
        return all_smells, processed_files, active_detectors
    
    def _filter_detectors(self, only_detectors: List[str] = None,
                         exclude_detectors: List[str] = None) -> List[str]:
        """Filter detectors based on CLI arguments"""
        # Start with all enabled detectors from config
        active_detectors = get_active_detectors(self.config)
        
        # Apply --only filter
        if only_detectors:
            active_detectors = [d for d in active_detectors if d in only_detectors]
        
        # Apply --exclude filter
        if exclude_detectors:
            active_detectors = [d for d in active_detectors if d not in exclude_detectors]
        
        return active_detectors
    
    def generate_and_save_report(self, smells: List[Dict[str, Any]], 
                                file_paths: List[str], 
                                active_detectors: List[str],
                                output_path: str = None,
                                format_type: str = None) -> bool:
        """Generate and save the detection report"""
        # Generate report
        report = generate_report(smells, active_detectors, file_paths, self.config)
        
        # Print summary to console
        print_summary(report)
        
        # Save report to file
        if output_path:
            format_type = format_type or self.config.get('report', {}).get('format', 'json')
            return save_report(report, output_path, format_type)
        
        return True


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Code Smell Detection Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py file.py                    # Analyze single file
  python main.py src/                       # Analyze directory
  python main.py file.py --only LongMethod  # Only detect long methods
  python main.py file.py --exclude MagicNumbers  # All except magic numbers
  python main.py file.py --output report.json  # Save report to file
        """
    )
    
    parser.add_argument('target', 
                       help='File or directory to analyze')
    parser.add_argument('--config', '-c',
                       default='config.yaml',
                       help='Configuration file path (default: config.yaml)')
    parser.add_argument('--output', '-o',
                       help='Output file path for report')
    parser.add_argument('--format', '-f',
                       choices=['json', 'txt'],
                       help='Output format (json or txt)')
    parser.add_argument('--only',
                       help='Only run specific detectors (comma-separated)')
    parser.add_argument('--exclude',
                       help='Exclude specific detectors (comma-separated)')
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Parse detector filters
    only_detectors = None
    if args.only:
        only_detectors = [d.strip() for d in args.only.split(',')]
    
    exclude_detectors = None
    if args.exclude:
        exclude_detectors = [d.strip() for d in args.exclude.split(',')]
    
    # Initialize detector
    try:
        detector = CodeSmellDetector(args.config)
    except Exception as e:
        print(f"Error initializing detector: {e}")
        return 1
    
    # Determine files to analyze
    if os.path.isfile(args.target):
        file_paths = [args.target]
    elif os.path.isdir(args.target):
        file_paths = find_python_files(args.target)
        if not file_paths:
            print(f"No Python files found in directory: {args.target}")
            return 1
    else:
        print(f"Target not found: {args.target}")
        return 1
    
    print(f"Found {len(file_paths)} Python file(s) to analyze")
    
    # Detect smells
    try:
        smells, processed_files, active_detectors = detector.detect_smells(
            file_paths, only_detectors, exclude_detectors
        )
        
        # Generate and save report
        output_path = args.output or 'output/report.json'
        success = detector.generate_and_save_report(
            smells, processed_files, active_detectors, 
            output_path, args.format
        )
        
        if success:
            print(f"\nReport saved to: {output_path}")
            return 0
        else:
            print("Error saving report")
            return 1
            
    except Exception as e:
        print(f"Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
