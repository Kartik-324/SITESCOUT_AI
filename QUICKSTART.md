# 🚀 Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.9+ installed
- [ ] OpenAI API Key
- [ ] Serper.dev API Key (free tier available)
- [ ] Google Cloud Account
- [ ] Gmail account (for SMTP, optional)

## Step-by-Step Setup

### 1️⃣ Install Python Dependencies (2 min)

```bash
cd backend
pip install -r requirements.txt
```

### 2️⃣ Get Your API Keys (3 min)

**OpenAI:**
- Visit: https://platform.openai.com/api-keys
- Create new key → Copy it

**Serper.dev:**
- Visit: https://serper.dev/
- Sign up (2,500 free searches)
- Copy API key from dashboard

### 3️⃣ Setup Google Sheets (5 min)

1. Go to https://console.cloud.google.com/
2. Create new project
3. Enable "Google Sheets API"
4. Create Service Account → Download JSON key
5. Rename to `credentials.json`, place in `backend/` folder
6. Create a Google Sheet
7. Share it with the email from credentials.json (Editor access)
8. Copy Sheet ID from URL

### 4️⃣ Configure Environment (1 min)

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
OPENAI_API_KEY=sk-your-key-here
SERPER_API_KEY=your-key-here
GOOGLE_SHEET_ID=your-sheet-id-here
```

### 5️⃣ Run the System (30 seconds)

**Start Backend:**
```bash
cd backend
python main.py
```

**Open Frontend:**
- Open `frontend/index.html` in your browser
- Or run: `cd frontend && python -m http.server 8080`

### 6️⃣ Generate Your First Leads!

1. Enter query: "best cafes in bhopal"
2. Set max results: 5
3. Click "Generate Leads"
4. Wait 30-60 seconds
5. View results!

## Common First-Time Issues

**"Module not found"**
→ Run: `pip install -r requirements.txt`

**"Google Sheets permission denied"**
→ Share your sheet with service account email

**"Invalid API key"**
→ Double-check keys in .env file

**"CORS error"**
→ Make sure backend is running on localhost:8000

## What Happens Next?

The system will:
1. ✅ Search Google (via Serper)
2. ✅ Scrape websites
3. ✅ Extract emails & data (via OpenAI)
4. ✅ Generate cold emails (via OpenAI)
5. ✅ Save to Google Sheets automatically
6. ✅ Display results in beautiful table

## Optional: Setup Email Sending

For Gmail SMTP:
1. Enable 2FA on Google Account
2. Generate App Password
3. Add to `.env`:
```env
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

## Test API Directly

```bash
curl -X POST "http://localhost:8000/generate-leads" \
  -H "Content-Type: application/json" \
  -d '{"query": "best cafes in bhopal", "max_results": 5}'
```

## Next Steps

- Check `README.md` for detailed documentation
- View `API_EXAMPLES.md` for more examples
- Customize email templates in `services/email_generator.py`
- Add more data fields in `services/extractor_service.py`

## Need Help?

1. Check backend terminal for errors
2. Visit http://localhost:8000/docs for API documentation
3. Verify all API keys are correct
4. Check Google Sheet permissions

---

**You're all set! Start generating leads! 🎉**
