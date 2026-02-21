# Push Ferox to GitHub

Run these commands in your terminal. **Replace** `YOUR_GITHUB_USERNAME` and the email/name if needed.

### Step 1: Set your Git identity (one-time, if not done before)
```bash
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"
```

### Step 2: Commit and push
```bash
cd /home/mauricio/agents/playground/ferox-micropayments

# Commit (files already added)
git commit -m "Initial commit: Ferox Micropayments API"

# Add your GitHub repo (replace YOUR_GITHUB_USERNAME!)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ferox-micropayments.git

# Push
git branch -M main
git push -u origin main
```

**Example:** If your username is `mauricio123`, the remote URL would be:
```
https://github.com/mauricio123/ferox-micropayments.git
```

---

**If GitHub asks for login:** Use your GitHub username and a **Personal Access Token** (not your password). Create one at: https://github.com/settings/tokens
