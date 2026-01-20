# Deployment and Development Guide

## For Plugin Developers and Contributors

### Project Structure

```
nlsq_plugin/
│
├── __init__.py                 # Plugin initialization
├── metadata.txt                # Plugin metadata for QGIS
├── nlsq_plugin.py             # Main plugin class
├── nlsq_dialog.py             # User interface dialog
├── query_processor.py         # Core NLP and spatial processing
├── advanced_processor.py      # Optional AI-powered features
├── examples.py                # Test cases and examples
│
├── resources.qrc              # Qt resources
├── icon.svg                   # Vector icon
├── icon.png                   # Raster icon (generated)
│
├── README.md                  # Main documentation
├── USER_GUIDE.md             # End-user documentation
├── REQUIREMENTS.md           # Dependencies and setup
└── DEPLOYMENT.md             # This file
```

---

## Development Setup

### Prerequisites

1. **QGIS Installation**
   - QGIS 3.x (preferably 3.22 or later)
   - Available from: https://qgis.org/download/

2. **Development Tools**
   - Python 3.6+ (comes with QGIS)
   - Text editor or IDE (PyCharm, VS Code, etc.)
   - Git for version control

3. **Optional Tools**
   - Qt Designer for UI editing
   - pytest for testing
   - Black/flake8 for code formatting

### Local Development Setup

#### 1. Clone Repository

```bash
git clone https://github.com/yourusername/nlsq-qgis-plugin.git
cd nlsq-qgis-plugin
```

#### 2. Set Up Development Environment

**Option A: Direct Installation**

```bash
# Copy to QGIS plugins directory
# Windows
xcopy /E /I nlsq_plugin "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\nlsq_plugin"

# macOS/Linux
cp -r nlsq_plugin ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

**Option B: Symbolic Link (Recommended for Development)**

```bash
# Windows (run as Administrator)
mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\nlsq_plugin" "%CD%\nlsq_plugin"

# macOS/Linux
ln -s "$(pwd)/nlsq_plugin" ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/nlsq_plugin
```

#### 3. Enable Plugin Reloader (for development)

Install the "Plugin Reloader" plugin in QGIS to reload your plugin without restarting:

1. Plugins → Manage and Install Plugins
2. Search for "Plugin Reloader"
3. Install and configure to reload NLSQ plugin

### Testing Your Changes

#### Manual Testing

1. Make changes to plugin code
2. Use Plugin Reloader to reload
3. Test in QGIS
4. Check QGIS logs: View → Panels → Log Messages

#### Automated Testing

Create test file: `tests/test_query_processor.py`

```python
import unittest
from nlsq_plugin.query_processor import QueryProcessor

class TestQueryProcessor(unittest.TestCase):
    def test_parse_simple_query(self):
        processor = QueryProcessor(None)
        result = processor.parse_query("show me all parks")
        self.assertIn('parks', result['layers'])
    
    def test_distance_extraction(self):
        processor = QueryProcessor(None)
        result = processor.parse_query("within 500 meters of schools")
        self.assertEqual(result['distance'], 500)
        self.assertEqual(result['unit'], 'meters')

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m pytest tests/
```

---

## Building for Distribution

### 1. Prepare for Release

**Update Version:**

Edit `metadata.txt`:
```ini
version=1.1.0
```

**Update Changelog:**

Create `CHANGELOG.md`:
```markdown
## [1.1.0] - 2024-01-20
### Added
- New spatial operation types
- Improved query parsing

### Fixed
- Distance unit conversion bug
- Layer name matching
```

### 2. Generate Icon (if needed)

```bash
# Convert SVG to PNG
convert icon.svg -resize 48x48 icon.png

# Or use Python
from PIL import Image
# ... conversion code
```

### 3. Compile Resources

```bash
# Compile Qt resources (if using .qrc)
pyrcc5 resources.qrc -o resources.py
```

### 4. Create Plugin Package

```bash
# Create ZIP file
cd ..
zip -r nlsq_plugin_v1.0.0.zip nlsq_plugin/ \
  -x "*.pyc" -x "*.git*" -x "*__pycache__*" \
  -x "*.vscode*" -x "*.idea*"
