# LiveVox Automation Hub

A comprehensive multi-module automation platform designed for LiveVox call center operations. Built with Python FastAPI and Playwright WebKit for reliable browser automation across three core modules: call recording downloads, HCI summary reports, and phrase management with TTS capabilities.

## 🚀 Core Modules

### 1. LiveVox Call Automation
- **Agent Management**: Manage agents with ID, folder name, and locator ID
- **Call Recording Downloads**: Automated batch download of call recordings
- **Call Data Management**: Track phone numbers and call durations per agent
- **Excel Integration**: Import/export agent and call data via Excel templates
- **Progress Monitoring**: Real-time automation progress with detailed logging

### 2. HCI Summary Report
- **Multi-Agent Processing**: Generate reports for up to 16 predefined HCI agents
- **Automated Report Generation**: Browser automation handles complex report workflows  
- **Date Range Selection**: Flexible date filtering for report scope
- **Batch Processing**: Process multiple agents in a single automation run
- **Data Export**: Export summary reports in Excel format

### 3. Add Phrases (TTS & Audio Management)
- **Phrase Database**: Create and manage phrases with verbiage and descriptions
- **Audio File Upload**: Upload and convert WAV files for phrase association
- **TTS Integration**: Text-to-speech generation for phrases
- **Audio Conversion**: Automatic audio format conversion and storage
- **Phrase Automation**: Automated phrase addition to LiveVox platform

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Linux system dependencies (for Playwright WebKit)

### Quick Start

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd livevox_deployables
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies (Linux)**
   ```bash
   # Install required system packages for Playwright WebKit
   sudo apt-get update
   sudo apt-get install $(cat package.txt | tr '\n' ' ')
   ```

4. **Install Playwright WebKit browser**
   ```bash
   ./setup.sh
   ```
   Or manually:
   ```bash
   python -m playwright install webkit
   ```

5. **Start the application**
   ```bash
   python main.py
   ```

6. **Access the web interface**
   Open your browser to `http://localhost:8001`

## 📖 Usage Guide

### Initial Setup
1. **Configure Credentials**: On the main page, save your LiveVox portal credentials
2. **Select Portal**: Choose between BII_1 or CADEX_2 portals
3. **User Management**: The system tracks users and login sessions

### LiveVox Call Automation

**Agent Management:**
- Add agents with format: Agent ID (e.g., "3P_95"), Folder name, Locator ID
- View existing agents: Chuck (3P_95), Jim (3P_235), Clifford (3P_1483), Kathy (3P_260), Laurie (3P_282)

**Call Data:**
- Add calls with phone numbers (10-digit format) and duration in seconds
- Import bulk call data via Excel templates
- Track call history per agent

**Running Automation:**
- Select "Call Recording Report" function type
- Choose agent and date range
- Monitor real-time progress and logs
- Download results as ZIP file

### HCI Summary Reports

**Available HCI Agents:**
- JCI_HCI_AGENT (3181894)
- BN_HCI_AGENT (3176615)
- AU_HCI_AGENT (3174939)
- DS_HCI_AGENT (3173370)
- FEDEX_HCI_AGENT (3175378)
- And 11 more predefined agents

**Report Generation:**
- Select multiple agents from the list
- Set optional report date
- Provide LiveVox credentials and URL
- Download generated Excel reports

### Phrases Management

**Phrase Operations:**
- Create phrases with name, verbiage, and description
- Upload WAV audio files for association
- Convert audio files to required formats
- Edit and delete existing phrases

**Audio Management:**
- Supported format: WAV files
- Automatic base64 encoding for storage
- In-browser audio playback
- File association with phrases

## 🔧 API Documentation

### Core Endpoints

#### Agent Management
```
GET /api/agents - List LiveVox agents
POST /api/agents - Create agent (agent_id, folder, locator_id)
PUT /api/agents/{agent_id} - Update agent
DELETE /api/agents/{agent_id} - Delete agent
```

#### Call Management
```
GET /api/agents/{agent_id}/calls - Get agent calls
POST /api/agents/{agent_id}/calls - Add call (phone, duration)
PUT /api/agents/{agent_id}/calls/{call_index} - Update call
DELETE /api/agents/{agent_id}/calls/{call_index} - Delete call
```

#### HCI Operations
```
GET /api/hci/agents - List HCI agents
POST /api/hci/agents - Add HCI agent
DELETE /api/hci/agents/{agent_name} - Remove HCI agent
```

#### Phrases Management
```
GET /api/phrases - List all phrases
POST /api/phrases - Create phrase
GET /api/phrases/{phrase_id} - Get specific phrase
PUT /api/phrases/{phrase_id} - Update phrase
DELETE /api/phrases/{phrase_id} - Delete phrase
GET /api/phrases/audio/{filename} - Stream audio file
```

#### Automation Control
```
POST /api/start-automation-fixed - Start LiveVox automation
POST /api/start-hci-automation - Start HCI report automation
POST /api/start-phrases-automation - Start phrases automation
GET /api/automation/{task_id}/status - Check automation status
POST /api/automation/{task_id}/stop - Stop running automation
GET /api/automation/{task_id}/download - Download results
```

