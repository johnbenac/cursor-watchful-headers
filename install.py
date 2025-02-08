import os
import shutil
import subprocess
import sys

def install():
    # Files to move
    files = ["watcher.py", "watchlist"]
    
    # Get current directory and parent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    print("Installing watcher files...")
    
    # Move files to parent directory if they don't exist
    for file in files:
        parent_path = os.path.join(parent_dir, file)
        current_path = os.path.join(current_dir, file)
        
        if os.path.exists(parent_path):
            print(f"File {file} already exists in parent directory. Skipping.")
        elif os.path.exists(current_path):
            print(f"Moving {file} to parent directory")
            shutil.copy2(current_path, parent_path)
        else:
            print(f"File {file} not found in repository directory!")

    # Install dependencies
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return

    print("\nInstallation complete! The watcher files have been copied to your project root.")
    print("You can now run the watcher from your project root using: python watcher.py")

if __name__ == "__main__":
    install() 