```

### 5. Test Package

1. Remove current installation
2. Install from ZIP in QGIS
3. Test all features
4. Check in different QGIS versions

---

## Publishing to QGIS Plugin Repository

### Prerequisites

1. Create account at: https://plugins.qgis.org/
2. Validate your email
3. Read publishing guidelines

### Submission Process

1. **Prepare Metadata**

Ensure `metadata.txt` has all required fields:
```ini
[general]
name=Natural Language Spatial Query
description=Execute spatial queries using natural language
about=Detailed description here...
version=1.0.0
qgisMinimumVersion=3.0
author=Your Name
email=your.email@example.com
homepage=https://github.com/yourusername/nlsq-qgis-plugin
tracker=https://github.com/yourusername/nlsq-qgis-plugin/issues
repository=https://github.com/yourusername/nlsq-qgis-plugin
tags=natural language, spatial query, analysis, nlp
category=Analysis
icon=icon.png
```

2. **Upload Plugin**

- Log in to plugins.qgis.org
- Click "Upload Plugin"
- Select your ZIP file
- Fill in additional information
- Submit for review

3. **Wait for Approval**

- Moderators will review (usually 1-3 days)
- May request changes
- Once approved, plugin is published

### Updates and Versions

For updates:
1. Increment version in `metadata.txt`
2. Create new ZIP package
3. Upload as new version
4. Update changelog

---

## Continuous Integration

### GitHub Actions Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest tests/ --cov=nlsq_plugin
    
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 nlsq_plugin --max-line-length=120

  package:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Create package
      run: |
        zip -r nlsq_plugin.zip nlsq_plugin/ \
          -x "*.pyc" -x "*__pycache__*"
    
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: plugin-package
        path: nlsq_plugin.zip
```

---

## Contributing Guidelines

### How to Contribute

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub
   git clone https://github.com/yourusername/nlsq-qgis-plugin.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write clear, documented code
   - Follow PEP 8 style guide
   - Add tests for new features
   - Update documentation

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add: description of changes"
   ```

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   # Create PR on GitHub
   ```

### Code Style

Follow these conventions:

```python
# Good
def process_query(self, query_text: str) -> Dict[str, Any]:
    """
    Process a natural language query.
    
    Args:
        query_text: The natural language query string
        
    Returns:
        Dictionary containing interpretation and results
    """
    # Implementation
    pass

# Avoid
def proc_q(q):
    # No docs, unclear naming
    pass
```

### Commit Messages

Use clear, descriptive commit messages:

```
Add: Support for temporal queries with relative dates
Fix: Distance unit conversion for kilometers
Update: Documentation with new examples
Refactor: Query parsing logic for better performance
```

### Adding New Features

1. **New Spatial Operation:**

```python
# In query_processor.py
self.operation_patterns['your_operation'] = r'regex_pattern'

# Implement handler
def handle_your_operation(self, interpretation):
    # Implementation
    pass
```

2. **New Layer Type:**

```python
# In query_processor.py
self.layer_synonyms['new_type'] = [
    'synonym1', 'synonym2', 'synonym3'
]
```

3. **New Filter Type:**

```python
def apply_your_filter(self, features, filter_def):
    # Filter logic
    return filtered_features
```

---

## Maintenance

### Regular Tasks

1. **Monitor Issues**
   - Respond to user reports
   - Triage and label issues
   - Fix critical bugs promptly

2. **Update Dependencies**
   - Test with new QGIS versions
   - Update compatibility notes
   - Handle API changes

3. **Documentation**
   - Keep examples current
   - Add new use cases
   - Update screenshots

### Version Support

- Maintain compatibility with QGIS LTR (Long Term Release)
- Test with latest QGIS version
- Document breaking changes

### Release Schedule

Suggested schedule:
- **Patch releases:** As needed for bug fixes
- **Minor releases:** Every 2-3 months with new features
- **Major releases:** Annually with significant changes

---

## Troubleshooting Development

### Common Issues

**Plugin Not Loading:**
```python
# Check Python console in QGIS
import sys
print(sys.path)  # Verify plugin path is included
```

**Import Errors:**
```python
# Ensure all dependencies are available
import qgis.core
import qgis.gui
# etc.
```

**UI Not Updating:**
- Use Plugin Reloader
- Check for cached .pyc files
- Restart QGIS if necessary

### Debugging

Enable debug logging:

```python
from qgis.core import QgsMessageLog, Qgis

QgsMessageLog.logMessage(
    "Debug message",
    "NLSQ Plugin",
    Qgis.Info
)
```

Use Python debugger:

```python
import pdb; pdb.set_trace()  # Breakpoint
```

---

## Resources

### QGIS Development

- **API Documentation:** https://qgis.org/pyqgis/
- **PyQGIS Cookbook:** https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/
- **Plugin Development:** https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins/index.html

### Python Spatial Libraries

- **Shapely:** Geometric operations
- **Fiona:** Vector data reading/writing
- **GeoPandas:** Spatial dataframes

### Community

- **QGIS Users Mailing List:** qgis-users@lists.osgeo.org
- **Stack Exchange:** gis.stackexchange.com (tag: qgis-plugins)
- **GitHub Discussions:** For this specific plugin

---

## License

This plugin is released under the MIT License. See LICENSE file for details.

## Credits

Developed by [Your Name/Organization]

Contributors welcome!

---

**Happy Plugin Development!** 🚀
