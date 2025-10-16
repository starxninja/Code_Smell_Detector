"""
Code Smell Detectors Package
"""

from .base_detector import BaseDetector
from .long_method_detector import LongMethodDetector
from .god_class_detector import GodClassDetector
from .duplicated_code_detector import DuplicatedCodeDetector
from .large_parameter_list_detector import LargeParameterListDetector
from .magic_numbers_detector import MagicNumbersDetector
from .feature_envy_detector import FeatureEnvyDetector

__all__ = [
    'BaseDetector',
    'LongMethodDetector',
    'GodClassDetector', 
    'DuplicatedCodeDetector',
    'LargeParameterListDetector',
    'MagicNumbersDetector',
    'FeatureEnvyDetector'
]
