"""
Long Method Detector
Detects methods that are too long (exceed line count or cyclomatic complexity thresholds)
"""

from typing import List, Dict, Any
import ast
from .base_detector import BaseDetector


class LongMethodDetector(BaseDetector):
    """Detects long methods based on line count and cyclomatic complexity"""
    
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """Detect long methods in the source code"""
        if not self.is_enabled():
            return []
        
        smells = []
        tree = self.parse_ast(source_code)
        if not tree:
            return smells
        
        max_lines = self.get_threshold('max_lines', 30)
        max_complexity = self.get_threshold('max_complexity', 10)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                method_smells = self._analyze_method(node, file_path, source_code, max_lines, max_complexity)
                smells.extend(method_smells)
        
        return smells
    
    def _analyze_method(self, method_node: ast.FunctionDef, file_path: str, 
                       source_code: str, max_lines: int, max_complexity: int) -> List[Dict[str, Any]]:
        """Analyze a single method for long method smell"""
        smells = []
        
        # Calculate method length
        method_lines = self._count_method_lines(method_node, source_code)
        complexity = self._calculate_complexity(method_node)
        
        # Check line count threshold
        if method_lines > max_lines:
            smell = self.create_smell_instance(
                file_path=file_path,
                line_number=method_node.lineno,
                severity="high" if method_lines > max_lines * 1.5 else "medium",
                message=f"Method '{method_node.name}' is too long ({method_lines} lines, max: {max_lines})",
                details={
                    "method_name": method_node.name,
                    "line_count": method_lines,
                    "max_lines": max_lines,
                    "complexity": complexity,
                    "max_complexity": max_complexity
                }
            )
            smells.append(smell)
        
        # Check cyclomatic complexity
        if complexity > max_complexity:
            smell = self.create_smell_instance(
                file_path=file_path,
                line_number=method_node.lineno,
                severity="high" if complexity > max_complexity * 1.5 else "medium",
                message=f"Method '{method_node.name}' has high complexity ({complexity}, max: {max_complexity})",
                details={
                    "method_name": method_node.name,
                    "line_count": method_lines,
                    "max_lines": max_lines,
                    "complexity": complexity,
                    "max_complexity": max_complexity
                }
            )
            smells.append(smell)
        
        return smells
    
    def _count_method_lines(self, method_node: ast.FunctionDef, source_code: str) -> int:
        """Count the number of lines in a method"""
        lines = source_code.split('\n')
        
        # Find the end of the method by looking for the next function/class at same indentation
        start_line = method_node.lineno - 1
        end_line = start_line + 1
        
        # Get the indentation of the method
        method_line = lines[start_line]
        base_indent = len(method_line) - len(method_line.lstrip())
        
        # Find the end of the method
        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if line.strip() == "":
                continue
            
            current_indent = len(line) - len(line.lstrip())
            if current_indent <= base_indent and line.strip():
                end_line = i
                break
        else:
            end_line = len(lines)
        
        return end_line - start_line
    
    def _calculate_complexity(self, method_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a method"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(method_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        
        return complexity
