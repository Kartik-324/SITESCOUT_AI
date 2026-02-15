# 🚀 AI Lead Generation & Cold Email Automation System

A production-ready system that automatically finds business leads, extracts contact information, generates personalized cold emails, and saves everything to Google Sheets.

## ✨ Features

- 🔍 **Intelligent Search**: Uses Serper.dev API to search Google
- 🌐 **Web Scraping**: Asynchronously scrapes business websites
- 🤖 **AI Extraction**: OpenAI-powered data extraction from HTML
- 📧 **Email Generation**: Personalized cold emails for each lead
- 📊 **Google Sheets Integration**: Auto-save to spreadsheets
- 📬 **Email Sending**: Optional SMTP integration for bulk emails
- 💻 **Modern Frontend**: Clean, responsive web interface

## 📋 Prerequisites

- Python 3.9+
- OpenAI API Key
- Serper.dev API Key
- Google Cloud Project (for Sheets API)
- SMTP credentials (optional, for email sending)

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
cd lead-gen-system/backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key
SERPER_API_KEY=your-serper-api-key
GOOGLE_SHEET_ID=your-google-sheet-id

# Optional (for email sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

### 5. Configure Google Sheets API

#### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API:
   - Go to "APIs & Services" → "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

#### Step 2: Create Service Account

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in service account details and click "Create"
4. Skip optional steps and click "Done"

#### Step 3: Generate Key

1. Click on the created service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose JSON format
5. Download the JSON file
6. Rename it to `credentials.json`
7. Place it in the `backend/` directory

#### Step 4: Create Google Sheet

1. Create a new Google Sheet
2. Copy the Sheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit
   ```
3. Share the sheet with your service account email:
   - Open the credentials.json file
   - Copy the `client_email` value
   - Share your Google Sheet with this email (Editor access)

### 6. Get API Keys

#### OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create new secret key
5. Copy and save it securely

#### Serper.dev API Key

1. Go to [Serper.dev](https://serper.dev/)
2. Sign up for free account (2,500 free searches)
3. Go to Dashboard
4. Copy your API key

### 7. SMTP Setup (Optional)

For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification
   - App passwords
   - Select "Mail" and your device
   - Copy the generated password
3. Use this app password in `.env` file

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start Frontend

Open `frontend/index.html` in your web browser or use a local server:

```bash
cd frontend
python -m http.server 8080
```

Then visit: `http://localhost:8080`

## 📖 Usage

### Using the Web Interface

1. Open the frontend in your browser
2. Enter a search query (e.g., "best cafes in bhopal")
3. Set maximum results (1-50)
4. Click "Generate Leads"
5. Wait for processing to complete
6. View results in the table
7. Click "View Email" to see generated cold emails
8. Optional: Click "Send Cold Emails" to send via SMTP
9. Optional: Click "Download JSON" to save results locally

### Using the API Directly

#### Generate Leads

```bash
curl -X POST "http://localhost:8000/generate-leads" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "best cafes in bhopal",
    "max_results": 10
  }'
```

#### Response Example

```json
{
  "success": true,
  "message": "Successfully generated 8 leads",
  "total_leads": 8,
  "leads": [
    {
      "business_name": "Coffee House Bhopal",
      "owner_name": "John Doe",
      "rating": "4.5",
      "website": "https://example.com",
      "email": "info@example.com",
      "opening_hours": "9 AM - 10 PM",
      "website_exists": true,
      "cold_email": "Hi,\n\nI came across Coffee House Bhopal..."
    }
  ],
  "saved_to_sheets": true
}
```

#### Send Emails

```bash
curl -X POST "http://localhost:8000/send-emails" \
  -H "Content-Type: application/json" \
  -d '{
    "leads": [...],
    "subject": "Business Opportunity"
  }'
```

#### Health Check

```bash
curl http://localhost:8000/health
```

## 📁 Project Structure

```
lead-gen-system/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Environment configuration
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search_service.py   # Serper API integration
│   │   ├── scraper_service.py  # Web scraping
│   │   ├── extractor_service.py # OpenAI data extraction
│   │   ├── email_generator.py  # Cold email generation
│   │   ├── sheets_service.py   # Google Sheets integration
│   │   └── mail_service.py     # SMTP email sending
│   ├── utils/
│   │   └── __init__.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── .env                    # Your configuration (not in git)
│   ├── credentials.json        # Google service account (not in git)
│   └── README.md
└── frontend/
    ├── index.html              # Main HTML file
    ├── style.css               # Styling
    └── script.js               # Frontend logic
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `SERPER_API_KEY` | Yes | Serper.dev API key |
| `GOOGLE_SHEET_ID` | Yes | Google Sheet ID |
| `GOOGLE_SHEETS_CREDENTIALS_FILE` | Yes | Path to credentials.json |
| `SMTP_HOST` | No | SMTP server host |
| `SMTP_PORT` | No | SMTP server port |
| `SMTP_USERNAME` | No | SMTP username |
| `SMTP_PASSWORD` | No | SMTP password |
| `SMTP_FROM_EMAIL` | No | From email address |

## 🐛 Troubleshooting

### Common Issues

**1. Google Sheets API Error**
- Ensure service account email has access to the sheet
- Check credentials.json is in the correct location
- Verify Google Sheets API is enabled

**2. OpenAI API Error**
- Check API key is valid
- Ensure you have credits in your OpenAI account
- Verify model name is correct (gpt-4o-mini)

**3. Serper API Error**
- Verify API key is correct
- Check you haven't exceeded rate limits
- Ensure you have remaining credits

**4. SMTP Error**
- For Gmail, use App Password, not regular password
- Enable "Less secure app access" or use App Password
- Check firewall/antivirus isn't blocking SMTP

**5. CORS Error in Frontend**
- Ensure backend is running on localhost:8000
- Check CORS middleware is properly configured
- Use browser dev tools to see exact error

## 📊 Google Sheets Output

The system creates the following columns:

| Column | Description |
|--------|-------------|
| Name | Business name |
| Owner | Owner/founder name |
| Rating | Business rating |
| Website | Website URL |
| Email | Contact email |
| Opening Hours | Business hours |
| Website Exists | Boolean (TRUE/FALSE) |
| Cold Email | Generated personalized email |

## 🔐 Security Notes

- Never commit `.env` file or `credentials.json`
- Keep API keys secure
- Use environment variables for sensitive data
- Rotate API keys regularly
- Be mindful of API rate limits and costs

## 📈 Scaling & Performance

- Async operations for fast concurrent scraping
- Configurable result limits to manage costs
- Rate limiting on API calls
- Error handling for failed scrapes
- Modular architecture for easy modifications

## 🤝 Contributing

This is a production-ready template. Feel free to:
- Add more data extraction fields
- Improve email templates
- Add more integrations (Airtable, Notion, etc.)
- Enhance error handling
- Add authentication

## 📝 License

This project is provided as-is for educational and commercial use.

## 🙏 Credits

- OpenAI for GPT models
- Serper.dev for search API
- Google for Sheets API
- FastAPI framework
- BeautifulSoup for web scraping

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review error logs
3. Verify all API keys are correct
4. Ensure all dependencies are installed

---

**Built with ❤️ using Python, FastAPI, OpenAI, and modern web technologies**
