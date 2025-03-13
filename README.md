# Gamma EC Auto 🤖📧📞
```markdown
AI-powered insurance outreach automation system with parallel email, phone, and strategy generation.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Twilio](https://img.shields.io/badge/Twilio-9.5-red)](https://www.twilio.com/)

## 🌟 Features

- **Parallel Outreach Execution**
  - Simultaneous email & phone call generation
  - AI-powered follow-up strategies
- **Multi-Format Support**
  - CSV/Excel/JSON input processing
  - Batch operations
- **Smart Communication**
  - LLM-generated personalized content (Llama 3 70B)
  - Objection handling strategies
  - Engagement-level adaptation

## ⚡ Workflow Architecture

```plaintext
           [Input Data]
                │
                ▼
       [Prompt Template]
                │
                ▼
          [LLM Processing]
                │
                ▼
         [JSON Parsing]──────────────────┐
                │                        │
     ┌──────────┴──────────┐             │
     ▼         ▼           ▼             │
[Email]   [Phone]   [Advice Gen]         │
  │          │           │               │
  └─────┬────┴─────┬─────┘               │
        ▼           ▼                    │
  [Status Aggregation]◄──────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Twilio account
- Gmail app password
- [Together.ai](https://together.ai) API key

### Installation
```bash
git clone https://github.com/yourusername/gamma-ec-auto.git
cd gamma-ec-auto

# Create .env file
cp .env.example .env
# Fill in your credentials

# Install dependencies
pip install -r requirements.txt
```

### Docker Setup
```bash
docker build -t gamma-ec-auto .
docker run -p 8000:8000 --env-file .env gamma-ec-auto
```

## 🛠️ Usage

### Single Outreach
```python
response = full_chain.invoke({
    "company_name": "TechCorp",
    "industry": "Fintech",
    "engagement_level": "high",
    "objection": "Security concerns",
    "insurance_company_name": "SafeInsure",
    "sender_name": "John Doe",
    "recipient_email": "contact@techcorp.com",
    "recipient_phone": "+1234567890"
})
```

### Batch Processing
```python
# Process CSV file
company_data = get_company_info('clients.csv')
batch_response = await full_chain.abatch(company_data)
```

## 📡 API Endpoints

### POST `/generate_email`
```json
{
  "company_name": "Example Corp",
  "industry": "Manufacturing",
  "engagement_level": "medium",
  "objections": "Cost concerns",
  "insurance_company_name": "FactoryShield",
  "sender_name": "Jane Smith",
  "recipient_email": "contact@example.com",
  "recipient_phone": "+1234567890"
}
```

### POST `/generate_batch`
- **Accepts**: CSV/Excel files
- **Returns**: Excel file with generated strategies

```bash
curl -X POST -F "file=@clients.csv" http://localhost:8000/generate_batch
```

## 🔧 Configuration

```ini
# .env
ACCOUNT_SID="your_twilio_sid"
AUTH_TOKEN="your_twilio_token"
TWILIO_NUMBER="+1234567890"
EMAIL_APP_PASSWORD="your_gmail_app_password"
TOGETHER_API_KEY="your_together_key"
```

## 📂 Project Structure
```
├── ChainWorkflow/
│   ├── chain.py          # Main execution pipeline
│   └── utils/
│       ├── ec.py         # Email/call implementations
│       ├── model.py      # LLM configuration
│       └── parser.py     # Response formatting
├── main.py               # FastAPI endpoints
├── Dockerfile
└── requirements.txt
```

## 🤝 Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add some feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open a Pull Request

## ⚖️ License
MIT License - See [LICENSE](LICENSE) for details

---

> **Note**  
> Replace placeholder values (`yourusername`, credentials, etc.) with your actual project information before use.
```
