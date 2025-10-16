"""
Configuration utility functions
"""

import yaml
import os
from typing import Dict, Any, Optional, List


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    default_config = {
        'language': 'python',
        'LongMethod': {
            'enabled': True,
            'max_lines': 30,
            'max_complexity': 10
        },
        'GodClass': {
            'enabled': True,
            'max_fields': 15,
            'max_methods': 20,
            'max_lines': 200
        },
        'DuplicatedCode': {
            'enabled': True,
            'min_similarity': 0.8,
            'min_chunk_size': 3
        },
        'LargeParameterList': {
            'enabled': True,
            'max_parameters': 5
        },
        'MagicNumbers': {
            'enabled': True,
            'min_occurrences': 3,
            'whitelist': [0, 1, -1],
            'min_value': 2,
            'max_value': 1000
        },
        'FeatureEnvy': {
            'enabled': True,
            'min_foreign_accesses': 3,
            'foreign_access_ratio': 1.5
        },
        'report': {
            'format': 'json',
            'include_metrics': True,
            'show_active_smells': True
        }
    }
    
    if not os.path.exists(config_path):
        return default_config
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            return merge_configs(default_config, config)
    except (yaml.YAMLError, IOError) as e:
        print(f"Error loading config file {config_path}: {e}")
        return default_config


def merge_configs(default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """Merge user config with default config"""
    merged = default.copy()
    
    for key, value in user.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = merge_configs(merged[key], value)
        else:
            merged[key] = value
    
    return merged


def get_active_detectors(config: Dict[str, Any]) -> List[str]:
    """Get list of active detectors from config"""
    active_detectors = []
    
    for detector_name in ['LongMethod', 'GodClass', 'DuplicatedCode', 
                         'LargeParameterList', 'MagicNumbers', 'FeatureEnvy']:
        if config.get(detector_name, {}).get('enabled', True):
            active_detectors.append(detector_name)
    
    return active_detectors
