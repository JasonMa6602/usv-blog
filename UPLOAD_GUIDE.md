# GitHub Blog Uploader - Usage Guide

## 🚀 Quick Start

I've created two files to help you upload your blog to GitHub:

1. **`github_uploader.py`** - Main Python script
2. **`upload_to_github.bat`** - Windows batch file for easy execution

## 📋 Prerequisites

Before using the script, make sure you have:

1. **Git installed** on your computer
2. **Python 3** installed (comes with most systems)
3. **GitHub account** with a repository created
4. **GitHub repository URL** (e.g., `https://github.com/yourusername/your-blog.git`)

## 🔧 Setup Steps

### 1. Create a GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name it (e.g., "my-blog")
4. Make it public or private
5. **Don't** initialize with README (you already have one)
6. Copy the repository URL

### 2. Configure Git Authentication
Choose one method:

**Option A: HTTPS (Personal Access Token)**
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate new token with "repo" permissions
3. When prompted for password, use the token instead

**Option B: SSH Key (Recommended)**
1. Generate SSH key: `ssh-keygen -t ed25519 -C "your-email@example.com"`
2. Add key to SSH agent
3. Add public key to GitHub Settings > SSH keys

## 🎯 How to Use

### Method 1: Double-click (Easiest)
1. Double-click `upload_to_github.bat`
2. Follow the prompts
3. Enter your GitHub repository URL when asked

### Method 2: Command Line
```bash
python github_uploader.py
```

### Method 3: Check Status Only
```bash
python github_uploader.py status
```

## 📖 What the Script Does

1. **Checks Git installation**
2. **Shows current repository status**
3. **Adds all files to Git staging**
4. **Creates a commit** with timestamp
5. **Sets up GitHub remote** (if needed)
6. **Pushes to GitHub**

## 🛠️ Commands Available

- `python github_uploader.py` - Full upload process
- `python github_uploader.py status` - Check repository status
- `python github_uploader.py help` - Show help information

## 🔍 Understanding the Output

When you run `python github_uploader.py status`, you'll see:

```
?? README.md          # ?? means untracked file
?? blog-post-1.html   # These files need to be added to Git
?? styles.css         # This is normal for new files
⚠️  No remote repositories configured  # Need to set up GitHub URL
```

## 🚀 First Time Setup Workflow

1. **Run the script**: `python github_uploader.py`
2. **Enter GitHub URL** when prompted
3. **Choose commit message** (or press Enter for default)
4. **Authenticate** with GitHub (token or SSH)
5. **Wait for upload** to complete

## 🔄 Regular Updates

For future blog updates:
1. Add/edit your blog files
2. Run `python github_uploader.py`
3. Enter a commit message (e.g., "Added new blog post")
4. Script will automatically push changes

## 🆘 Troubleshooting

### "Git is not installed"
- Download and install Git from [git-scm.com](https://git-scm.com)

### "Authentication failed"
- Use personal access token instead of password
- Check if SSH key is properly configured
- Verify repository URL is correct

### "Push failed"
- Script will try to pull latest changes first
- Check your internet connection
- Verify you have write permissions to the repository

### "No remote repositories configured"
- This is normal for first run
- Script will prompt you to enter GitHub URL

## 📞 Need Help?

The script includes built-in help:
```bash
python github_uploader.py help
```

## ✅ Success Indicators

When upload is successful, you'll see:
- ✅ Checkmarks next to each step
- "Successfully uploaded to GitHub!"
- "Your blog has been uploaded to GitHub"

## 📝 Example Workflow

```bash
# Check status first
python github_uploader.py status

# Upload to GitHub
python github_uploader.py

# Future updates
# (edit your blog files)
python github_uploader.py
# Enter commit message: "Added new blog post about Python"
```

---

**Ready to upload your blog?** Just run `python github_uploader.py` and follow the prompts!
