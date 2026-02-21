# Deploy Ferox on Render (Free Tier)

Step-by-step guide.

---

## Step 1: Sign up

1. Go to **https://render.com**
2. Click **Get Started**
3. Sign up with **GitHub** (easiest – it will connect your repos)

---

## Step 2: Create a Web Service

1. Click **New +** → **Web Service**
2. Connect GitHub if asked, and find **mammirata7-droid/ferox-micropayments**
3. Click **Connect** next to it

---

## Step 3: Configure the service

| Field | What to enter |
|-------|----------------|
| **Name** | `ferox-micropayments` (or leave default) |
| **Region** | Choose closest to you |
| **Runtime** | **Docker** |
| **Instance Type** | **Free** (if available) or **Starter** ($7/mo) |

---

## Step 4: Add environment variable

1. Click **Advanced**
2. Under **Environment Variables**, click **Add Environment Variable**
3. **Key:** `FEROX_API_SECRET`
4. **Value:** your secret (the one from your `.env` file – e.g. `ProCordisFortisEtAnimaeFerocitateVictoriaEst1927` or whatever you set)

---

## Step 5: Deploy

1. Click **Create Web Service**
2. Render will build and deploy (takes 2–5 minutes)
3. When it’s done, you’ll see a URL like `https://ferox-micropayments-xxxx.onrender.com`

---

## Step 6: Test

1. Open `https://your-url.onrender.com/docs`
2. Try **POST /v1/pay** with your API key
3. If it works, Ferox is live

---

## Note about Free Tier

- Free web services **spin down** after ~15 minutes of no traffic
- First request after spin-down can take 30–60 seconds to wake up
- For always-on, use **Starter** ($7/month)
