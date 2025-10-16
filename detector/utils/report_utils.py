"""
Report utility functions
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


def generate_report(smells: List[Dict[str, Any]], 
                   active_detectors: List[str], 
                   file_paths: List[str],
                   config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a comprehensive report"""
    
    # Group smells by type
    smells_by_type = {}
    for smell in smells:
        smell_type = smell['smell_type']
        if smell_type not in smells_by_type:
            smells_by_type[smell_type] = []
        smells_by_type[smell_type].append(smell)
    
    # Calculate statistics
    total_smells = len(smells)
    smells_by_file = {}
    for smell in smells:
        file_path = smell['file_path']
        if file_path not in smells_by_file:
            smells_by_file[file_path] = 0
        smells_by_file[file_path] += 1
    
    # Generate report
    report = {
        'metadata': {
            'generated_at': datetime.now().isoformat(),
            'total_files_analyzed': len(file_paths),
            'total_smells_found': total_smells,
            'active_detectors': active_detectors,
            'config_used': config
        },
        'summary': {
            'smells_by_type': {smell_type: len(smells_list) 
                             for smell_type, smells_list in smells_by_type.items()},
            'smells_by_file': smells_by_file,
            'severity_breakdown': _calculate_severity_breakdown(smells)
        },
        'smells': smells,
        'smells_by_type': smells_by_type
    }
    
    return report


def _calculate_severity_breakdown(smells: List[Dict[str, Any]]) -> Dict[str, int]:
    """Calculate severity breakdown"""
    severity_counts = {'high': 0, 'medium': 0, 'low': 0}
    
    for smell in smells:
        severity = smell.get('severity', 'medium')
        if severity in severity_counts:
            severity_counts[severity] += 1
    
    return severity_counts


def save_report(report: Dict[str, Any], output_path: str, format_type: str = 'json') -> bool:
    """Save report to file"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if format_type.lower() == 'json':
            with open(output_path, 'w', encoding='utf-8') as file:
                json.dump(report, file, indent=2, ensure_ascii=False)
        elif format_type.lower() == 'txt':
            with open(output_path, 'w', encoding='utf-8') as file:
                _write_text_report(report, file)
        else:
            print(f"Unsupported format: {format_type}")
            return False
        
        return True
    except (IOError, OSError) as e:
        print(f"Error saving report to {output_path}: {e}")
        return False


def _write_text_report(report: Dict[str, Any], file) -> None:
    """Write text format report"""
    metadata = report['metadata']
    summary = report['summary']
    
    file.write("CODE SMELL DETECTION REPORT\n")
    file.write("=" * 50 + "\n\n")
    
    file.write(f"Generated at: {metadata['generated_at']}\n")
    file.write(f"Files analyzed: {metadata['total_files_analyzed']}\n")
    file.write(f"Total smells found: {metadata['total_smells_found']}\n")
    file.write(f"Active detectors: {', '.join(metadata['active_detectors'])}\n\n")
    
    file.write("SUMMARY\n")
    file.write("-" * 20 + "\n")
    file.write("Smells by type:\n")
    for smell_type, count in summary['smells_by_type'].items():
        file.write(f"  {smell_type}: {count}\n")
    
    file.write("\nSeverity breakdown:\n")
    for severity, count in summary['severity_breakdown'].items():
        file.write(f"  {severity}: {count}\n")
    
    file.write("\nDETAILED FINDINGS\n")
    file.write("-" * 20 + "\n")
    
    for smell in report['smells']:
        file.write(f"\n{smell['smell_type']} - {smell['severity'].upper()}\n")
        file.write(f"File: {smell['file_path']}\n")
        file.write(f"Line: {smell['line_number']}\n")
        file.write(f"Message: {smell['message']}\n")
        if smell.get('details'):
            file.write("Details:\n")
            for key, value in smell['details'].items():
                file.write(f"  {key}: {value}\n")


def print_summary(report: Dict[str, Any]) -> None:
    """Print a summary of the report to console"""
    metadata = report['metadata']
    summary = report['summary']
    
    print("\n" + "=" * 60)
    print("CODE SMELL DETECTION SUMMARY")
    print("=" * 60)
    print(f"Files analyzed: {metadata['total_files_analyzed']}")
    print(f"Total smells found: {metadata['total_smells_found']}")
    print(f"Active detectors: {', '.join(metadata['active_detectors'])}")
    
    print("\nSmells by type:")
    for smell_type, count in summary['smells_by_type'].items():
        print(f"  {smell_type}: {count}")
    
    print("\nSeverity breakdown:")
    for severity, count in summary['severity_breakdown'].items():
        print(f"  {severity}: {count}")
    
    print("=" * 60)
