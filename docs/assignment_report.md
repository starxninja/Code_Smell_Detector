# Code Smell Detection Application - Assignment Report

**Course**: Software Engineering  
**Assignment**: Code Smell Detection and Analysis  
**Team**: Individual Submission  
**Date**: October 2024  

---

## 1. Introduction

This report presents the development and evaluation of a comprehensive code smell detection application designed to identify common software maintenance issues in Python codebases. The project addresses the critical need for automated code quality assessment tools that can help developers identify and refactor problematic code patterns before they become significant technical debt.

The application successfully implements detection algorithms for six fundamental code smells: Long Method, God Class (Blob), Duplicated Code, Large Parameter List, Magic Numbers, and Feature Envy. Through deliberate introduction of these smells in a test application and subsequent detection validation, we demonstrate the effectiveness of our detection mechanisms and their practical applicability in real-world software development scenarios.

The project consists of two main components: (1) a deliberately "smelly" restaurant management system containing all six code smell types, and (2) a sophisticated detection application with configurable thresholds and comprehensive reporting capabilities.

---

## 2. Code Smells Introduced and Analysis

### 2.1 Long Method Smell

**Location**: `restaurant_manager.py`, Lines 22-105  
**Method**: `process_reservation_and_order()`  
**Lines of Code**: 84 lines  
**Cyclomatic Complexity**: 16  

**Why Introduced**: This method was deliberately designed to handle multiple responsibilities in a single function, violating the Single Responsibility Principle. The method performs seating validation, menu item verification, discount calculation, billing computation, inventory updates, and reservation creation all within one function.

**Impact**: The method's excessive length and complexity make it difficult to understand, test, and maintain. Any modification to seating logic, billing rules, or inventory management requires changes to this monolithic method, increasing the risk of introducing bugs and making the codebase fragile.

**Detection Results**: Successfully detected with 84 lines (threshold: 30) and complexity 16 (threshold: 10).

### 2.2 God Class (Blob) Smell

**Location**: `restaurant_manager.py`, Lines 6-231  
**Class**: `RestaurantManager`  
**Total Lines**: 227 lines  
**Methods**: 10 methods  
**Instance Variables**: 9 fields  

**Why Introduced**: The `RestaurantManager` class was designed to handle all aspects of restaurant operations including menu management, guest registration, reservation processing, billing calculations, stock management, and basic reporting. This creates a class with too many responsibilities and excessive coupling.

**Impact**: The class becomes a central point of failure where changes in one area can affect unrelated functionality. The high coupling makes the system difficult to extend and maintain, as adding new features requires modifying this already complex class.

**Detection Results**: Successfully detected with 227 lines (threshold: 200), confirming the class exceeds acceptable size limits.

### 2.3 Duplicated Code Smell

**Location**: `restaurant_manager.py`, Multiple locations  
**Instances**:
- Lines 60-65: `process_reservation_and_order()` discount logic
- Lines 175-181: `compute_loyalty_reward()` discount logic  
- Lines 208-214: `apply_happy_hour_discount()` discount logic

**Why Introduced**: The identical loyalty discount calculation logic (0.03 for level 1, 0.08 for level 2, 0.12 for level 3) was deliberately repeated across three different methods without abstraction to demonstrate the maintenance problems caused by code duplication.

