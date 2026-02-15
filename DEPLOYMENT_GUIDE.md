# 🚀 Complete Deployment & Usage Guide

## 📦 What's Included

This package contains a **complete, production-ready** AI Lead Generation system with:

- ✅ Backend API (Python/FastAPI)
- ✅ Frontend UI (HTML/CSS/JavaScript)
- ✅ Full documentation
- ✅ Setup scripts (Linux/Mac/Windows)
- ✅ Example configurations
- ✅ API request examples

## 🎯 System Capabilities

### What It Does
1. **Searches Google** for businesses based on your query
2. **Scrapes websites** to collect information
3. **Extracts data** using AI (emails, ratings, hours, etc.)
4. **Generates personalized cold emails** for each business
5. **Saves automatically to Google Sheets**
6. **Optionally sends emails** via SMTP

### Example Use Cases
- Find and contact local cafes
- Generate leads for restaurants
- Discover gyms in your area
- Contact salons for partnerships
- Find retail stores for B2B sales
- Any business-to-business outreach

## ⚡ Quick Setup (3 Methods)

### Method 1: Automated Setup (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Method 2: Manual Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your keys
python main.py
```

### Method 3: Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 🔑 API Keys Setup

### 1. OpenAI API Key

**Cost:** ~$0.01-0.05 per 10 leads

**Steps:**
1. Go to https://platform.openai.com/
2. Create account or sign in
3. Navigate to API Keys
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add to `.env` as `OPENAI_API_KEY`

**Pricing:**
- GPT-4o-mini: ~$0.15 per 1M input tokens
- GPT-4o-mini: ~$0.60 per 1M output tokens
- Typical cost: $0.001-0.005 per lead

### 2. Serper.dev API Key

**Cost:** FREE (2,500 searches/month)

**Steps:**
1. Go to https://serper.dev/
2. Sign up with Google
3. Free tier includes 2,500 searches
4. Copy API key from dashboard
5. Add to `.env` as `SERPER_API_KEY`

**Limits:**
- Free: 2,500 searches/month
- Paid plans available for higher volume

### 3. Google Sheets API

**Cost:** FREE

**Complete Setup:**

#### A. Create Google Cloud Project
1. Visit https://console.cloud.google.com/
2. Click "Select a project" → "New Project"
3. Name: "Lead Generation System"
4. Click "Create"

#### B. Enable Google Sheets API
1. In your project, go to "APIs & Services" → "Library"
2. Search: "Google Sheets API"
3. Click on it → Click "Enable"

#### C. Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name: "lead-gen-service"
4. Description: "Service account for lead generation"
5. Click "Create and Continue"
6. Skip optional steps → Click "Done"

#### D. Generate JSON Key
1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create"
6. File downloads automatically
7. Rename to `credentials.json`
8. Move to `backend/` directory

#### E. Create Google Sheet
1. Go to https://sheets.google.com/
2. Create new blank spreadsheet
3. Name it: "Lead Generation Data"
4. Copy the Sheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/COPY_THIS_PART/edit
   ```
5. Open `credentials.json`
6. Find `client_email` value (looks like: name@project.iam.gserviceaccount.com)
7. In your Google Sheet, click "Share"
8. Paste the service account email
9. Give "Editor" access
10. Click "Send" (ignore warning about email)

#### F. Add to .env
```env
GOOGLE_SHEET_ID=your_copied_sheet_id_here
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json
```

### 4. SMTP Setup (Optional)

**For Gmail:**

#### A. Enable 2-Factor Authentication
1. Go to https://myaccount.google.com/
2. Security → 2-Step Verification
3. Turn it ON if not already

#### B. Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and your device
3. Click "Generate"
4. Copy the 16-character password
5. Use this password in `.env` (NOT your regular Gmail password)

#### C. Add to .env
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
SMTP_FROM_EMAIL=your-email@gmail.com
SMTP_FROM_NAME=Your Name
```

## 📝 .env Configuration

Complete `.env` file example:

```env
# Required
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
SERPER_API_KEY=xxxxxxxxxxxxx
GOOGLE_SHEET_ID=1xxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials.json

