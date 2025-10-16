"""
Feature Envy Detector
Detects methods that use more data from other classes than their own
"""

from typing import List, Dict, Any, Set
import ast
from .base_detector import BaseDetector


class FeatureEnvyDetector(BaseDetector):
    """Detects feature envy by analyzing method access patterns"""
    
    def detect(self, file_path: str, source_code: str) -> List[Dict[str, Any]]:
        """Detect feature envy in the source code"""
        if not self.is_enabled():
            return []
        
        smells = []
        tree = self.parse_ast(source_code)
        if not tree:
            return smells
        
        min_foreign_accesses = self.get_threshold('min_foreign_accesses', 3)
        foreign_access_ratio = self.get_threshold('foreign_access_ratio', 1.5)
        
        # Find all classes and their methods
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes[node.name] = node
        
        # Analyze each method for feature envy
        for class_name, class_node in classes.items():
            for method_node in class_node.body:
                if isinstance(method_node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    envy_analysis = self._analyze_feature_envy(
                        method_node, class_name, classes, source_code
                    )
                    
                    if envy_analysis['is_feature_envy']:
                        smell = self.create_smell_instance(
                            file_path=file_path,
                            line_number=method_node.lineno,
                            severity="medium",
                            message=f"Method '{method_node.name}' shows feature envy (foreign accesses: {envy_analysis['foreign_accesses']}, self accesses: {envy_analysis['self_accesses']})",
                            details={
                                "method_name": method_node.name,
                                "class_name": class_name,
                                "foreign_accesses": envy_analysis['foreign_accesses'],
                                "self_accesses": envy_analysis['self_accesses'],
                                "foreign_ratio": envy_analysis['foreign_ratio'],
                                "min_foreign_accesses": min_foreign_accesses,
                                "foreign_access_ratio": foreign_access_ratio,
                                "foreign_classes": envy_analysis['foreign_classes']
                            }
                        )
                        smells.append(smell)
        
        return smells
    
    def _analyze_feature_envy(self, method_node: ast.FunctionDef, class_name: str, 
                             classes: Dict[str, ast.ClassDef], source_code: str) -> Dict[str, Any]:
        """Analyze a method for feature envy patterns"""
        foreign_accesses = 0
        self_accesses = 0
        foreign_classes = set()
        
        # Analyze all attribute accesses in the method
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                # Check if it's accessing another class's attributes
                if isinstance(node.value, ast.Name):
                    var_name = node.value.id
                    if var_name in classes and var_name != class_name:
                        foreign_accesses += 1
                        foreign_classes.add(var_name)
                    elif var_name == 'self':
                        self_accesses += 1
                elif isinstance(node.value, ast.Attribute):
                    # Handle chained attribute access like obj.attr.method()
                    if self._is_foreign_access(node.value, class_name, classes):
                        foreign_accesses += 1
                        foreign_classes.add(self._get_class_name(node.value))
                    elif self._is_self_access(node.value):
                        self_accesses += 1
                elif isinstance(node.value, ast.Call):
                    # Handle method calls on other objects
                    if self._is_foreign_method_call(node.value, class_name, classes):
                        foreign_accesses += 1
                        foreign_classes.add(self._get_called_object_class(node.value, classes))
                    elif self._is_self_method_call(node.value):
                        self_accesses += 1
        
        # Also check for direct access to other class instances (like self.restaurant.something)
        for node in ast.walk(method_node):
            if isinstance(node, ast.Attribute):
                if (isinstance(node.value, ast.Attribute) and 
                    isinstance(node.value.value, ast.Name) and 
                    node.value.value.id == 'self' and
                    node.value.attr in ['restaurant', 'manager', 'service', 'store', 'data']):  # Common patterns
                    foreign_accesses += 1
                    foreign_classes.add('ExternalService')
                # Also check for deeper chaining like self.restaurant.menu_items
                elif (isinstance(node.value, ast.Attribute) and 
                      isinstance(node.value.value, ast.Attribute) and
                      isinstance(node.value.value.value, ast.Name) and
                      node.value.value.value.id == 'self' and
                      node.value.value.attr in ['restaurant', 'manager', 'service', 'store', 'data']):
                    foreign_accesses += 1
                    foreign_classes.add('ExternalService')
        
        # Calculate foreign access ratio
        foreign_ratio = foreign_accesses / max(self_accesses, 1)
        
        # Determine if it's feature envy
        is_feature_envy = (
            foreign_accesses >= 2 and  # At least 2 foreign accesses
            foreign_ratio >= 0.5      # Foreign accesses are significant compared to self accesses
        )
        
        return {
            'is_feature_envy': is_feature_envy,
            'foreign_accesses': foreign_accesses,
            'self_accesses': self_accesses,
            'foreign_ratio': foreign_ratio,
            'foreign_classes': list(foreign_classes)
        }
    
    def _is_foreign_access(self, node: ast.Attribute, class_name: str, 
                          classes: Dict[str, ast.ClassDef]) -> bool:
        """Check if an attribute access is to a foreign class"""
        if isinstance(node.value, ast.Name):
            return node.value.id in classes and node.value.id != class_name
        elif isinstance(node.value, ast.Attribute):
            return self._is_foreign_access(node.value, class_name, classes)
        return False
    
    def _is_self_access(self, node: ast.Attribute) -> bool:
        """Check if an attribute access is to self"""
        if isinstance(node.value, ast.Name):
            return node.value.id == 'self'
        elif isinstance(node.value, ast.Attribute):
            return self._is_self_access(node.value)
        return False
    
    def _get_class_name(self, node: ast.Attribute) -> str:
        """Get the class name from an attribute access"""
        if isinstance(node.value, ast.Name):
            return node.value.id
        elif isinstance(node.value, ast.Attribute):
            return self._get_class_name(node.value)
        return "unknown"
    
    def _is_foreign_method_call(self, node: ast.Call, class_name: str, classes: Dict[str, ast.ClassDef]) -> bool:
        """Check if a method call is on a foreign object"""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return node.func.value.id in classes and node.func.value.id != class_name
            elif isinstance(node.func.value, ast.Attribute):
                return self._is_foreign_access(node.func.value, class_name, classes)
        return False
    
    def _is_self_method_call(self, node: ast.Call) -> bool:
        """Check if a method call is on self"""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return node.func.value.id == 'self'
            elif isinstance(node.func.value, ast.Attribute):
                return self._is_self_access(node.func.value)
        return False
    
    def _get_called_object_class(self, node: ast.Call, classes: Dict[str, ast.ClassDef]) -> str:
        """Get the class name of the object being called"""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return node.func.value.id
            elif isinstance(node.func.value, ast.Attribute):
                return self._get_class_name(node.func.value)
        return "unknown"
