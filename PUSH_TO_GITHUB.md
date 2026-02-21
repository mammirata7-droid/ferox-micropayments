# Push Ferox to GitHub

Run these commands in your terminal. **Replace `YOUR_GITHUB_USERNAME`** with your actual GitHub username.

```bash
cd /home/mauricio/agents/playground/ferox-micropayments

# Initialize git (only Ferox folder)
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: Ferox Micropayments API"

# Add your GitHub repo as remote (replace YOUR_GITHUB_USERNAME!)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ferox-micropayments.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Example:** If your username is `mauricio123`, the remote URL would be:
```
https://github.com/mauricio123/ferox-micropayments.git
```

---

**If GitHub asks for login:** Use your GitHub username and a **Personal Access Token** (not your password). Create one at: https://github.com/settings/tokens
