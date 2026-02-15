# 🚀 SITESCOUT_AI (AI Lead Generation & Cold Email Automation System )

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Complete production-ready system for automated lead generation and personalized cold email creation.**

## 🎯 What This System Does

1. 🔍 **Searches Google** for businesses matching your query
2. 🌐 **Scrapes websites** to extract contact information
3. 🤖 **Uses AI** to structure and clean the data
4. 📧 **Generates and send personalized** cold emails for each lead
5. 📊 **Saves automatically** to Google Sheets
6. 📬 **Optionally sends** emails via SMTP

**Example:** Type "best cafes in bhopal" → Get 10 leads with emails, ratings, and personalized cold emails in 60 seconds!



## 📸 Working UI

![UI 1](https://raw.githubusercontent.com/Kartik-324/SITESCOUT_AI/main/Working%20UI/Screenshot%202026-02-14%20180247.png)

![UI 2](https://raw.githubusercontent.com/Kartik-324/SITESCOUT_AI/main/Working%20UI/Screenshot%202026-02-15%20091943.png)

![UI 3](https://raw.githubusercontent.com/Kartik-324/SITESCOUT_AI/main/Working%20UI/Screenshot%202026-02-15%20092000.png)

![UI 4](https://raw.githubusercontent.com/Kartik-324/SITESCOUT_AI/main/Working%20UI/Screenshot%202026-02-15%20092045.png)

![UI 5](https://raw.githubusercontent.com/Kartik-324/SITESCOUT_AI/main/Working%20UI/Screenshot%202026-02-15%20092143.png)

![UI 6](https://raw.githubusercontent.com/Kartik-324/SITESCOUT_AI/main/Working%20UI/Screenshot%202026-02-15%20092320.png)


---

## ⚡ Quick Start (3 Steps)

### 1. Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

### 2. Run
```bash
python main.py
```

### 3. Use
Open `frontend/index.html` in your browser → Enter query → Generate leads!

**Full setup guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📁 Project Structure

```
lead-gen-system/
│
├── 📄 README.md                    ← You are here
├── 📄 DEPLOYMENT_GUIDE.md          ← Complete setup & deployment guide
├── 📄 QUICKSTART.md                ← 5-minute quick start
├── 📄 PROJECT_SUMMARY.md           ← Technical overview
├── 🔧 setup.sh                     ← Auto-setup script (Linux/Mac)
├── 🔧 setup.bat                    ← Auto-setup script (Windows)
│
├── backend/                        ← Python/FastAPI backend
│   ├── main.py                     ← Main API application
│   ├── requirements.txt            ← Python dependencies
│   ├── .env.example                ← Configuration template
│   ├── README.md                   ← Backend documentation
│   ├── API_EXAMPLES.md             ← API usage examples
│   │
│   ├── config/                     ← Configuration management
│   │   ├── settings.py             ← Environment variables
│   │   └── __init__.py
│   │
│   ├── services/                   ← Business logic services
│   │   ├── search_service.py       ← Google search (Serper API)
│   │   ├── scraper_service.py      ← Website scraping
│   │   ├── extractor_service.py    ← AI data extraction
│   │   ├── email_generator.py      ← Cold email generation
│   │   ├── sheets_service.py       ← Google Sheets integration
│   │   ├── mail_service.py         ← Email sending (SMTP)
│   │   └── __init__.py
│   │
│   └── utils/                      ← Utility functions
│       └── __init__.py
│
└── frontend/                       ← Web interface
    ├── index.html                  ← Main HTML page
    ├── style.css                   ← Styling
    └── script.js                   ← Frontend logic
```

---

## 🎓 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This overview (start here) |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Complete setup, deployment & usage |
| [QUICKSTART.md](QUICKSTART.md) | Get started in 5 minutes |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Technical details & architecture |
| [backend/README.md](backend/README.md) | Backend-specific documentation |
| [backend/API_EXAMPLES.md](backend/API_EXAMPLES.md) | API request/response examples |

---

## ✨ Features

### Core Features
- ✅ **AI-Powered Search** - Intelligent Google search via Serper.dev
- ✅ **Async Web Scraping** - Fast concurrent website scraping
- ✅ **Smart Data Extraction** - OpenAI-powered information extraction
- ✅ **Email Generation** - Personalized cold emails for each lead
- ✅ **Google Sheets Integration** - Auto-save with formatted columns
- ✅ **SMTP Support** - Optional bulk email sending
- ✅ **Modern UI** - Clean, responsive web interface
- ✅ **Production Ready** - Error handling, logging, validation

### Technical Features
- ⚡ Async/await for performance
- 🔒 Environment-based configuration
- 📝 Comprehensive logging
- ✅ Input validation (Pydantic)
- 🎨 Responsive frontend
- 📊 Real-time progress indicators
- 💾 JSON export capability
- 🔄 Auto-generated API docs

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- httpx - Async HTTP client
- BeautifulSoup - HTML parsing
- OpenAI API - AI data extraction & email generation
- Google Sheets API - Data storage
- aiosmtplib - Async email sending

**Frontend:**
- HTML5/CSS3 - Modern web standards
- Vanilla JavaScript - No frameworks needed
- Fetch API - HTTP requests
- Responsive Design - Mobile-friendly

---

## 🔑 Required API Keys

| Service | Cost | Setup Link |
|---------|------|------------|
| OpenAI | ~$0.01-0.05 per 10 leads | [platform.openai.com](https://platform.openai.com/api-keys) |
| Serper.dev | FREE (2,500/month) | [serper.dev](https://serper.dev/) |
| Google Sheets | FREE | [console.cloud.google.com](https://console.cloud.google.com/) |
| SMTP (Gmail) | FREE | [Google App Passwords](https://myaccount.google.com/apppasswords) |

**Total Cost:** ~$0.01-0.05 per 10 leads (essentially free for testing)

---

## 📊 Sample Output

### Input
```json
{
  "query": "best cafes in bhopal",
  "max_results": 5
}
```

### Output (Google Sheets)
| Name | Owner | Rating | Website | Email | Opening Hours | Website Exists | Cold Email |
|------|-------|--------|---------|-------|---------------|----------------|------------|
| Cafe Coffee Day | John Smith | 4.5 | example.com | contact@... | 8 AM - 10 PM | TRUE | Hi, I came across... |
| Starbucks Bhopal | | 4.3 | starbucks.com | info@... | 7 AM - 11 PM | TRUE | Hi, I noticed... |

---

## 🚀 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/generate-leads` | POST | Generate leads from query |
| `/send-emails` | POST | Send bulk cold emails |
| `/health` | GET | Detailed service status |
| `/docs` | GET | Interactive API documentation |

**Full API docs:** Visit `http://localhost:8000/docs` after starting the server

---

## 💻 Usage Examples

### Web Interface
```
1. Open frontend/index.html
2. Enter: "best cafes in bhopal"
3. Click "Generate Leads"
4. View results in table
5. Click "View Email" to see cold emails
6. Optional: Send emails or download JSON
```

### API (cURL)
```bash
curl -X POST "http://localhost:8000/generate-leads" \
  -H "Content-Type: application/json" \
  -d '{"query": "best cafes in bhopal", "max_results": 10}'
```

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/generate-leads",
    json={"query": "best cafes in bhopal", "max_results": 10}
)

data = response.json()
print(f"Generated {data['total_leads']} leads")
```

---

## 🎯 Use Cases

- 🍽️ **Restaurant Outreach** - Find and contact local restaurants
- ☕ **Cafe Partnerships** - Discover cafes for collaborations
- 💪 **Gym Marketing** - Contact gyms for B2B services
- 🏪 **Retail Lead Gen** - Find retail stores in any area
- 🏢 **B2B Sales** - Generate leads for any industry
- 📧 **Email Campaigns** - Build targeted contact lists

---

## 📈 Performance

- ⚡ **Fast:** Processes 10 leads in ~60 seconds
- 🔄 **Concurrent:** Async scraping of multiple sites
- 💰 **Cost-effective:** ~$0.01-0.05 per 10 leads
- 📊 **Scalable:** Handle 1-50 results per query
- 🛡️ **Reliable:** Comprehensive error handling

---

## 🔒 Security

- ✅ Environment variables for secrets
- ✅ .gitignore configured
- ✅ No hardcoded credentials
- ✅ Input validation
- ✅ CORS configuration
- ✅ Secure API practices

---

## 🐛 Troubleshooting

### Common Issues

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Google Sheets permission denied"**
- Share sheet with service account email from credentials.json

**"Invalid API key"**
- Check .env file has correct keys
- Verify keys are active

**See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete troubleshooting**

---

## 📚 Learn More

### Documentation
- [Complete Setup Guide](DEPLOYMENT_GUIDE.md) - Detailed instructions
- [Quick Start](QUICKSTART.md) - Get running in 5 minutes
- [Technical Overview](PROJECT_SUMMARY.md) - Architecture details
- [API Examples](backend/API_EXAMPLES.md) - Request/response samples

### External Resources
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Serper.dev Docs](https://serper.dev/docs)
- [Google Sheets API](https://developers.google.com/sheets/api)

---

## 🤝 Contributing

This is a complete, production-ready system. Feel free to:
- Fork and customize
- Add new features
- Improve email templates
- Enhance UI/UX
- Add more integrations

---

## 📝 License

This project is provided as-is for educational and commercial use.

---

## 🙏 Credits

**Built with:**
- OpenAI GPT-4o-mini
- Serper.dev Search API
- Google Sheets API
- FastAPI Framework
- BeautifulSoup

---

## 🎉 Ready to Start?

1. **Automated:** Run `./setup.sh` (Linux/Mac) or `setup.bat` (Windows)
2. **Manual:** Follow [QUICKSTART.md](QUICKSTART.md)
3. **Detailed:** Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Questions?** Check the documentation files listed above!

---

<div align="center">

**⭐ If this helps you, consider starring the repository! ⭐**

**Built with ❤️ using AI and modern web technologies**

[Get Started](QUICKSTART.md) · [Full Guide](DEPLOYMENT_GUIDE.md) · [API Docs](backend/API_EXAMPLES.md)

</div>
