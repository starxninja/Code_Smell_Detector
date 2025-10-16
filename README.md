# Code_Smell_Detector
Code Smell Detector
A comprehensive static analysis tool for detecting code smells in Python source code. This application helps identify common anti-patterns and maintainability issues through both a web interface and command-line interface.
Features

🔍 6 Code Smell Detectors:

Long Method
God Class
Large Parameter List
Magic Numbers
Duplicated Code
Feature Envy


🎯 Dual Interface: Web-based GUI and command-line tool
⚙️ Configurable Thresholds: Customize detection sensitivity
📊 Detailed Reports: Line-by-line analysis with severity levels
🚀 Fast Analysis: AST-based processing for quick results

Installation
Prerequisites

Python 3.7 or higher
Required packages: Flask, PyYAML

Setup

Clone or download the project files.
Ensure all required files are in the same directory:

FlaskIntegrated.py (Web server)
CodeSmellDetector.py (Core detection engine)
main.py (CLI interface)
code_smell_detector_frontend.html (Web interface)
config.yaml (Configuration file)


Install dependencies:
text# Install required dependencies
pip install pyyaml flask

# Or use requirements.txt if provided
pip install -r requirements.txt


Project Structure
textcode-smell-detector/
│
├── FlaskIntegrated.py     # Web server (Flask-based)
├── CodeSmellDetector.py   # Core detection engine
├── main.py                # CLI interface
├── code_smell_detector_frontend.html  # Web interface HTML
├── config.yaml            # Configuration file
├── smelly_code.py         # Sample code with intentional smells
├── test_smelly_code.py    # Unit tests
├── docs/
│   └── smells.md          # Documentation of intentional smells
├── requirements.txt       # Python dependencies
└── README.md              # This file
Usage
Web Interface (Recommended)

Start the web server:
textpython FlaskIntegrated.py

Access the application: Open your browser and navigate to http://127.0.0.1:5000.
The server automatically finds an available port between 5000-5020.
Using the web interface:

Upload a Python file (.py)
Configure detection settings using toggle switches
Click "Analyze Code" to run the analysis
View results with detailed explanations and code snippets



Command Line Interface
Basic Usage
text# Run all enabled smells from default config
python main.py SmellyCode.py
Advanced Options
text# Run only specific smells
python main.py --only LongMethod,GodClass SmellyCode.py

# Run all except specific smells  
python main.py --exclude MagicNumbers SmellyCode.py

# Use custom config file
python main.py --config my_config.yaml SmellyCode.py

# Save report to file
python main.py --output report.txt SmellyCode.py

# Verbose output
python main.py --verbose SmellyCode.py
Command Line Options

































OptionDescription<file>Path to Python file to analyze (required)--configPath to config file (default: config.yaml)--onlyComma-separated list of smells to check (overrides config)--excludeComma-separated list of smells to exclude (overrides config)--output, -oOutput file for report (default: stdout)--verbose, -vVerbose output
Configuration
Default Thresholds
yamlsmells:
  LongMethod:
    enabled: true
    threshold: 40      # Maximum lines per method
    
  GodClass:
    enabled: true
    method_threshold: 5    # Maximum methods
    loc_threshold: 100     # Maximum lines of code
    field_threshold: 3     # Maximum fields
    
  LargeParameterList:
    enabled: true
    threshold: 5       # Maximum parameters
    
  MagicNumbers:
    enabled: true
    threshold: 3       # Minimum occurrences
    ignore: [0, 1, -1, 2]  # Common numbers to ignore
    
  DuplicatedCode:
    enabled: true
    min_lines: 3       # Minimum lines for duplication
    similarity: 0.6    # Similarity threshold (0.0-1.0)
    
  FeatureEnvy:
    enabled: true
    threshold: 3       # Minimum foreign object accesses
Custom Configuration
Create a config.yaml file to customize detection thresholds. The application will merge custom settings with defaults.
Detected Code Smells

Long Method
Description: Methods that are too long and difficult to maintain
Detection: Methods exceeding configured line threshold (excluding comments/blanks)
Default Threshold: 40 lines
God Class
Description: Classes with too many responsibilities
Detection: Classes violating multiple size thresholds (methods, LOC, fields)
Default Threshold: 5 methods, 100 LOC, 3 fields
Large Parameter List
Description: Functions with too many parameters
Detection: Functions with parameters exceeding threshold (excluding self/cls)
Default Threshold: 5 parameters
Magic Numbers
Description: Unexplained numeric literals in code
Detection: Numbers appearing multiple times (excluding common values)
Default Threshold: 3 occurrences
Duplicated Code
Description: Similar code blocks repeated throughout the codebase
Detection: Code blocks with high similarity score
Default Threshold: 3+ lines, 0.6 similarity
Feature Envy
Description: Methods that access other objects' data excessively
Detection: Methods making multiple accesses to foreign objects
Default Threshold: 3 accesses to same foreign object

Output Examples
Web Interface Output

Color-coded severity levels (High, Medium, Low)
Code snippets showing detected issues
Line numbers and specific locations
Refactoring suggestions

Command Line Output
text=== CODE SMELL DETECTION REPORT ===
Active Smells: LongMethod, GodClass, LargeParameterList
Total Issues: 5

LONG METHOD (2 issue(s))
---
Lines 60-125: Method 'process_loan' is too long (65 lines, threshold: 40)

GOD CLASS (1 issue(s))
---
Lines 12-140: Class 'LibraryManager' is a God Class: 5 methods, 4 fields, 128 LOC
Troubleshooting
Common Issues

"Module not found" errors:

Ensure all Python files are in the same directory
Check Python version (requires 3.7+)


Port already in use:

The Flask server automatically finds available ports 5000-5020
Manually specify port: python FlaskIntegrated.py --port 5001


Analysis errors:

Check Python file syntax
Ensure file encoding is UTF-8



Debug Mode
For detailed error information, run the Flask server with debug mode enabled (modify FlaskIntegrated.py).
Technical Details

Analysis Method: Abstract Syntax Tree (AST) parsing
Processing: Static analysis without code execution
Performance: Optimized for files up to 1000+ lines
Output: Comprehensive reports with actionable insights

Limitations

Currently supports Python only
AST-based analysis (requires valid Python syntax)
Some complex patterns may not be detected
Thresholds may need adjustment for different codebases

License
© 2024 Code Smell Detector. All rights reserved.
This software is proprietary and confidential. No part of this application may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the owner.
The owner retains all intellectual property rights, including but not limited to copyrights, patents, and trademarks in the software and documentation. Any unauthorized use, reproduction, or distribution is strictly prohibited.
For licensing inquiries, please contact the owner.
