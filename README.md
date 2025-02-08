# File Watcher with Header Management

A Python-based file watching system that automatically manages headers in text files and maintains a clean, focused project tree structure. Perfect for maintaining consistent file headers and documentation across your project.

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
   - Copy `watcher.py` and `.watchlist` to your current directory (if they don't already exist)
   - Install the required dependencies

3. Start the watcher:
   ```bash
   python watcher.py
   ```

## Configuration Files

The watcher uses three main configuration files:

1. `.watchlist`: Lists files that should receive headers and be monitored for changes
   ```
   # One file per line
   src/components/header.js
   src/utils/helpers.py
   ```

2. `.donotwatchlist`: Controls tree visualization in `.cursorrules`
   ```
   # Regex patterns to exclude from tree display
   node_modules     # Hide node_modules directory
   build/.*         # Hide build directory and contents
   .*\.pyc$        # Hide Python cache files
   ```
   Note: `.donotwatchlist` only affects what appears in the tree structure. It does not prevent files listed in `.watchlist` from receiving headers.

3. `.cursorrules`: Automatically maintained tree structure
   - Updated whenever watched files change
   - Excludes directories/files matching `.donotwatchlist` patterns
   - Provides clean, focused context for LLM coding agents
   - Labels unwatched files to help identify what should be monitored

## Tree Visualization Features

The tree structure in `.cursorrules` provides two key features:

1. **Directory Exclusion** (via `.donotwatchlist`):
   ```
   foods/
   ├── fruits/
   │   ├── apple.txt
   │   └── banana.txt
   └── vegetables/       # guilty_pleasures/ directory is hidden
       ├── carrot.txt
       └── spinach.txt
   ```

2. **Unwatched File Labeling**:
   ```
   ├── src/
   │   ├── main.py
   │   ├── utils.py  # unwatched
   │   └── config.py  # unwatched
   ```
   Files marked with "# unwatched" are visible in the tree but not receiving headers.

### How This Helps LLMs

The combination of these features helps LLMs maintain better project awareness:

1. **Clean Context**: 
   - `.donotwatchlist` hides irrelevant directories (build outputs, dependencies)
   - Keeps the tree focused on project-specific files

2. **Active Monitoring**:
   - "# unwatched" labels help LLMs identify files that should potentially be monitored
   - When an LLM sees an unwatched file being modified, it can suggest:
     ```
     "I notice utils.py is marked as unwatched. Would you like me to add it to .watchlist
     to ensure it receives proper headers and monitoring?"
     ```

3. **Intelligent Recommendations**:
   - LLMs can analyze patterns of watched vs. unwatched files
   - Suggest consistent monitoring strategies (e.g., "Other Python files in this directory are watched, should we watch this one too?")
   - Help maintain consistent header management across similar file types

This labeling system creates a self-documenting workflow where:
- The tree structure shows what exists
- `.donotwatchlist` controls what's visible
- "# unwatched" labels guide what should be monitored
- LLMs can proactively suggest improvements to file monitoring

## Example: Tree Visualization Control

Consider this project structure with some files we want to hide from the tree:

```
foods/
├── fruits/
│   ├── apple.txt
│   └── banana.txt
├── vegetables/
│   ├── carrot.txt
│   └── spinach.txt
└── guilty_pleasures/    # Directory we want to hide
    ├── chocolate.txt
    ├── cake.txt
    └── icecream.txt
```

By adding `guilty_pleasures` to `.donotwatchlist`:
```
guilty_pleasures    # Hide our guilty pleasures from the tree
```

The `.cursorrules` tree becomes cleaner:
```
# Project Tree Structure:
#
# ├── foods
# │   ├── fruits
# │   │   ├── apple.txt
# │   │   └── banana.txt
# │   └── vegetables
# │       ├── carrot.txt
# │       └── spinach.txt
```

This is particularly useful for:
- Hiding large dependency directories (node_modules, venv)
- Excluding build/output directories
- Omitting temporary or cache directories
- Maintaining focused context for LLM coding agents

## Usage

1. Configure file watching in `.watchlist`:
   ```
   # Files to receive headers and be monitored
   src/components/*.js
   src/utils/*.py
   ```

2. Configure tree visualization in `.donotwatchlist`:
   ```
   # Patterns to exclude from tree display
   node_modules
   dist
   build/.*
   tmp/.*
   ```

3. Run the watcher:
   ```bash
   python watcher.py
   ```

The watcher will:
- Add headers to files listed in `.watchlist`
- Monitor those files for changes
- Maintain a clean tree structure in `.cursorrules`, excluding patterns from `.donotwatchlist`

## File Headers

Headers are automatically added to files listed in `.watchlist`:
```
# === WATCHER HEADER START ===
# File: src/components/header.js
# Managed by file watcher
# === WATCHER HEADER END ===
```

Note: Files not listed in `.watchlist` won't receive headers, regardless of `.donotwatchlist` settings.

## Best Practices

1. `.watchlist` Management:
   - Include only files that need headers
   - Use relative paths from project root
   - Group related files together

2. `.donotwatchlist` Usage:
   - Focus on directories that clutter the tree
   - Hide build artifacts and dependencies
   - Keep patterns simple and maintainable

3. Tree Structure:
   - Keep it focused on relevant code
   - Hide implementation details
   - Maintain clean context for LLM agents

## Example Tree and File Headers

When you run the watcher, it automatically generates file headers that include the current project tree structure. For example, a portion of the generated **.cursorrules** file may look like:

```
# === WATCHER HEADER START ===
# File: .cursorrules
# Managed by file watcher
# Project Tree Structure:
#
# ├── foods
# │   ├── beverages
# │   │   ├── juice.txt
# │   │   ├── smoothie.txt
# │   │   └── tea.txt
# │   ├── dairy
# │   │   ├── cheese.txt
# │   │   ├── milk.txt
# │   │   └── yogurt.txt
# │   ├── fruits
# │   │   ├── apple.txt
# │   │   ├── banana.txt
# │   │   └── orange.txt
# │   ├── grains
# │   │   ├── bread.txt
# │   │   ├── pasta.txt
# │   │   └── rice.txt
# │   ├── snacks
# │   │   ├── chips.txt
# │   │   ├── nuts.txt
# │   │   └── popcorn.txt
# │   └── vegetables
# │       ├── broccoli.txt
# │       ├── carrot.txt
# │       └── spinach.txt
# ├── watcher.py
# └── watchlist
# === WATCHER HEADER END ===
```

Similarly, individual files receive headers. For example, the header in **foods/vegetables/carrot.txt** might be:

```
# === WATCHER HEADER START ===
# File: foods/vegetables/carrot.txt
# Managed by file watcher
# === WATCHER HEADER END ===
Crunchy orange carrot, straight from the ground! 🥕
Rich in vitamin A, making your eyesight sound!
```

### How This Helps LLMs

Long conversations or complex projects can cause the context of file paths and project structure to become obscured. By including explicit header information that shows each file's location within the overall project tree, both developers and LLM-based coding assistants are provided with clear context. This mitigates common issues such as:

- Duplicating files by forgetting existing entries
- Losing track of how individual files relate to the larger codebase
- Overlooking important structural context during long modification sessions

This way, when an LLM is assisting with code modifications, it can reference the file's placement and relationships, ensuring consistent and context-aware modifications even when conversation history becomes very lengthy.

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
   - Copy `watcher.py` and `.watchlist` to your current directory (if they don't already exist)
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
   .watchlist
   ```

2. Install the required dependency:
   ```bash
   pip install watchdog==3.0.0
   ```

3. Create or modify your `.watchlist` file:
   ```
   # Files to receive headers and be monitored
   src/components/*.js
   src/utils/*.py
   ```

4. Start the watcher:
   ```bash
   python watcher.py
   ```

**Note:** The `.cursorrules` file will be automatically created in your project root when you first run the watcher.

## Usage

1. (Optional) Remove example files:
   ```bash
   rm -rf foods  # On Windows: rmdir /s /q foods
   ```
   Then clear the watchlist file, leaving just the header:
   ```
   # List files to be watched (one per line)
   # Lines starting with # are ignored
   ```

2. Add files to watch in `.watchlist`. You can do this:
   - Manually by editing the file
   - Using your AI coding assistant (recommended):
     ```
     Ask: "Please add the following files to the watchlist..."
     or
     Ask: "Could you analyze my project and suggest files to watch?"
     ```
   
   The watchlist format is simple:
   ```
   # One file per line
   path/to/your/file.txt
   ```

3. Configure tree visualization in `.donotwatchlist`:
   ```
   # Patterns to exclude from tree display
   node_modules
   dist
   build/.*
   tmp/.*
   ```

4. Run the watcher:
   ```bash
   python watcher.py
   ```

4. The watcher will:
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