### Data Models

#### LiveVox Agent
```json
{
  "id": "3P_95",
  "folder": "Chuck", 
  "locator_id": "963665"
}
```

#### Call Record
```json
{
  "phone": "7028710005",
  "duration": "62"
}
```

#### Phrase
```json
{
  "id": "uuid",
  "phrase_name": "Welcome Message",
  "verbiage": "Welcome to our service",
  "description": "Standard greeting",
  "wav_org_file": {
    "filename": "welcome.wav",
    "original_name": "welcome_message.wav",
    "size": 1024000,
    "base64_content": "..."
  }
}
```

## 📁 Project Structure

```
livevox_deployables/
├── main.py                          # FastAPI application (port 8001)
├── requirements.txt                 # Python dependencies
├── package.txt                      # Linux system dependencies  
├── setup.sh                         # Playwright WebKit installer
├── templates/                       # HTML templates
│   ├── index.html                  # Main dashboard with credential management
│   ├── livevox.html                # LiveVox call automation interface
│   ├── hci_summary.html            # HCI report generation interface
│   ├── add_phrases.html            # Phrases management interface
│   └── admin.html                  # Admin panel
├── static/
│   └── global-progress.js          # Real-time progress tracking
├── Data Files/
│   ├── livevox_data.json           # Agent configs and call data
│   ├── hci_data.json               # HCI agent list (16 agents)
│   ├── phrases_data.json           # Phrases database
│   ├── users.json                  # User accounts and credentials
│   ├── login_logs.json             # Login history tracking
│   ├── sessions.json               # Active user sessions
│   ├── converted_audio_files.json  # Audio file metadata
│   └── active_tasks.json           # Running automation tasks
├── Excel Templates/
│   ├── all_existing_agent_data.xlsx # Agent data template
│   └── call_upload_template.xlsx   # Call data import template
├── tasks/
│   ├── todo.md                     # Task management
│   └── map-positioning-plan.md     # Planning documents
├── chrome-data/                    # Browser automation data
└── CLAUDE.md                       # Development guidelines
```

## ⚙️ Configuration

### Portal Selection
The system supports two LiveVox portals:
- **BII_1**: `https://portal.na6.livevox.com/BII_1`
- **CADEX_2**: `https://portal.na3.livevox.com/CADEX_2`

### Data Storage
- **Format**: JSON files for lightweight data persistence
- **Location**: Root directory alongside main.py
- **Backup**: Manual backup recommended for production use

### Browser Automation
- **Engine**: Playwright WebKit only
- **Timeout**: 45 minutes for HCI, 30 minutes for LiveVox
- **Headless**: Configurable in automation functions

## 🔒 Security & Authentication

- **User Management**: JSON-based user accounts with portal association
- **Session Tracking**: Active session monitoring in sessions.json
- **Login Logging**: All login attempts logged with IP geolocation
- **Credential Storage**: Portal-specific credential management
- **IP Tracking**: Location data for security monitoring

## 🧪 Development

### Key Dependencies
```
fastapi==0.115.12         # Web framework
playwright==1.52.0        # Browser automation  
pandas==2.3.0             # Data processing
openpyxl==3.1.5          # Excel file handling
matplotlib==3.10.3        # Chart generation
uvicorn==0.34.3          # ASGI server
streamlit==1.45.1        # Additional UI components
pygame==2.6.1            # Audio processing
```

### Running in Development
```bash
# Direct execution
python main.py

# Or with uvicorn for auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

### Adding New Modules
1. Create new DataManager class inheriting from DataManager
2. Add corresponding HTML template in templates/
3. Register new routes in main.py
4. Update sidebar navigation in index.html

## 📊 Performance & Monitoring

- **Concurrent Tasks**: Multiple automation tasks supported via active_tasks.json
- **Progress Tracking**: Real-time updates via polling mechanism
- **Memory Management**: Automatic cleanup of completed tasks
- **File Storage**: Base64 encoded audio files in JSON
- **Browser Management**: Automatic WebKit instance cleanup

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**: Application runs on port 8001, check for conflicts
2. **WebKit Installation**: Run `./setup.sh` or manually install webkit browser
3. **System Dependencies**: Install packages from package.txt on Linux systems
4. **File Permissions**: Ensure write access for JSON data files
5. **Audio Upload Issues**: Check file format (WAV only) and size limits

### Browser Automation Issues
- **Timeout Errors**: Check network connectivity and increase timeout values
- **Element Not Found**: LiveVox UI changes may require locator updates
- **Download Failures**: Verify download directory permissions and disk space

### Data Issues
- **JSON Corruption**: Backup and restore from valid JSON files
- **Missing Agents**: Check livevox_data.json and hci_data.json structure
- **Audio File Errors**: Verify base64 encoding in converted_audio_files.json

## 📄 License & Support

This project is designed for LiveVox call center automation. Ensure compliance with your organization's automation policies and LiveVox terms of service.

For technical support:
1. Check application logs in console output
2. Review automation progress logs in web interface  
3. Verify JSON data file integrity
4. Consult troubleshooting section above

---

*Multi-Project LiveVox Automation Hub - Built for efficiency and reliability*