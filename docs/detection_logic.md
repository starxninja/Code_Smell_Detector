# Code Smell Detection Logic Documentation

## Overview
This document explains the detection algorithms, thresholds, and reasoning behind each code smell detector in our application.

---

## 1. Long Method Detector

### Detection Algorithm
The Long Method detector identifies methods that exceed specified thresholds for:
- **Lines of Code (LOC)**: Total lines in the method body
- **Cyclomatic Complexity**: Number of decision points (if, for, while, etc.)

### Thresholds and Reasoning

| Threshold | Value | Justification |
|-----------|-------|---------------|
| **Max Lines** | 30 | Based on industry standards and readability research. Methods over 30 lines become difficult to understand and maintain. Studies show optimal method length is 10-20 lines. |
| **Max Complexity** | 10 | Cyclomatic complexity of 10+ indicates high cognitive load. Each decision point adds mental overhead, making code harder to test and debug. |

### Implementation Details
```python
def detect_long_method(self, method_node):
    line_count = method_node.end_lineno - method_node.lineno
    complexity = self.calculate_cyclomatic_complexity(method_node)
    
    if line_count > self.max_lines or complexity > self.max_complexity:
        return True
```

### Why These Thresholds?
- **30 lines**: Allows for reasonable business logic while maintaining readability
- **10 complexity**: Balances functionality with testability (each branch needs testing)

---

## 2. God Class (Blob) Detector

### Detection Algorithm
Identifies classes that violate Single Responsibility Principle by having:
- Too many fields (instance variables)
- Too many methods
- Excessive total lines

### Thresholds and Reasoning

| Threshold | Value | Justification |
|-----------|-------|---------------|
| **Max Fields** | 15 | Classes with 15+ fields typically handle multiple concerns. Each field represents state that needs to be managed and understood. |
| **Max Methods** | 20 | Methods represent behaviors. 20+ methods suggest the class is doing too much and should be split. |
| **Max Lines** | 200 | Large classes are hard to navigate and understand. 200 lines is a reasonable limit for maintainability. |

### Implementation Details
```python
def detect_god_class(self, class_node):
    field_count = len([node for node in class_node.body if isinstance(node, ast.Assign)])
    method_count = len([node for node in class_node.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))])
    line_count = class_node.end_lineno - class_node.lineno
    
    return (field_count > self.max_fields or 
            method_count > self.max_methods or 
            line_count > self.max_lines)
```

### Why These Thresholds?
- **15 fields**: Each field adds coupling and complexity
- **20 methods**: Indicates multiple responsibilities
- **200 lines**: Maintains class cohesion and readability

---

## 3. Duplicated Code Detector

### Detection Algorithm
Uses multiple similarity metrics to identify code duplication:
- **String Similarity**: Jaccard similarity on normalized code tokens
- **Pattern Similarity**: Structural pattern matching (if-else, loops, assignments)

### Thresholds and Reasoning

| Threshold | Value | Justification |
|-----------|-------|---------------|
| **Min Similarity** | 0.8 (80%) | 80% similarity indicates significant code duplication. Lower values would catch too many false positives. |
| **Min Chunk Size** | 3 lines | Prevents flagging trivial similarities. 3+ lines indicate meaningful duplication. |

### Implementation Details
```python
def calculate_similarity(self, func1, func2):
    # Normalize code (remove comments, whitespace)
    body1_normalized = self._normalize_code(body1)
    body2_normalized = self._normalize_code(body2)
    
    # Calculate multiple similarity metrics
    string_sim = self._string_similarity(body1_normalized, body2_normalized)
    pattern_sim = self._pattern_similarity(body1_normalized, body2_normalized)
    
    return max(string_sim, pattern_sim)
```

### Why These Thresholds?
- **80% similarity**: High enough to catch real duplication, low enough to avoid false positives
- **3 lines minimum**: Ensures meaningful code blocks are compared

---

## 4. Large Parameter List Detector

### Detection Algorithm
Counts method parameters and flags methods exceeding the threshold.

### Thresholds and Reasoning

| Threshold | Value | Justification |
|-----------|-------|---------------|
| **Max Parameters** | 5 | Research shows 5+ parameters significantly reduce code readability and increase error rates. The "Rule of 5" is widely accepted in software engineering. |

### Implementation Details
```python
def detect_large_parameter_list(self, method_node):
    param_count = len(method_node.args.args)
    # Exclude 'self' parameter for instance methods
    if param_count > 1 and method_node.args.args[0].arg == 'self':
        param_count -= 1
    
    return param_count > self.max_parameters
```