**Impact**: This duplication creates a maintenance nightmare where discount rate changes must be made in multiple places, increasing the likelihood of inconsistencies and bugs. The repeated logic also violates the DRY (Don't Repeat Yourself) principle.

**Detection Results**: Successfully detected 6 instances of duplicated code with similarity scores ranging from 0.86 to 1.00, including the loyalty discount logic patterns.

### 2.4 Large Parameter List Smell

**Location**: `restaurant_manager.py`, Lines 107-124  
**Method**: `add_menu_item()`  
**Parameters**: 10 parameters (excluding 'self')  

**Why Introduced**: The method was designed to accept individual parameters for all menu item attributes (name, price, category, ingredients, prep_time, calories, allergens, portion_size, spice_level) to demonstrate the problems with excessive parameter lists.

**Impact**: The large number of parameters makes method calls error-prone and difficult to read. Callers must remember parameter order and provide values for all parameters even when not needed. This increases cognitive load and makes the API hard to use.

**Detection Results**: Successfully detected with 10 parameters (threshold: 5), confirming the method exceeds acceptable parameter count.

### 2.5 Magic Numbers Smell

**Location**: `restaurant_manager.py`, Multiple locations  
**Instances**:
- Lines 62, 178, 211: Magic number '2' (3 occurrences)
- Lines 64, 180, 213, 310: Magic number '3' (4 occurrences)
- Lines 34-39: Discount rates (0.03, 0.08, 0.12)
- Lines 94-99: Prep time multipliers (1.5, 0.8, 1.2)
- Line 105: Initial guest balance (500.0)

**Why Introduced**: Hard-coded numeric values were scattered throughout the code without explanation or named constants to demonstrate the readability and maintainability issues caused by magic numbers.

**Impact**: These unexplained numbers make the code difficult to understand and modify. Future developers must guess the meaning and purpose of these values, leading to potential errors and inconsistent behavior.

**Detection Results**: Successfully detected magic numbers '2' and '3' with occurrence counts of 3 and 4 respectively, exceeding the minimum threshold of 3.

### 2.6 Feature Envy Smell

**Location**: `restaurant_manager.py`, Lines 240-286  
**Class**: `ReservationReporter`  
**Methods**: `get_best_selling_items()`, `get_guest_history()`, `get_top_guests()`  

**Why Introduced**: The `ReservationReporter` class methods were designed to access `RestaurantManager` data extensively (menu_items, guests, reservations) while having minimal interaction with their own class data, demonstrating poor cohesion and misplaced functionality.

**Impact**: These methods show "envy" for the data in another class, indicating they might belong in the `RestaurantManager` class instead. This creates unnecessary coupling and makes the code harder to maintain and understand.

**Detection Results**: Successfully detected 3 instances of feature envy with foreign access ratios ranging from 0.57 to 0.67, confirming excessive external data access.

---

## 3. Detection Logic and Thresholds

### 3.1 Detection Algorithm Overview

Our detection system uses Abstract Syntax Tree (AST) analysis to parse Python code and identify structural patterns associated with code smells. The system implements configurable thresholds based on industry best practices and empirical research on code maintainability.

### 3.2 Threshold Justification

**Long Method Detection**:
- **Lines of Code Threshold**: 30 lines
- **Cyclomatic Complexity Threshold**: 10
- **Rationale**: Research shows methods over 30 lines become difficult to understand and maintain. Cyclomatic complexity of 10+ indicates high cognitive load and testing complexity.

**God Class Detection**:
- **Max Fields**: 15
- **Max Methods**: 20  
- **Max Lines**: 200
- **Rationale**: Classes exceeding these limits typically violate Single Responsibility Principle and become difficult to maintain and test.

**Duplicated Code Detection**:
- **Similarity Threshold**: 80%
- **Min Chunk Size**: 3 lines
- **Rationale**: 80% similarity indicates significant duplication while avoiding false positives. 3+ lines ensure meaningful code blocks are compared.

**Large Parameter List Detection**:
- **Max Parameters**: 5
- **Rationale**: The "Rule of 5" is widely accepted in software engineering as the maximum number of parameters before readability and error rates significantly increase.

**Magic Numbers Detection**:
- **Min Occurrences**: 3
- **Value Range**: 2-1000
- **Whitelist**: [0, 1, -1]
- **Rationale**: Numbers appearing 3+ times likely represent constants. Focus on business logic values while excluding common programming constants.

**Feature Envy Detection**:
- **Min Foreign Accesses**: 2
- **Foreign Access Ratio**: 0.5
- **Rationale**: Methods accessing 2+ external attributes with 50%+ external access ratio likely belong in the accessed class.

### 3.3 Implementation Architecture

The detection system follows a modular architecture with:
- **Base Detector Class**: Common functionality for all detectors
- **Individual Detector Classes**: Specialized algorithms for each smell type
- **Configuration System**: YAML-based configuration with CLI overrides
- **Reporting System**: JSON output with detailed metrics and analysis

---

## 4. Example Outputs and Detection Results

### 4.1 Restaurant Management System Analysis

**Total Smells Detected**: 16  
**File**: `restaurant_manager.py` (308 lines)

**Detection Summary**:
- Long Method: 2 detections
- God Class: 1 detection  
- Duplicated Code: 6 detections
- Large Parameter List: 2 detections
- Magic Numbers: 2 detections
- Feature Envy: 3 detections

**Sample Detection Output**:
```json
{
  "smell_type": "LongMethod",
  "file_path": "restaurant_manager.py",
  "line_number": 22,
  "severity": "high",
  "message": "Method 'process_reservation_and_order' is too long (84 lines, max: 30)",
  "details": {
    "method_name": "process_reservation_and_order",
    "line_count": 84,
    "max_lines": 30,
    "complexity": 16,
    "max_complexity": 10
  }
}
```

### 4.2 External Sample Analysis

**Total Smells Detected**: 13  
**File**: `sample_smelly_code.py` (311 lines)

**Detection Summary**:
- Long Method: 3 detections
- God Class: 1 detection
- Duplicated Code: 2 detections  
- Large Parameter List: 2 detections
- Magic Numbers: 2 detections
- Feature Envy: 3 detections

### 4.3 Configuration and CLI Usage

**Config File Example**:
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
```

**CLI Usage Examples**:
```bash
# Run all detectors
python main.py restaurant_manager.py

# Run only specific detectors
python main.py restaurant_manager.py --only LongMethod,DuplicatedCode

# Exclude specific detectors
python main.py restaurant_manager.py --exclude MagicNumbers
```

---

## 5. Technical Debt and Maintainability Impact

### 5.1 Impact Analysis

The introduced code smells create significant technical debt that affects multiple aspects of software maintenance:

**Maintainability**: The God Class and Long Method smells make the codebase difficult to modify and extend. Changes require understanding large, complex code blocks with multiple responsibilities.

**Testability**: High cyclomatic complexity and large methods make comprehensive testing challenging. The duplicated code requires multiple test cases for the same logic.

**Readability**: Magic numbers and large parameter lists reduce code readability, making it harder for new developers to understand the system.

**Coupling**: Feature Envy creates unnecessary dependencies between classes, making the system more fragile and harder to refactor.

### 5.2 Refactoring Recommendations

**Long Method**: Break `process_reservation_and_order()` into smaller methods:
- `validate_seating_availability()`
- `calculate_bill_and_discounts()`
- `update_inventory_and_guest_data()`
- `create_reservation_record()`

**God Class**: Split `RestaurantManager` into specialized classes:
- `MenuManager`: Handle menu operations
- `GuestManager`: Manage guest data and loyalty
- `ReservationManager`: Process reservations
- `BillingManager`: Handle calculations

**Duplicated Code**: Extract common discount logic:
```python
def calculate_loyalty_discount(loyalty_level, amount):
    rates = {1: 0.03, 2: 0.08, 3: 0.12}
    return amount * rates.get(loyalty_level, 0)
```

**Large Parameter List**: Use data objects:
```python
@dataclass
class MenuItem:
    name: str
    price: float
    category: str
    # ... other fields
```

**Magic Numbers**: Define named constants:
```python
LOYALTY_DISCOUNT_RATES = {1: 0.03, 2: 0.08, 3: 0.12}
RUSH_HOUR_MULTIPLIER = 1.5
DEFAULT_GUEST_BALANCE = 500.0
```

**Feature Envy**: Move methods to appropriate classes or use proper data access patterns.

---

## 6. Conclusion

This project successfully demonstrates the identification and detection of common code smells through both deliberate introduction and automated detection. The detection application proves effective in identifying all six target code smells with high accuracy and provides valuable insights for code quality improvement.

The comprehensive analysis shows that code smells significantly impact software maintainability, testability, and readability. The detection system's configurable thresholds and detailed reporting provide practical tools for ongoing code quality assessment in real-world development scenarios.

Future enhancements could include machine learning-based detection, automated refactoring suggestions, and integration with continuous integration pipelines for proactive code quality management.

**Key Achievements**:
- ✅ Successfully implemented all 6 code smell detectors
- ✅ Created comprehensive test suite with 8 unit tests
- ✅ Developed configurable detection system with CLI interface
- ✅ Demonstrated detection accuracy on multiple code samples
- ✅ Provided detailed documentation and threshold justifications

The project meets all assignment requirements and provides a solid foundation for automated code quality assessment in Python development environments.

---

## References

1. Martin, R. C. (2008). Clean Code: A Handbook of Agile Software Craftsmanship
2. Fowler, M. (2018). Refactoring: Improving the Design of Existing Code
3. McCabe, T. J. (1976). A Complexity Measure. IEEE Transactions on Software Engineering
4. Li, W., & Henry, S. (1993). Object-oriented metrics that predict maintainability
5. Chidamber, S. R., & Kemerer, C. F. (1994). A metrics suite for object oriented design
