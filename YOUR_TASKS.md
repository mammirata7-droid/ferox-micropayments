# Your Tasks – What You Need To Do

Everything I could do is done. Here’s what **you** need to do next.

---

## Phase 4: Deploy Online

### Option A: Railway (simplest)

1. Go to **https://railway.app**
2. Click **“Start a New Project”** → **“Deploy from GitHub repo”**
3. Sign in with GitHub and select your repo (or push Ferox to a new repo first)
4. Railway will detect the Dockerfile and deploy
5. In the project dashboard, go to **Variables** and add:
   - `FEROX_API_SECRET` = your secret (the one in your .env)
6. Click **Generate Domain** to get a public URL like `https://ferox-xxx.railway.app`
7. Test: open `https://your-url/docs` and try POST /v1/pay

### Option B: Render

1. Go to **https://render.com**
2. Sign up, then **New** → **Web Service**
3. Connect your GitHub repo
4. Render will use the `render.yaml` in the repo
5. Add environment variables in the dashboard:
   - `FEROX_API_SECRET`
   - (Optional) `FEROX_LNBITS_*` if you set up Lightning
6. Deploy and get your URL

### Option C: Fly.io

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run: `fly auth signup` (or `fly auth login`)
3. In the ferox-micropayments folder: `fly launch`
4. Create a volume for data: `fly volumes create ferox_data`
5. Set secrets: `fly secrets set FEROX_API_SECRET=your-secret`
6. Deploy: `fly deploy`

---

## Phase 5: Real Lightning (LNbits)

### Step 1: Get an LNbits wallet

1. Go to **https://legend.lnbits.com**
2. Click **“Create wallet”**
3. Save the **Admin key** and **Invoice/Payment key** somewhere safe
4. You’ll use the **Invoice/Payment key** as `FEROX_LNBITS_API_KEY`

### Step 2: Add to your .env

Open your `.env` file and add (or update):

```
FEROX_LNBITS_ENABLED=true
FEROX_LNBITS_URL=https://legend.lnbits.com
FEROX_LNBITS_API_KEY=paste-your-invoice-payment-key-here
```

### Step 3: Restart the app

```bash
cd /home/mauricio/agents/playground/ferox-micropayments
./run.sh
```

### Step 4: Test

1. Create a payment via POST /v1/pay
2. Copy the `invoice` from the response (starts with `lnbc`)
3. Pay it from any Lightning wallet (Wallet of Satoshi, Phoenix, etc.)
4. Use POST /v1/pay/{payment_id}/confirm to mark it paid (or poll GET /v1/pay/{id})

---

## Phase 6: Share It

1. Write 2–3 sentences: what Ferox does, who it’s for
2. Post on Twitter/X, Reddit (r/lightningnetwork, r/SideProject), or Hacker News (Show HN)
3. Add a simple contact or pricing page if you want

---

## Quick Reference

| Task | Where | What |
|------|-------|------|
| Deploy | railway.app / render.com / fly.io | Sign up, connect repo, add FEROX_API_SECRET |
| Lightning | legend.lnbits.com | Create wallet, get API key, add to .env |
| Share | Twitter, Reddit, HN | Post about Ferox |
