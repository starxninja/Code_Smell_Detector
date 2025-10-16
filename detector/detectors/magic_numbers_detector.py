"""
Magic Numbers Detector
Detects hard-coded numeric literals without explanation
"""

from typing import List, Dict, Any, Tuple
import ast
import re
from .base_detector import BaseDetector


class MagicNumbersDetector(BaseDetector):
    """Detects magic numbers in the source code"""
    
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """Detect magic numbers in the source code"""
        if not self.is_enabled():
            return []
        
        smells = []
        tree = self.parse_ast(source_code)
        if not tree:
            return smells
        
        min_occurrences = self.get_threshold('min_occurrences', 3)
        whitelist = self.get_threshold('whitelist', [0, 1, -1])
        min_value = self.get_threshold('min_value', 2)
        max_value = self.get_threshold('max_value', 1000)
        
        # Find all numeric literals
        magic_numbers = self._find_magic_numbers(tree, whitelist, min_value, max_value)
        
        # Group by value and count occurrences
        number_counts = {}
        for number, line_num in magic_numbers:
            if number not in number_counts:
                number_counts[number] = []
            number_counts[number].append(line_num)
        
        # Report numbers that appear frequently
        for number, line_numbers in number_counts.items():
            if len(line_numbers) >= min_occurrences:
                smell = self.create_smell_instance(
                    file_path=file_path,
                    line_number=line_numbers[0],
                    severity="medium",
                    message=f"Magic number '{number}' appears {len(line_numbers)} times",
                    details={
                        "magic_number": number,
                        "occurrences": len(line_numbers),
                        "line_numbers": line_numbers,
                        "min_occurrences": min_occurrences,
                        "whitelist": whitelist
                    }
                )
                smells.append(smell)
        
        return smells
    
    def _find_magic_numbers(self, tree: ast.AST, whitelist: List[int], 
                           min_value: int, max_value: int) -> List[Tuple[float, int]]:
        """Find all magic numbers in the AST"""
        magic_numbers = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                value = node.value
                if (value not in whitelist and 
                    min_value <= abs(value) <= max_value and
                    not self._is_in_constant_definition(node, tree)):
                    magic_numbers.append((value, node.lineno))
            elif isinstance(node, ast.Num):  # Python < 3.8 compatibility
                value = node.n
                if (value not in whitelist and 
                    min_value <= abs(value) <= max_value and
                    not self._is_in_constant_definition(node, tree)):
                    magic_numbers.append((value, node.lineno))
        
        return magic_numbers
    
    def _is_in_constant_definition(self, node: ast.AST, tree: ast.AST) -> bool:
        """Check if the number is part of a constant definition"""
        # Look for assignment patterns like CONSTANT = 42
        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.Assign):
                for target in ast_node.targets:
                    if isinstance(target, ast.Name):
                        # Check if the name suggests it's a constant
                        name = target.id.upper()
                        if (name.isupper() or 
                            name.startswith('MAX_') or 
                            name.startswith('MIN_') or
                            name.startswith('DEFAULT_') or
                            name.endswith('_LIMIT') or
                            name.endswith('_THRESHOLD')):
                            # Check if our node is in this assignment
                            if self._node_in_subtree(node, ast_node):
                                return True
        return False
    
    def _node_in_subtree(self, target_node: ast.AST, parent_node: ast.AST) -> bool:
        """Check if target_node is within parent_node's subtree"""
        for child in ast.iter_child_nodes(parent_node):
            if child is target_node:
                return True
            if self._node_in_subtree(target_node, child):
                return True
        return False
