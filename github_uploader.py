#!/usr/bin/env python3
"""
GitHub Blog Uploader Script
Automatically uploads blog files to GitHub repository
Usage: python github_uploader.py
"""

import os
import subprocess
import sys
from datetime import datetime

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr.strip() if e.stderr else str(e)}")
        return False

def check_git_installed():
    """Check if git is installed"""
    return run_command("git --version", "Checking Git installation")

def get_repo_info():
    """Get current repository information"""
    print("\n📋 Current Repository Status:")
    run_command("git status --porcelain", "Checking repository status")
    
    # Check if remote exists
    result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("🌐 Remote repositories:")
        print(result.stdout)
        return True
    else:
        print("⚠️  No remote repositories configured")
        return False

def setup_remote():
    """Setup GitHub remote repository"""
    print("\n🔧 Setting up GitHub remote repository...")
    
    repo_url = input("Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): ").strip()
    
    if not repo_url:
        print("❌ Repository URL cannot be empty")
        return False
    
    # Add remote
    if run_command(f"git remote add origin {repo_url}", "Adding remote origin"):
        print(f"✅ Remote repository added: {repo_url}")
        return True
    return False

def commit_and_push():
    """Add files, commit, and push to GitHub"""
    print("\n📤 Preparing to upload files...")
    
    # Add all files
    if not run_command("git add .", "Adding all files to staging"):
        return False
    
    # Get commit message
    default_msg = f"Blog update - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    try:
        commit_msg = input(f"Enter commit message (or press Enter for default: '{default_msg}'): ").strip()
        if not commit_msg:
            commit_msg = default_msg
    except (KeyboardInterrupt, EOFError):
        print("\n\n❌ Operation cancelled by user")
        return False
    
    # Commit changes
    if not run_command(f'git commit -m "{commit_msg}"', "Committing changes"):
        return False
    
    # Check if this is the first commit
    result = subprocess.run("git rev-parse --verify HEAD", shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("🌟 First commit detected!")
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    
    # Check if remote exists, if not setup first
    remote_exists = get_repo_info()
    if not remote_exists:
        if not setup_remote():
            return False
    
    # Try to push
    push_cmd = "git push -u origin main" if not remote_exists else "git push origin main"
    if run_command(push_cmd, "Pushing to remote repository"):
        print("✅ Successfully uploaded to GitHub!")
        return True
    else:
        # If push fails, might need to pull first
        print("\n⚠️  Push failed. Attempting to pull latest changes...")
        if run_command("git pull origin main", "Pulling latest changes"):
            return run_command("git push origin main", "Retrying push")
        return False

def show_help():
    """Show help information"""
    print("""
🆘 GitHub Blog Uploader Help

This script automates the process of uploading your blog to GitHub.

Prerequisites:
- Git must be installed on your system
- You must have a GitHub account
- You need to have SSH key configured or use HTTPS with credentials

Usage:
1. Run: python github_uploader.py
2. Follow the prompts
3. For first-time setup, you'll need to provide your GitHub repository URL

Features:
- ✅ Automatically adds all files
- ✅ Creates meaningful commit messages
- ✅ Handles first-time setup
- ✅ Provides clear error messages
- ✅ Supports both new and existing repositories

Troubleshooting:
- If authentication fails, ensure your GitHub credentials are configured
- For SSH: Make sure your SSH key is added to GitHub
- For HTTPS: Use personal access token instead of password
- Check your internet connection
""")

def main():
    """Main function"""
    print("🚀 GitHub Blog Uploader")
    print("=" * 30)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            show_help()
            return
        elif sys.argv[1] == 'status':
            get_repo_info()
            return
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first.")
        return
    
    print("\n📁 Repository: blog")
    print(f"📍 Location: {os.getcwd()}")
    
    # Show current status
    get_repo_info()
    
    # Ask for confirmation
    print("\n🤔 This will:")
    print("  1. Add all files to Git")
    print("  2. Create a commit")
    print("  3. Push to GitHub")
    
    try:
        response = input("\nDo you want to continue? (y/n): ").lower().strip()
        
        if response != 'y':
            print("❌ Operation cancelled")
            return
    except (KeyboardInterrupt, EOFError):
        print("\n\n❌ Operation cancelled by user")
        return
    
    # Execute the upload process
    if commit_and_push():
        print("\n🎉 Success! Your blog has been uploaded to GitHub.")
        print("📝 You can run this script again anytime to update your blog.")
    else:
        print("\n❌ Upload failed. Please check the error messages above.")
        print("💡 You can run 'python github_uploader.py help' for troubleshooting tips.")

if __name__ == "__main__":
    main()
