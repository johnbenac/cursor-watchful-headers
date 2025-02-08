# File Watcher with Header Management

A Python-based file watching system that automatically manages headers in text files and maintains a project tree structure. Perfect for maintaining consistent file headers and documentation across your project.

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/johnbenac/cursor-watchful-headers.git
   ```

2. Run the installation script:
   ```bash
   python cursor-watchful-headers/install.py
   ```
   This will:
   - Copy `watcher.py` and `watchlist` to your current directory (if they don't already exist)
   - Install the required dependencies

3. Start the watcher:
   ```bash
   python watcher.py
   ```

## Features

- Automatically adds and updates headers in watched files
- Maintains a live project tree structure in `.cursorrules`
- Supports multiple file types with appropriate comment syntax
- Dynamic watching of new files and directories
- Debounced file updates to prevent excessive writes
- Thread-safe header management

## Example Data

This repository includes example food-themed content to demonstrate the watcher's functionality. When integrating into your own project:

1. You can safely remove the `foods/` directory and its contents
2. The example structure shows how the watcher handles:
   - Multiple directory levels
   - Different file types
   - Various comment syntaxes
   - Real-time updates

## Using in Your Project

### Option 1: Installing via Script (Recommended)

If you want to add the watcher to an existing project:

1. From your project root, clone and install:
   ```bash
   git clone https://github.com/johnbenac/cursor-watchful-headers.git
   python cursor-watchful-headers/install.py
   ```

2. The script will:
   - Copy `watcher.py` and `watchlist` to your current directory (if they don't already exist)
   - Install the required `watchdog` package
   - Leave your existing `requirements.txt` untouched
   - Leave your existing `.cursorrules` untouched (at least until you run watcher.py)

3. You can now delete the cloned directory if desired (the copied files in your current directory will remain):
   ```bash
   rm -rf cursor-watchful-headers  # On Windows: rmdir /s /q cursor-watchful-headers
   ```

### Option 2: Manual Installation

If you prefer to set things up manually:

1. Copy these essential files to your project root:
   ```
   watcher.py
   watchlist
   ```

2. Install the required dependency:
   ```bash
   pip install watchdog==3.0.0
   ```

3. Create or modify your `watchlist` file:
   ```
   # watchlist
   # Add your project files to watch (one per line)
   src/components/header.js
   src/utils/helpers.py
   docs/api.md
   # etc...
   ```

4. Start the watcher:
   ```bash
   python watcher.py
   ```

**Note:** The `.cursorrules` file will be automatically created in your project root when you first run the watcher.

## Usage

1. Add files to watch in `watchlist`:
   ```
   # One file per line
   path/to/your/file.txt
   ```

2. Run the watcher:
   ```bash
   python watcher.py
   ```

3. The watcher will:
   - Add headers to all watched files
   - Update `.cursorrules` with the project tree
   - Monitor for changes in real-time
   - Automatically watch new files added to the watchlist

## File Headers

Headers are automatically added to watched files in the appropriate comment syntax:
```
# === WATCHER HEADER START ===
# File: path/to/file.txt
# Managed by file watcher
# === WATCHER HEADER END ===
```

## Supported File Types

- Python (.py)
- JavaScript (.js)
- HTML (.html)
- XML (.xml)
- CSS (.css)
- Text (.txt)
- Markdown (.md)
- Java (.java)
- C++ (.cpp)
- C (.c)
- Shell scripts (.sh)

## Configuration

### Adding New File Types

Edit `COMMENT_SYNTAX` in `watcher.py` to add support for more file types:
```python
COMMENT_SYNTAX = {
    '.py': {'start': '# ', 'end': ''},
    '.js': {'start': '// ', 'end': ''},
    # Add your custom file types:
    '.xyz': {'start': '/* ', 'end': ' */'},
}
```

### Performance Tuning

- Modify `time.sleep(0.1)` in the main loop to adjust check frequency
- Adjust debounce time (default 1.0s) in `update_file_header`
- The `.cursorrules` file is automatically maintained with the project structure

## Best Practices

1. **Initial Setup**:
   - Start with a small set of files in your watchlist
   - Verify header format meets your needs
   - Add more files progressively

2. **Directory Structure**:
   - Keep watched files within your project root
   - Use relative paths in watchlist
   - Group related files in directories


## Contributing

Feel free to:
- Add support for new file types
- Improve header formatting
- Enhance tree visualization
- Add new features

## License

MIT License - Feel free to use in your own projects! 