# Optional (for email sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=yourname@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
SMTP_FROM_EMAIL=yourname@gmail.com
SMTP_FROM_NAME=Your Name

# Server (defaults are fine)
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🎮 Usage Guide

### Starting the System

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend (Optional):**
```bash
cd frontend
python -m http.server 8080
```

Or simply open `frontend/index.html` in your browser.

### Using the Web Interface

1. **Open Frontend**
   - Navigate to `http://localhost:8080`
   - Or open `frontend/index.html` directly

2. **Enter Query**
   - Example: "best cafes in bhopal"
   - Example: "top restaurants in mumbai"
   - Example: "gyms in delhi"

3. **Set Max Results**
   - Minimum: 1
   - Maximum: 50
   - Recommended: 10 for testing

4. **Click Generate Leads**
   - Wait 30-120 seconds
   - Progress indicator will show

5. **View Results**
   - Table displays all leads
   - Click "View Email" to see cold email
   - Data automatically saved to Google Sheets

6. **Optional Actions**
   - "Send Cold Emails" - Bulk email via SMTP
   - "Download JSON" - Save to local file

### Using the API Directly

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Generate Leads:**
```bash
curl -X POST http://localhost:8000/generate-leads \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best cafes in bhopal",
    "max_results": 5
  }'
```

**Send Emails:**
```bash
curl -X POST http://localhost:8000/send-emails \
  -H "Content-Type: application/json" \
  -d '{
    "leads": [...],
    "subject": "Partnership Opportunity"
  }'
```

**API Documentation:**
Visit: `http://localhost:8000/docs`

## 📊 Expected Output

### Google Sheets Columns
```
| Name | Owner | Rating | Website | Email | Opening Hours | Website Exists | Cold Email |
```

### Sample Data
```
Name: Cafe Coffee Day
Owner: John Smith
Rating: 4.5
Website: https://example.com
Email: contact@example.com
Opening Hours: 8 AM - 10 PM
Website Exists: TRUE
Cold Email: Hi, I came across Cafe Coffee Day...
```

## 🐛 Troubleshooting

### Common Issues & Solutions

#### "Module not found"
**Problem:** Missing dependencies
**Solution:**
```bash
pip install -r requirements.txt
```

#### "Permission denied" (Google Sheets)
**Problem:** Service account doesn't have access
**Solution:**
1. Open `credentials.json`
2. Copy `client_email`
3. Share Google Sheet with this email (Editor access)

#### "Invalid API key" (OpenAI)
**Problem:** Wrong or expired key
**Solution:**
1. Check `.env` file
2. Verify key starts with `sk-`
3. Generate new key if needed

#### "CORS error"
**Problem:** Backend not running or wrong port
**Solution:**
1. Ensure backend is on `http://localhost:8000`
2. Check browser console for exact error
3. Restart backend server

#### "No results found"
**Problem:** Search query too specific or network issue
**Solution:**
1. Try broader search terms
2. Check Serper API quota
3. Verify internet connection

#### "SMTP authentication failed"
**Problem:** Wrong password or 2FA not enabled
**Solution:**
1. Use App Password (not regular password)
2. Enable 2FA on Google account
3. Regenerate App Password

## 📈 Performance Tips

### Optimize for Speed
- Start with 5-10 results for testing
- Increase to 20-30 for production
- Max 50 to avoid rate limits

### Cost Optimization
- Use smaller result sets for testing
- Free tier: Serper (2,500/month)
- OpenAI costs ~$0.01-0.05 per 10 leads

### Best Practices
- Clear Google Sheet before large runs
- Monitor API quota usage
- Save JSON backups
- Test email templates before bulk sending

## 🔒 Security Best Practices

### Do's
✅ Use `.gitignore` (already configured)
✅ Keep `.env` file private
✅ Use environment variables
✅ Rotate API keys regularly
✅ Use HTTPS in production
✅ Enable 2FA on all accounts

### Don'ts
❌ Don't commit `.env` to git
❌ Don't commit `credentials.json`
❌ Don't share API keys
❌ Don't hardcode secrets
❌ Don't skip input validation

## 🚀 Production Deployment

