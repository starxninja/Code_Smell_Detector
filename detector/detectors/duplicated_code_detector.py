"""
Duplicated Code Detector
Detects duplicated or similar code blocks
"""

from typing import List, Dict, Any, Set, Tuple
import ast
import hashlib
from .base_detector import BaseDetector


class DuplicatedCodeDetector(BaseDetector):
    """Detects duplicated code using AST-based similarity analysis"""
    
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """Detect duplicated code in the source code"""
        if not self.is_enabled():
            return []
        
        smells = []
        tree = self.parse_ast(source_code)
        if not tree:
            return smells
        
        min_similarity = self.get_threshold('min_similarity', 0.8)
        min_chunk_size = self.get_threshold('min_chunk_size', 3)
        
        # Find all function definitions
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node)
        
        # Compare functions for similarity
        for i, func1 in enumerate(functions):
            for j, func2 in enumerate(functions[i+1:], i+1):
                similarity = self._calculate_similarity(func1, func2, source_code)
                if similarity >= min_similarity:
                    # Check if functions are large enough
                    func1_lines = self._count_function_lines(func1, source_code)
                    func2_lines = self._count_function_lines(func2, source_code)
                    
                    if func1_lines >= min_chunk_size and func2_lines >= min_chunk_size:
                        smell = self.create_smell_instance(
                            file_path=file_path,
                            line_number=func1.lineno,
                            severity="medium",
                            message=f"Duplicated code detected between '{func1.name}' and '{func2.name}' (similarity: {similarity:.2f})",
                            details={
                                "function1": func1.name,
                                "function2": func2.name,
                                "function1_line": func1.lineno,
                                "function2_line": func2.lineno,
                                "similarity": similarity,
                                "min_similarity": min_similarity,
                                "function1_lines": func1_lines,
                                "function2_lines": func2_lines
                            }
                        )
                        smells.append(smell)
        
        return smells
    
    def _calculate_similarity(self, func1: ast.FunctionDef, func2: ast.FunctionDef, source_code: str) -> float:
        """Calculate similarity between two functions"""
        # Extract function bodies
        body1 = self._extract_function_body(func1, source_code)
        body2 = self._extract_function_body(func2, source_code)
        
        if not body1 or not body2:
            return 0.0
        
        # Normalize whitespace and comments
        body1_normalized = self._normalize_code(body1)
        body2_normalized = self._normalize_code(body2)
        
        # Calculate similarity using multiple methods
        similarity1 = self._string_similarity(body1_normalized, body2_normalized)
        similarity2 = self._pattern_similarity(body1_normalized, body2_normalized)
        
        # Return the higher similarity score
        return max(similarity1, similarity2)
    
    def _extract_function_body(self, func: ast.FunctionDef, source_code: str) -> str:
        """Extract the body of a function as a string"""
        lines = source_code.split('\n')
        
        start_line = func.lineno - 1
        end_line = start_line + 1
        
        # Get the indentation of the function
        func_line = lines[start_line]
        base_indent = len(func_line) - len(func_line.lstrip())
        
        # Find the end of the function
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
        
        # Extract function body (skip the def line)
        body_lines = lines[start_line + 1:end_line]
        return '\n'.join(body_lines)
    
    def _normalize_code(self, code: str) -> str:
        """Normalize code by removing comments and normalizing whitespace"""
        lines = code.split('\n')
        normalized_lines = []
        
        for line in lines:
            # Remove comments
            if '#' in line:
                line = line[:line.index('#')]
            
            # Normalize whitespace
            line = line.strip()
            if line:
                normalized_lines.append(line)
        
        return '\n'.join(normalized_lines)
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings using Jaccard similarity"""
        if not str1 or not str2:
            return 0.0
        
        # Split into words/tokens
        tokens1 = set(str1.split())
        tokens2 = set(str2.split())
        
        if not tokens1 and not tokens2:
            return 1.0
        
        if not tokens1 or not tokens2:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0
    
    def _count_function_lines(self, func: ast.FunctionDef, source_code: str) -> int:
        """Count the number of lines in a function"""
        lines = source_code.split('\n')
        
        start_line = func.lineno - 1
        end_line = start_line + 1
        
        # Get the indentation of the function
        func_line = lines[start_line]
        base_indent = len(func_line) - len(func_line.lstrip())
        
        # Find the end of the function
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
    
    def _pattern_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity based on code patterns and structure"""
        # Look for common patterns like if-elif-else chains, variable assignments, etc.
        patterns1 = self._extract_patterns(code1)
        patterns2 = self._extract_patterns(code2)
        
        if not patterns1 and not patterns2:
            return 1.0
        
        if not patterns1 or not patterns2:
            return 0.0
        
        # Calculate pattern similarity
        common_patterns = 0
        total_patterns = len(patterns1) + len(patterns2)
        
        for pattern in patterns1:
            if pattern in patterns2:
                common_patterns += 2  # Count both occurrences
                patterns2.remove(pattern)  # Avoid double counting
        
        return common_patterns / total_patterns if total_patterns > 0 else 0.0
    
    def _extract_patterns(self, code: str) -> List[str]:
        """Extract structural patterns from code"""
        patterns = []
        lines = code.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Extract if-elif-else patterns
            if line.startswith('if ') or line.startswith('elif ') or line.startswith('else:'):
                patterns.append('conditional')
            
            # Extract assignment patterns
            if ' = ' in line and not line.startswith('#'):
                patterns.append('assignment')
            
            # Extract method call patterns
            if '(' in line and ')' in line and not line.startswith('#'):
                patterns.append('method_call')
            
            # Extract return patterns
            if line.startswith('return '):
                patterns.append('return')
            
            # Extract specific loyalty discount patterns
            if 'loyalty_level' in line or 'discount_rate' in line or 'reward_rate' in line:
                patterns.append('loyalty_logic')
            
            # Extract tier-based logic patterns
            if 'tier' in line.lower() or 'level' in line.lower():
                patterns.append('tier_logic')
        
        return patterns
