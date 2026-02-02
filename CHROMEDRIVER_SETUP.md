# ChromeDriver Path Configuration Guide

This guide explains how to use a custom ChromeDriver path with the exhibition scraper.

## Quick Answer

If you have ChromeDriver in the same folder as `exhibition_scraper.py`:

1. Open `exhibition_scraper.py`
2. Find line 70 (CONFIG section)
3. Change from: `CHROMEDRIVER_PATH = None`
4. Change to: `CHROMEDRIVER_PATH = "./chromedriver"` (Linux/Mac) or `"./chromedriver.exe"` (Windows)
5. Save and run the script

## Detailed Instructions

### Step 1: Download ChromeDriver

If you haven't already downloaded ChromeDriver:

1. Visit: https://chromedriver.chromium.org/downloads
2. Download the version matching your Chrome browser version
3. Extract the executable file (chromedriver or chromedriver.exe)

To check your Chrome version:
- Open Chrome
- Go to `chrome://version`
- Note the version number (e.g., 120.0.6099.109)

### Step 2: Place ChromeDriver

Choose one of these options:

**Option A: Same folder as the script (Recommended)**
```
automation-python/
├── exhibition_scraper.py
├── chromedriver              # Linux/Mac
└── chromedriver.exe          # Windows
```

**Option B: Specific location on your system**
- Place it anywhere (e.g., C:/tools/, /usr/local/bin/)
- Note the full path for configuration

### Step 3: Configure the Path

Open `exhibition_scraper.py` and locate the CONFIG section (around line 67-70).

#### For ChromeDriver in Same Folder:

**Windows:**
```python
CHROMEDRIVER_PATH = "./chromedriver.exe"
```

**Linux/Mac:**
```python
CHROMEDRIVER_PATH = "./chromedriver"
```

#### For ChromeDriver in Specific Location:

**Windows Examples:**
```python
CHROMEDRIVER_PATH = "C:/tools/chromedriver.exe"
CHROMEDRIVER_PATH = "D:/selenium/drivers/chromedriver.exe"
```

**Linux/Mac Examples:**
```python
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
CHROMEDRIVER_PATH = "/home/username/drivers/chromedriver"
```

### Step 4: Set Permissions (Linux/Mac Only)

Make the ChromeDriver executable:

```bash
chmod +x ./chromedriver
```

Or for specific location:
```bash
chmod +x /usr/local/bin/chromedriver
```

### Step 5: Run the Script

```bash
python exhibition_scraper.py
```

Check the console output or `scraper.log` for this message:
```
Using custom ChromeDriver from: ./chromedriver
```

## How It Works

The script uses this priority order:

1. **Custom Path** - If `CHROMEDRIVER_PATH` is set and the file exists
2. **Webdriver-Manager** - If path is None or file doesn't exist (automatic download)
3. **System Driver** - If both above methods fail (uses PATH environment variable)

This means:
- Setting `CHROMEDRIVER_PATH = None` uses automatic webdriver-manager (default)
- If your path is incorrect, it automatically falls back to webdriver-manager
- The script won't break even if the path is wrong

## Verification

To verify your ChromeDriver setup:

### Check File Exists:
**Windows:**
```cmd
dir chromedriver.exe
```

**Linux/Mac:**
```bash
ls -la chromedriver
```

### Check Version:
**Windows:**
```cmd
chromedriver.exe --version
```

**Linux/Mac:**
```bash
./chromedriver --version
```

The version should match your Chrome browser version.

## Troubleshooting

### Problem: "Permission denied" (Linux/Mac)
**Solution:** 
```bash
chmod +x ./chromedriver
```

### Problem: "File not found"
**Solutions:**
1. Verify the file exists at the specified path
2. Use absolute path instead of relative path
3. Check filename matches exactly (case-sensitive on Linux/Mac)
4. Verify no typos in the path

### Problem: ChromeDriver version mismatch
**Solution:**
1. Check Chrome version: `chrome://version`
2. Download matching ChromeDriver version
3. Replace the old chromedriver with the new one

### Problem: Script still downloads ChromeDriver
**This means your custom path isn't working. Check:**
1. Is `CHROMEDRIVER_PATH` set to a value (not `None`)?
2. Does the file exist at that path?
3. Is the path correctly formatted?

**Test in Python:**
```python
import os
CHROMEDRIVER_PATH = "./chromedriver"  # Your path
print(f"Path exists: {os.path.exists(CHROMEDRIVER_PATH)}")
```

### Problem: Windows path issues
**Solution:**
Use forward slashes or escaped backslashes:
```python
# Good:
CHROMEDRIVER_PATH = "C:/tools/chromedriver.exe"
CHROMEDRIVER_PATH = "C:\\tools\\chromedriver.exe"

# Bad:
CHROMEDRIVER_PATH = "C:\tools\chromedriver.exe"  # Wrong!
```

## Examples

### Example 1: Same Folder (Windows)
```
Project:
  automation-python/
  ├── exhibition_scraper.py
  ├── chromedriver.exe
  └── requirements.txt

Configuration:
  CHROMEDRIVER_PATH = "./chromedriver.exe"
```

### Example 2: Same Folder (Linux)
```
Project:
  automation-python/
  ├── exhibition_scraper.py
  ├── chromedriver
  └── requirements.txt

Setup:
  chmod +x ./chromedriver

Configuration:
  CHROMEDRIVER_PATH = "./chromedriver"
```

### Example 3: System-Wide Installation (Linux)
```
Installation:
  sudo mv chromedriver /usr/local/bin/
  sudo chmod +x /usr/local/bin/chromedriver

Configuration:
  CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
```

## Reverting to Automatic Mode

To go back to using webdriver-manager (automatic download):

Simply set:
```python
CHROMEDRIVER_PATH = None
```

The script will automatically download and manage ChromeDriver for you.

## Benefits of Custom Path

- **No internet required** for ChromeDriver download
- **Faster startup** - no download time
- **Version control** - use specific ChromeDriver version
- **Offline environments** - works without internet access
- **Corporate networks** - bypass download restrictions

## Benefits of Webdriver-Manager (Default)

- **No manual setup** - downloads automatically
- **Always updated** - gets latest compatible version
- **No maintenance** - handles updates automatically
- **Cross-platform** - works same on all operating systems

## Summary

The script now supports both methods:
1. **Custom path** - for users who want control
2. **Automatic** - for users who want convenience

Choose the method that works best for your situation!
