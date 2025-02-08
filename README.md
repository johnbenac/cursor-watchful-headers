# File Watcher with Header Management

A Python-based file watching system that automatically manages headers in text files and maintains a project tree structure. Perfect for maintaining consistent file headers and documentation across your project.

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/johnbenac/cursor-watchful-headers.git
   cd cursor-watchful-headers
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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

1. Either clone this repository or copy these essential files to your project:
   ```
   watcher.py
   watchlist
   .cursorrules
   requirements.txt
   ```

2. If copying files, create a `watchlist` file:
   ```
   # watchlist
   # Add your project files to watch (one per line)
   src/components/header.js
   src/utils/helpers.py
   docs/api.md
   # etc...
   ```

3. Install the required dependency:
   ```bash
   pip install watchdog==3.0.0
   # or
   pip install -r requirements.txt
   ```

4. Start the watcher:
   ```bash
   python watcher.py
   ```

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

3. **Version Control**:
   - Commit `.cursorrules` and `watchlist` to track project structure
   - Include `watcher.py` in your repository
   - Use the provided `.gitignore`

## Contributing

Feel free to:
- Add support for new file types
- Improve header formatting
- Enhance tree visualization
- Add new features

## License

MIT License - Feel free to use in your own projects! 