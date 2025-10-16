"""
God Class Detector
Detects classes that have too many responsibilities, methods, or fields
"""

from typing import List, Dict, Any
import ast
from .base_detector import BaseDetector


class GodClassDetector(BaseDetector):
    """Detects god classes based on field count, method count, and responsibilities"""
    
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """Detect god classes in the source code"""
        if not self.is_enabled():
            return []
        
        smells = []
        tree = self.parse_ast(source_code)
        if not tree:
            return smells
        
        max_fields = self.get_threshold('max_fields', 15)
        max_methods = self.get_threshold('max_methods', 20)
        max_lines = self.get_threshold('max_lines', 200)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_smells = self._analyze_class(node, file_path, source_code, max_fields, max_methods, max_lines)
                smells.extend(class_smells)
        
        return smells
    
    def _analyze_class(self, class_node: ast.ClassDef, file_path: str, 
                      source_code: str, max_fields: int, max_methods: int, max_lines: int) -> List[Dict[str, Any]]:
        """Analyze a single class for god class smell"""
        smells = []
        
        # Count fields and methods
        fields = self._count_fields(class_node)
        methods = self._count_methods(class_node)
        class_lines = self._count_class_lines(class_node, source_code)
        
        # Check field count
        if fields > max_fields:
            smell = self.create_smell_instance(
                file_path=file_path,
                line_number=class_node.lineno,
                severity="high" if fields > max_fields * 1.5 else "medium",
                message=f"Class '{class_node.name}' has too many fields ({fields}, max: {max_fields})",
                details={
                    "class_name": class_node.name,
                    "field_count": fields,
                    "max_fields": max_fields,
                    "method_count": methods,
                    "max_methods": max_methods,
                    "line_count": class_lines,
                    "max_lines": max_lines
                }
            )
            smells.append(smell)
        
        # Check method count
        if methods > max_methods:
            smell = self.create_smell_instance(
                file_path=file_path,
                line_number=class_node.lineno,
                severity="high" if methods > max_methods * 1.5 else "medium",
                message=f"Class '{class_node.name}' has too many methods ({methods}, max: {max_methods})",
                details={
                    "class_name": class_node.name,
                    "field_count": fields,
                    "max_fields": max_fields,
                    "method_count": methods,
                    "max_methods": max_methods,
                    "line_count": class_lines,
                    "max_lines": max_lines
                }
            )
            smells.append(smell)
        
        # Check class size
        if class_lines > max_lines:
            smell = self.create_smell_instance(
                file_path=file_path,
                line_number=class_node.lineno,
                severity="high" if class_lines > max_lines * 1.5 else "medium",
                message=f"Class '{class_node.name}' is too large ({class_lines} lines, max: {max_lines})",
                details={
                    "class_name": class_node.name,
                    "field_count": fields,
                    "max_fields": max_fields,
                    "method_count": methods,
                    "max_methods": max_methods,
                    "line_count": class_lines,
                    "max_lines": max_lines
                }
            )
            smells.append(smell)
        
        return smells
    
    def _count_fields(self, class_node: ast.ClassDef) -> int:
        """Count the number of fields in a class"""
        field_count = 0
        
        for node in class_node.body:
            if isinstance(node, ast.Assign):
                # Check if it's a field assignment (not inside a method)
                field_count += len(node.targets)
            elif isinstance(node, ast.AnnAssign):
                # Type annotated assignment
                field_count += 1
        
        return field_count
    
    def _count_methods(self, class_node: ast.ClassDef) -> int:
        """Count the number of methods in a class"""
        method_count = 0
        
        for node in class_node.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_count += 1
        
        return method_count
    
    def _count_class_lines(self, class_node: ast.ClassDef, source_code: str) -> int:
        """Count the number of lines in a class"""
        lines = source_code.split('\n')
        
        start_line = class_node.lineno - 1
        end_line = start_line + 1
        
        # Get the indentation of the class
        class_line = lines[start_line]
        base_indent = len(class_line) - len(class_line.lstrip())
        
        # Find the end of the class
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