### Deploy to Cloud

**Heroku:**
```bash
# Add Procfile
echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile

# Deploy
heroku create my-lead-gen
git push heroku main
heroku config:set OPENAI_API_KEY=xxx
```

**AWS/DigitalOcean:**
- Use Docker
- Set environment variables
- Configure HTTPS
- Set up monitoring

**VPS Setup:**
```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip

# Clone project
git clone [your-repo]
cd lead-gen-system/backend

# Setup
pip install -r requirements.txt
python main.py
```

### Environment Variables in Cloud
- Use platform's secret management
- Never commit `.env` to repository
- Use separate keys for prod/dev

## 📚 Additional Resources

### Documentation
- `README.md` - Complete documentation
- `QUICKSTART.md` - 5-minute setup
- `API_EXAMPLES.md` - API usage examples
- `PROJECT_SUMMARY.md` - Technical overview

### API Documentation
- FastAPI Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### External Links
- OpenAI Docs: https://platform.openai.com/docs
- Serper Docs: https://serper.dev/docs
- Google Sheets API: https://developers.google.com/sheets/api
- FastAPI Docs: https://fastapi.tiangolo.com/

## 💡 Customization Guide

### Modify Email Templates
Edit `backend/services/email_generator.py`:
```python
prompt = f"""
Your custom email template here
Business: {business_name}
...
"""
```

### Add Data Fields
Edit `backend/services/extractor_service.py`:
```python
# Add to extraction prompt
"your_field": "description",
```

### Change UI Styling
Edit `frontend/style.css`:
```css
/* Your custom styles */
```

### Adjust Timeouts
Edit `backend/services/scraper_service.py`:
```python
timeout=30.0  # Increase for slow sites
```

## 🎓 Learning Resources

### Understanding the Code
1. Start with `main.py` - API endpoints
2. Review `services/` - Business logic
3. Check `config/` - Configuration
4. Frontend: `script.js` - API calls

### Key Concepts
- **Async/Await:** Non-blocking operations
- **Pydantic:** Data validation
- **FastAPI:** Modern Python web framework
- **Service Pattern:** Modular architecture

## 📞 Support

### Debugging Steps
1. Check backend terminal for errors
2. Check browser console
3. Verify all API keys
4. Test with simple query
5. Check Google Sheet permissions

### Getting Help
1. Read error messages carefully
2. Check logs in terminal
3. Verify configuration
4. Test API with curl
5. Check API documentation

## ✅ Pre-Flight Checklist

Before first run:
- [ ] Python 3.9+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] OpenAI API key added
- [ ] Serper API key added
- [ ] Google Sheet created
- [ ] Sheet shared with service account
- [ ] credentials.json in place
- [ ] Backend server starts without errors

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Backend starts on port 8000
- ✅ No errors in terminal
- ✅ Frontend loads without errors
- ✅ First search returns results
- ✅ Data appears in Google Sheets
- ✅ Emails are generated
- ✅ Table displays properly

## 📊 System Requirements

**Minimum:**
- Python 3.9+
- 2GB RAM
- Internet connection
- Modern web browser

**Recommended:**
- Python 3.11+
- 4GB RAM
- Fast internet
- Chrome/Firefox browser

## 🔄 Updates & Maintenance

### Keeping Updated
```bash
pip install --upgrade -r requirements.txt
```

### Backup Important Files
- `.env` (configuration)
- `credentials.json` (Google access)
- Generated leads (JSON/Sheets)

### Monitor Usage
- OpenAI: Check billing dashboard
- Serper: Monitor quota
- Google: Check API usage

---

## 🎯 Final Notes

**This is a complete, production-ready system.** Everything you need is included:
- ✅ Full source code
- ✅ Dependencies listed
- ✅ Configuration templates
- ✅ Setup scripts
- ✅ Comprehensive documentation
- ✅ Example requests
- ✅ Error handling
- ✅ Security best practices

**You can start generating leads RIGHT NOW!**

Just follow the setup steps, add your API keys, and you're ready to go! 🚀

---

**Need help? Check the troubleshooting section or review the error messages in your terminal.**
