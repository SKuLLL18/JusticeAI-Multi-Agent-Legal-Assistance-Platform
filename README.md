# JusticeAI: Multi-Agent Legal Assistance Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![SDG](https://img.shields.io/badge/SDG-Goal%2016-orange.svg)](https://sdgs.un.org/goals/goal16)

> An intelligent web-based platform that uses Multi-Agent Systems (MAS) and Artificial Intelligence (AI) to help citizens resolve legal issues, understand basic laws, and access justice efficiently.

## 🧠 Project Overview

JusticeAI simulates the roles of legal institutions using multiple intelligent agents that collaborate to provide advice, suggest resolutions, and escalate cases if needed — all through an easy-to-use web interface.

This project supports **SDG Goal 16: Peace, Justice, and Strong Institutions**, making legal aid more accessible and efficient using technology.

## 🎯 Key Features

- 🤖 **Multi-Agent System**: 5 specialized AI agents working collaboratively
- ⚖️ **AI Legal Expert**: Intelligent legal advice using OpenAI/Gemini APIs
- 🤝 **Mediation Support**: Peaceful conflict resolution strategies
- 📄 **PDF Reports**: Professional case documentation and analysis
- 🚨 **Escalation System**: Critical case identification and routing
- 📱 **Responsive Design**: Works on all devices and screen sizes
- 🔒 **Privacy Focused**: No sensitive data stored permanently

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Multi-Agent   │
│   (HTML/CSS/JS) │◄──►│   (Flask)       │◄──►│   System        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   Database      │    │   PDF Reports   │
                       │   (SQLite)      │    │   (ReportLab)   │
                       └─────────────────┘    └─────────────────┘
```

## 🤖 Multi-Agent System

### Agent Overview:
1. **🧑‍💼 User Agent**: Case intake and coordination
2. **⚖️ Legal Expert Agent**: AI-powered legal advice
3. **🤝 Mediation Agent**: Conflict resolution strategies
4. **📊 Report Agent**: PDF report generation
5. **🚨 Escalation Agent**: Critical case assessment

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/JusticeAI.git
   cd JusticeAI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   ```
   Open your browser and go to: http://localhost:5001
   ```

## 📦 Project Structure

```
JusticeAI/
├── app.py                          # Main Flask application
├── agents/                         # Multi-agent system modules
│   ├── __init__.py
│   ├── user_agent.py              # User interaction & coordination
│   ├── legal_agent.py             # AI-powered legal advice
│   ├── mediation_agent.py         # Conflict resolution
│   ├── report_agent.py            # PDF report generation
│   └── escalation_agent.py        # Critical case handling
├── static/                        # Frontend assets
│   ├── style.css                  # Main stylesheet
│   ├── script.js                  # Frontend JavaScript
│   ├── ibm_logo.svg              # Partner logos
│   └── csrbox_logo.svg
├── templates/                     # HTML templates
│   └── index.html                # Main application page
├── reports/                       # Generated PDF reports
├── database/                      # SQLite database
├── requirements.txt               # Python dependencies
├── requirements-basic.txt         # Minimal dependencies
├── requirements-minimal.txt       # Core dependencies
├── JusticeAI_Project_Documentation.md  # Complete project documentation
└── README.md                     # This file
```

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | User interface and interactions |
| **Backend** | Python Flask | Web server and API endpoints |
| **Agents** | Python Classes | Multi-agent system implementation |
| **Database** | SQLite | Case storage and management |
| **PDF Generation** | ReportLab | Professional report creation |
| **AI Integration** | OpenAI/Gemini APIs | Intelligent legal advice |
| **Styling** | Custom CSS + FontAwesome | Modern, responsive design |

## 📋 Features in Detail

### 1. Case Submission System
- Comprehensive form with validation
- Real-time character counter
- Category and priority selection
- Email validation and error handling

### 2. Multi-Agent Processing
- Real-time agent status updates
- Visual progress indicators
- Simulated processing for realistic UX
- Comprehensive case analysis

### 3. Results Display
- Structured agent outputs
- Professional formatting
- Responsive design
- Downloadable PDF reports

### 4. PDF Report Generation
- Professional formatting with branding
- Comprehensive case summary
- Structured sections for all agent outputs
- Unique file naming with case tracking

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
```

### API Keys
- **OpenAI API**: For advanced legal advice (optional)
- **Google Gemini API**: Alternative AI provider (optional)
- **Fallback**: Rule-based system works without API keys

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment

#### Option 1: Render.com
1. Connect your GitHub repository to Render
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `python app.py`
4. Deploy automatically

#### Option 2: Heroku
```bash
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy to Heroku
heroku create justiceai-app
git push heroku main
```

#### Option 3: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
```

## 📊 API Endpoints

### Main Routes
- `GET /` - Main application page
- `GET /health` - System health check
- `POST /submit_case` - Process case submission
- `GET /download_report/<case_id>` - Download PDF report

### API Response Format
```json
{
    "success": true,
    "case_id": "unique_case_identifier",
    "legal_advice": "AI-generated legal analysis...",
    "mediation_suggestions": "Conflict resolution strategies...",
    "escalation_recommendations": "Critical case assessment...",
    "priority_level": "medium",
    "issue_category": "property_dispute"
}
```

## 🎯 SDG Alignment

This project directly supports **SDG Goal 16: Peace, Justice, and Strong Institutions** by:

- **Target 16.3**: Promote the rule of law and ensure equal access to justice
- **Target 16.6**: Develop effective, accountable, and transparent institutions
- **Target 16.10**: Ensure public access to information and protect fundamental freedoms

### Impact Metrics
- **Geographic Reach**: Accessible to rural and urban populations
- **Cost Reduction**: Free initial legal guidance
- **Time Efficiency**: Immediate response vs. traditional delays
- **Knowledge Empowerment**: Legal literacy improvement

## 👥 Development Team

- **Yash Sakariya** - Team Lead
- **Arpit Patoliya** - Team Member
- **Madhavi Parmar** - Team Member
- **Hill Soni** - Team Member
- **Arya Patel** - Team Member

## 📞 Contact

- **Email**: sakariyayash04@gmail.com
- **Project Repository**: [JusticeAI Multi-Agent System](https://github.com/yourusername/JusticeAI)
- **Platform**: Web-based application

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📚 Documentation

For detailed project documentation, see [JusticeAI_Project_Documentation.md](JusticeAI_Project_Documentation.md)

## ⚠️ Disclaimer

This platform provides informational guidance only and does not constitute legal advice. Please consult with qualified legal professionals for formal legal counsel.

---


**Built with ❤️ for SDG Goal 16: Peace, Justice, and Strong Institutions** 