### Why This Threshold?
- **5 parameters**: Based on cognitive load research and industry best practices
- **Excludes 'self'**: Instance methods naturally have 'self' parameter

---

## 5. Magic Numbers Detector

### Detection Algorithm
Identifies hard-coded numeric literals that appear frequently without explanation.

### Thresholds and Reasoning

| Threshold | Value | Justification |
|-----------|-------|---------------|
| **Min Occurrences** | 3 | Numbers appearing 3+ times likely represent constants that should be named |
| **Min Value** | 2 | Excludes 0, 1, -1 which are often legitimate (array indices, flags) |
| **Max Value** | 1000 | Focuses on business logic numbers, not large technical values |
| **Whitelist** | [0, 1, -1] | Common programming values that are usually acceptable |

### Implementation Details
```python
def detect_magic_numbers(self, tree):
    number_occurrences = {}
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            value = node.value
            if (self.min_value <= value <= self.max_value and 
                value not in self.whitelist):
                number_occurrences[value] = number_occurrences.get(value, 0) + 1
    
    return [num for num, count in number_occurrences.items() 
            if count >= self.min_occurrences]
```

### Why These Thresholds?
- **3 occurrences**: Indicates repeated use, suggesting a constant
- **2-1000 range**: Focuses on business logic, not technical constants
- **Whitelist**: Excludes common programming values

---

## 6. Feature Envy Detector

### Detection Algorithm
Analyzes method behavior to identify methods that access external class data more than their own.

### Thresholds and Reasoning

| Threshold | Value | Justification |
|-----------|-------|---------------|
| **Min Foreign Accesses** | 2 | Methods accessing 2+ external attributes show dependency on other classes |
| **Foreign Access Ratio** | 0.5 | When foreign accesses are 50%+ of total accesses, method likely belongs elsewhere |

### Implementation Details
```python
def analyze_feature_envy(self, method_node, class_name, classes):
    foreign_accesses = 0
    self_accesses = 0
    
    for node in ast.walk(method_node):
        if isinstance(node, ast.Attribute):
            if self._is_foreign_access(node, class_name, classes):
                foreign_accesses += 1
            elif self._is_self_access(node):
                self_accesses += 1
    
    foreign_ratio = foreign_accesses / max(self_accesses, 1)
    
    return (foreign_accesses >= 2 and foreign_ratio >= 0.5)
```

### Why These Thresholds?
- **2 foreign accesses**: Indicates significant dependency on external data
- **0.5 ratio**: When half or more accesses are external, method likely belongs elsewhere

---

## Configuration System

### Config File Structure
```yaml
language: "python"

LongMethod:
  enabled: true
  max_lines: 30
  max_complexity: 10

GodClass:
  enabled: true
  max_fields: 15
  max_methods: 20
  max_lines: 200

DuplicatedCode:
  enabled: true
  min_similarity: 0.8
  min_chunk_size: 3

LargeParameterList:
  enabled: true
  max_parameters: 5

MagicNumbers:
  enabled: true
  min_occurrences: 3
  whitelist: [0, 1, -1]
  min_value: 2
  max_value: 1000

FeatureEnvy:
  enabled: true
  min_foreign_accesses: 2
  foreign_access_ratio: 0.5
```

### CLI Override System
- `--only LongMethod,DuplicatedCode`: Run only specified detectors
- `--exclude MagicNumbers`: Run all except specified detectors
- CLI flags override config file settings

---

## Detection Accuracy and Limitations

### Strengths
1. **AST-based analysis**: Provides accurate structural understanding
2. **Multiple similarity metrics**: Reduces false positives in duplication detection
3. **Configurable thresholds**: Allows tuning for different codebases
4. **Comprehensive coverage**: Detects all major code smell categories

### Limitations
1. **Context awareness**: May flag legitimate patterns in certain domains
2. **Semantic analysis**: Limited understanding of business logic context
3. **Refactoring suggestions**: Provides detection but not refactoring guidance

### Future Improvements
1. **Machine learning integration**: Learn from codebase-specific patterns
2. **Refactoring suggestions**: Provide specific improvement recommendations
3. **Historical analysis**: Track smell evolution over time
4. **Team-specific thresholds**: Adapt to team coding standards

---

## Conclusion

Our detection system uses industry-standard thresholds and proven algorithms to identify code smells effectively. The configurable nature allows adaptation to different coding standards and project requirements while maintaining consistency and accuracy in detection.
