"""
Base detector class for code smell detection
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import ast


class BaseDetector(ABC):
    """Base class for all code smell detectors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.smell_name = self.__class__.__name__.replace('Detector', '')
        
    @abstractmethod
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """
        Detect code smells in the given source code
        
        Args:
            file_path: Path to the source file
            source_code: Content of the source file
            
        Returns:
            List of detected smell instances with details
        """
        pass
    
    def parse_ast(self, source_code: str) -> Optional[ast.AST]:
        """Parse source code into AST"""
        try:
            return ast.parse(source_code)
        except SyntaxError as e:
            print(f"Syntax error in source code: {e}")
            return None
    
    def get_line_content(self, source_code: str, line_number: int) -> str:
        """Get content of a specific line"""
        lines = source_code.split('\n')
        if 1 <= line_number <= len(lines):
            return lines[line_number - 1]
        return ""
    
    def get_line_range_content(self, source_code: str, start_line: int, end_line: int) -> List[str]:
        """Get content of a range of lines"""
        lines = source_code.split('\n')
        if 1 <= start_line <= end_line <= len(lines):
            return lines[start_line - 1:end_line]
        return []
    
    def count_lines(self, source_code: str) -> int:
        """Count total lines in source code"""
        return len(source_code.split('\n'))
    
    def is_enabled(self) -> bool:
        """Check if this detector is enabled in config"""
        detector_config = self.config.get(self.smell_name, {})
        if isinstance(detector_config, dict):
            return detector_config.get('enabled', True)
        return bool(detector_config)
    
    def get_threshold(self, threshold_name: str, default: Any = None) -> Any:
        """Get threshold value from config"""
        detector_config = self.config.get(self.smell_name, {})
        if isinstance(detector_config, dict):
            return detector_config.get(threshold_name, default)
        return default
    
    def create_smell_instance(self, 
                            file_path: str, 
                            line_number: int, 
                            severity: str = "medium",
                            message: str = "",
                            details: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized smell instance"""
        return {
            "smell_type": self.smell_name,
            "file_path": file_path,
            "line_number": line_number,
            "severity": severity,
            "message": message,
            "details": details or {}
        }
