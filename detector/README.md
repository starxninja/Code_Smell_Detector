# Code Smell Detection Application

A comprehensive Python application for detecting code smells in Python source code. This tool implements detection for 6 common code smells and provides both command-line and configuration-based interfaces.

## Features

- **6 Code Smell Detectors:**
  - Long Method (excessive lines or complexity)
  - God Class (too many responsibilities/fields)
  - Duplicated Code (similar code blocks)
  - Large Parameter List (too many parameters)
  - Magic Numbers (hard-coded numeric literals)
  - Feature Envy (methods using external data excessively)

- **Flexible Configuration:**
  - YAML configuration file support
  - CLI argument overrides
  - Per-detector enable/disable
  - Customizable thresholds

- **Multiple Output Formats:**
  - JSON reports
  - Text reports
  - Console summaries

## Installation

1. Clone or download the detector directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```bash
# Analyze a single file
python main.py file.py

# Analyze a directory
python main.py src/

# Save report to specific file
python main.py file.py --output report.json

# Use specific format
python main.py file.py --format txt
```

### Advanced Usage

```bash
# Run only specific detectors
python main.py file.py --only LongMethod,GodClass

# Exclude specific detectors
python main.py file.py --exclude MagicNumbers

# Use custom config file
python main.py file.py --config custom_config.yaml

# Verbose output
python main.py file.py --verbose
```

### Configuration

The `config.yaml` file allows you to customize detection thresholds:

```yaml
LongMethod:
  enabled: true
  max_lines: 30
  max_complexity: 10

GodClass:
  enabled: true
  max_fields: 15
  max_methods: 20
  max_lines: 200

# ... other detectors
```

## Project Structure

```
detector/
├── detectors/           # Individual smell detectors
│   ├── __init__.py
│   ├── base_detector.py
│   ├── long_method_detector.py
│   ├── god_class_detector.py
│   ├── duplicated_code_detector.py
│   ├── large_parameter_list_detector.py
│   ├── magic_numbers_detector.py
│   └── feature_envy_detector.py
├── utils/              # Utility functions
│   ├── __init__.py
│   ├── file_utils.py
│   ├── config_utils.py
│   └── report_utils.py
├── output/             # Generated reports
│   └── report.json
├── main.py            # Main application
├── config.yaml        # Configuration file
├── requirements.txt   # Dependencies
├── test_detectors.py  # Test suite
└── sample_smelly_code.py  # Sample code for testing
```

## Detection Logic

### Long Method
- **Threshold:** 30 lines or complexity > 10
- **Logic:** Counts lines and calculates cyclomatic complexity
- **Severity:** High if > 1.5x threshold, Medium otherwise

### God Class
- **Threshold:** 15 fields, 20 methods, or 200 lines
- **Logic:** Analyzes class structure and size
- **Severity:** High if > 1.5x threshold, Medium otherwise

### Duplicated Code
- **Threshold:** 80% similarity, minimum 3 lines
- **Logic:** AST-based similarity analysis using Jaccard similarity
- **Severity:** Medium

### Large Parameter List
- **Threshold:** 5 parameters
- **Logic:** Counts function parameters
- **Severity:** High if > 2x threshold, Medium otherwise

### Magic Numbers
- **Threshold:** 3+ occurrences, values 2-1000
- **Logic:** Finds repeated numeric literals
- **Severity:** Medium

### Feature Envy
- **Threshold:** 3+ foreign accesses, 1.5x ratio
- **Logic:** Analyzes method access patterns
- **Severity:** Medium

## Testing

Run the test suite:
```bash
python test_detectors.py
```

Test on sample smelly code:
```bash
python main.py sample_smelly_code.py
```

## Examples

### Example 1: Basic Analysis
```bash
python main.py sample_smelly_code.py
```

Output:
```
Found 1 Python file(s) to analyze
Analyzing files with detectors: LongMethod, GodClass, DuplicatedCode, LargeParameterList, MagicNumbers, FeatureEnvy
Analyzing: sample_smelly_code.py
  Found 8 smells

============================================================
CODE SMELL DETECTION SUMMARY
============================================================
Files analyzed: 1
Total smells found: 8
Active detectors: LongMethod, GodClass, DuplicatedCode, LargeParameterList, MagicNumbers, FeatureEnvy

Smells by type:
  LongMethod: 3
  GodClass: 1
  LargeParameterList: 2
  MagicNumbers: 2

Severity breakdown:
  high: 3
  medium: 5
  low: 0
============================================================
```

### Example 2: Focused Analysis
```bash
python main.py sample_smelly_code.py --only LongMethod,GodClass
```

### Example 3: Custom Output
```bash
python main.py sample_smelly_code.py --output detailed_report.json --format json
```

## Requirements

- Python 3.7+
- PyYAML 6.0+

## License

This project is created for educational purposes as part of a code smell detection assignment.
