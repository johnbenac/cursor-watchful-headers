import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
import os
import re
import sys
from threading import Lock

def build_tree(root, prefix=""):
    """Build a tree-like structure of the project directory."""
    tree_lines = []
    try:
        entries = sorted(os.listdir(root))
    except Exception:
        return ""
        
    for i, entry in enumerate(entries):
        # Skip certain directories
        if entry in ['node_modules', '.git', '__pycache__']:
            continue
            
        path = os.path.join(root, entry)
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        tree_lines.append(prefix + connector + entry)
        
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            subtree = build_tree(path, prefix + extension)
            if subtree:
                tree_lines.extend(subtree.splitlines())
                
    return "\n".join(tree_lines)

class WatcherError(Exception):
    """Base exception for watcher errors"""
    pass

class CursorRulesError(WatcherError):
    """Raised when there are issues with .cursorrules file"""
    pass

class HeaderManager:
    _lock = Lock()
    _last_update = {}
    
    # Name of this script and watchlist - to be ignored
    SCRIPT_NAME = "watcher.py"
    WATCHLIST_NAME = "watchlist"
    CURSORRULES_NAME = ".cursorrules"
    
    COMMENT_SYNTAX = {
        '.py': {'start': '# ', 'end': ''},
        '.js': {'start': '// ', 'end': ''},
        '.html': {'start': '<!-- ', 'end': ' -->'},
        '.xml': {'start': '<!-- ', 'end': ' -->'},
        '.css': {'start': '/* ', 'end': ' */'},
        '.txt': {'start': '# ', 'end': ''},
        '.md': {'start': '<!-- ', 'end': ' -->'},
        '.java': {'start': '// ', 'end': ''},
        '.cpp': {'start': '// ', 'end': ''},
        '.c': {'start': '// ', 'end': ''},
        '.sh': {'start': '# ', 'end': ''},
        '': {'start': '# ', 'end': ''},  # Default for files without extension
        '.cursorrules': {'start': '# ', 'end': ''},  # Explicit mapping for .cursorrules
    }

    @classmethod
    def get_comment_syntax(cls, file_ext):
        return cls.COMMENT_SYNTAX.get(file_ext.lower(), {'start': '# ', 'end': ''})

    @classmethod
    def create_header(cls, filepath, extra_content=None):
        """Create a header for a file, optionally with extra content.
        
        Args:
            filepath: Path to the file
            extra_content: Optional list of extra lines to include in header
        """
        # Convert to relative path from current directory
        rel_path = os.path.relpath(filepath).replace('\\', '/')
        file_ext = os.path.splitext(filepath)[1]
        comment = cls.get_comment_syntax(file_ext)
        
        header_lines = [
            f"{comment['start']}=== WATCHER HEADER START ==={comment['end']}",
            f"{comment['start']}File: {rel_path}{comment['end']}",
            f"{comment['start']}Managed by file watcher{comment['end']}"
        ]
        
        # If extra content provided, add it to header
        if extra_content:
            header_lines.extend(f"{comment['start']}{line}{comment['end']}" for line in extra_content)
            
        header_lines.extend([
            f"{comment['start']}=== WATCHER HEADER END ==={comment['end']}",
            ""  # Empty line after header
        ])
        
        return '\n'.join(header_lines)

    @classmethod
    def get_header_pattern(cls, file_ext):
        comment = cls.get_comment_syntax(file_ext)
        start = re.escape(comment['start'])
        end = re.escape(comment['end'])
        
        # Create a pattern that matches the entire header block at the start of the file
        pattern = (
            fr"^{start}=== WATCHER HEADER START ==={end}\n"
            fr"(?:{start}[^\n]*{end}\n)*"  # Match any number of comment lines
            fr"{start}=== WATCHER HEADER END ==={end}\n?"
        )
        return re.compile(pattern, re.MULTILINE)

    @classmethod
    def get_watched_files(cls):
        try:
            if not os.path.exists(cls.WATCHLIST_NAME):
                return []
            with open(cls.WATCHLIST_NAME, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
        except Exception as e:
            print(f"Error reading watchlist: {str(e)}")
            return []

    @classmethod
    def should_process_file(cls, filepath):
        # Normalize path separators for comparison
        filepath = filepath.replace('\\', '/')
        filename = os.path.basename(filepath)
        
        # Don't process the watcher script, watchlist, or cursorrules
        if filename in [cls.SCRIPT_NAME, cls.WATCHLIST_NAME, cls.CURSORRULES_NAME]:
            return False
            
        # Don't process non-existent files
        if not os.path.exists(filepath):
            return False
            
        # Check if file is in watchlist (using normalized paths)
        watched_files = [f.replace('\\', '/') for f in cls.get_watched_files()]
        if filepath not in watched_files:
            return False
            
        # Check if file extension is supported
        file_ext = os.path.splitext(filepath)[1]
        return file_ext in cls.COMMENT_SYNTAX

    @classmethod
    def update_file_header(cls, filepath):
        # Normalize path for processing
        filepath = filepath.replace('\\', '/')
        
        if not cls.should_process_file(filepath) and filepath != cls.CURSORRULES_NAME:
            return
            
        current_time = time.time()
        last_update = cls._last_update.get(filepath, 0)
        
        # Debounce: skip if updated less than 1 second ago
        if current_time - last_update < 1.0:
            return

        with cls._lock:
            try:
                # Read the entire file content
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()

                # Create new header with extra content for cursorrules
                if filepath == cls.CURSORRULES_NAME:
                    tree_str = build_tree(".")
                    extra_content = [
                        "Project Tree Structure:",
                        "",
                        *[line for line in tree_str.splitlines()],
                        ""
                    ]
                    new_header = cls.create_header(filepath, extra_content)
                else:
                    new_header = cls.create_header(filepath)

                # Get the regex pattern for the current file type
                file_ext = os.path.splitext(filepath)[1]
                header_pattern = cls.get_header_pattern(file_ext)

                # Check if there's an existing header at the start of the file
                match = header_pattern.match(content)
                if match:
                    # Replace existing header while preserving the rest of the content exactly
                    updated_content = new_header + content[match.end():]
                else:
                    # No existing header, preserve all content
                    updated_content = new_header + content

                # Ensure the file ends with exactly one newline
                updated_content = updated_content.rstrip('\n') + '\n'

                # Write back to file
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(updated_content)

                # Update last update time
                cls._last_update[filepath] = current_time
                print(f"Updated header for {filepath}")

            except Exception as e:
                print(f"Error updating header in {filepath}: {str(e)}")

    @classmethod
    def update_cursorrules(cls):
        """Update the .cursorrules file with the current project tree."""
        if not os.path.exists(cls.CURSORRULES_NAME):
            return
            
        cls.update_file_header(cls.CURSORRULES_NAME)

    @classmethod
    def verify_cursorrules(cls):
        """Verify .cursorrules exists or create it"""
        if not os.path.exists(cls.CURSORRULES_NAME):
            try:
                with open(cls.CURSORRULES_NAME, 'w', encoding='utf-8') as f:
                    f.write("# This file will be automatically updated with the project tree structure\n")
                print(f"Created {cls.CURSORRULES_NAME}")
            except Exception as e:
                raise CursorRulesError(f"Failed to create {cls.CURSORRULES_NAME}: {str(e)}")

    @classmethod
    def verify_watchlist(cls):
        """Verify watchlist exists and check for missing files"""
        if not os.path.exists(cls.WATCHLIST_NAME):
            print(f"Creating {cls.WATCHLIST_NAME} file...")
            with open(cls.WATCHLIST_NAME, 'w') as f:
                f.write("# List files to be watched (one per line)\n")
                f.write("# Lines starting with # are ignored\n")
            return

        # Check for missing files
        missing_files = []
        for filepath in cls.get_watched_files():
            if not os.path.exists(filepath):
                missing_files.append(filepath)
        
        if missing_files:
            print("\nWarning: The following files in watchlist do not exist:")
            for filepath in missing_files:
                print(f"  - {filepath}")
            print("\nThese files will be watched once they are created.\n")

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_events = {}
        self._watched_files = set(HeaderManager.get_watched_files())
        self._observer = None  # Will be set later

    def set_observer(self, observer):
        self._observer = observer

    def handle_watchlist_update(self):
        """Check for new files in watchlist and start watching them"""
        current_files = set(HeaderManager.get_watched_files())
        new_files = current_files - self._watched_files
        
        if new_files:
            print("\nNew files detected in watchlist:")
            
            # Update watched directories
            watched_dirs = set('.')
            for filepath in current_files:
                dirpath = os.path.dirname(filepath)
                while dirpath:
                    watched_dirs.add(dirpath)
                    dirpath = os.path.dirname(dirpath)
            
            # Schedule new directory watchers
            for dirpath in watched_dirs:
                if os.path.exists(dirpath):
                    self._observer.schedule(self, dirpath, recursive=True)
                    print(f"Now watching directory: {dirpath}")
            
            # Process new files
            for filepath in new_files:
                print(f"Now watching: {filepath}")
                if os.path.exists(filepath):
                    HeaderManager.update_file_header(filepath)
            
            self._watched_files = current_files
            HeaderManager.update_cursorrules()

    def handle_file_event(self, event):
        """Common handler for both modify and create events"""
        if event.is_directory:
            return

        filepath = event.src_path.replace('\\', '/')
        current_time = time.time()
        last_time = self.last_events.get(filepath, 0)

        # Debounce events for the same file
        if current_time - last_time < 0.1:  # Reduced debounce time for more sensitivity
            return

        self.last_events[filepath] = current_time
        
        # Check if this is the watchlist being modified - do this FIRST
        if os.path.basename(filepath) == HeaderManager.WATCHLIST_NAME:
            print(f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Watchlist modified, updating watchers...")
            self.handle_watchlist_update()
            return
            
        # Then check if it's a watched file
        if HeaderManager.should_process_file(filepath):
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] Detected change in {filepath}")
            HeaderManager.update_file_header(filepath)
            # After any file is modified, update the cursorrules
            HeaderManager.update_cursorrules()

    def on_modified(self, event):
        self.handle_file_event(event)
            
    def on_created(self, event):
        self.handle_file_event(event)

def start_watching():
    try:
        # Verify essential files first
        HeaderManager.verify_cursorrules()
        HeaderManager.verify_watchlist()
        
        event_handler = FileChangeHandler()
        observer = Observer()
        event_handler.set_observer(observer)
        
        # Watch both the current directory and all subdirectories that contain watched files
        watched_dirs = set()
        watched_files = HeaderManager.get_watched_files()
        
        if not watched_files:
            print(f"\nNo files listed in {HeaderManager.WATCHLIST_NAME}.")
            print("Add files to watch using the format:")
            print("  path/to/your/file.txt")
            print("\nStarting watcher anyway to detect new additions...\n")
        
        # Add current directory
        watched_dirs.add('.')
        
        # Add all parent directories of watched files
        for filepath in watched_files:
            dirpath = os.path.dirname(filepath)
            while dirpath:
                watched_dirs.add(dirpath)
                dirpath = os.path.dirname(dirpath)
        
        # Schedule watchers for all directories
        for dirpath in watched_dirs:
            if os.path.exists(dirpath):
                observer.schedule(event_handler, dirpath, recursive=True)
                print(f"Watching directory: {dirpath}")
        
        observer.start()
        print("\nFile watcher started! Monitoring for changes...")
        print("Watching for file changes in current directory and subdirectories")
        print("Supported extensions:", ", ".join(HeaderManager.COMMENT_SYNTAX.keys()))
        print(f"Note: Only watching files listed in '{HeaderManager.WATCHLIST_NAME}'")
        print(f"Note: {HeaderManager.CURSORRULES_NAME} will be automatically updated with project tree")
        
        if watched_files:
            print("\nCurrently watching:", ", ".join(watched_files))
            print("\nUpdating headers for all watched files...")
            for filepath in watched_files:
                if os.path.exists(filepath):
                    HeaderManager.update_file_header(filepath)
            print("Initial header update complete!\n")
        
        # Update cursorrules at startup
        HeaderManager.update_cursorrules()
        
        try:
            while True:
                time.sleep(0.1)  # More frequent checks
        except KeyboardInterrupt:
            observer.stop()
            print("\nFile watcher stopped!")
            observer.join()
            
    except CursorRulesError as e:
        print(f"\nError: {str(e)}")
        print("The .cursorrules file is required for operation.")
        print("Please ensure you have write permissions in this directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    start_watching() 