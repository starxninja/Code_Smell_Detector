"""
Large Parameter List Detector
Detects methods with too many parameters
"""

from typing import List, Dict, Any
import ast
from .base_detector import BaseDetector


class LargeParameterListDetector(BaseDetector):
    """Detects methods with too many parameters"""
    
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """Detect large parameter lists in the source code"""
        if not self.is_enabled():
            return []
        
        smells = []
        tree = self.parse_ast(source_code)
        if not tree:
            return smells
        
        max_parameters = self.get_threshold('max_parameters', 5)
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                param_count = self._count_parameters(node)
                
                if param_count > max_parameters:
                    smell = self.create_smell_instance(
                        file_path=file_path,
                        line_number=node.lineno,
                        severity="high" if param_count > max_parameters * 2 else "medium",
                        message=f"Method '{node.name}' has too many parameters ({param_count}, max: {max_parameters})",
                        details={
                            "method_name": node.name,
                            "parameter_count": param_count,
                            "max_parameters": max_parameters,
                            "parameters": [arg.arg for arg in node.args.args]
                        }
                    )
                    smells.append(smell)
        
        return smells
    
    def _count_parameters(self, func_node: ast.FunctionDef) -> int:
        """Count the number of parameters in a function"""
        param_count = 0
        
        # Count regular arguments
        param_count += len(func_node.args.args)
        
        # Count keyword-only arguments
        if func_node.args.kwonlyargs:
            param_count += len(func_node.args.kwonlyargs)
        
        # Count positional-only arguments
        if func_node.args.posonlyargs:
            param_count += len(func_node.args.posonlyargs)
        
        return param_count
