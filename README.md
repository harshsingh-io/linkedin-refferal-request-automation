
# LinkedIn Connection Request Automation

An automated tool to send personalized LinkedIn connection requests based on specified search criteria. The tool uses Selenium WebDriver to automate browser interactions with LinkedIn.

## Features

- Search for LinkedIn profiles based on company, role, and location
- Send personalized connection requests with custom messages
- Configurable search criteria and connection message templates
- Built-in rate limiting and random delays to avoid detection
- Detailed logging of all operations
- Chrome browser automation using Selenium

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- LinkedIn account

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd linkedin-request-automation
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy the example configuration file:
```bash
cp config/config.example.yaml config/config.yaml
```

2. Update `config/config.yaml` with your settings:
```yaml
# Search Criteria
search:
  company_name: "Company Name"
  location: "Location"
  role_category: "Role"
  max_requests: 10
  mutual_connections: false

# Connection Message Template
connection_message: "Your connection message here"

# LinkedIn Credentials
credentials:
  email: "your-email@example.com"
  password: "your-password"
```

## Usage

Run the main script:
```bash
python main.py
```

The script will:
1. Log in to LinkedIn using provided credentials
2. Search for profiles matching your criteria
3. Send connection requests with your custom message
4. Log all activities in the `logs` directory

## Project Structure

```
linkedin_automation/
├── config/
│   └── config.py         # Configuration handling
├── src/
│   ├── auth.py          # LinkedIn authentication
│   ├── linkedin_api.py  # Core LinkedIn automation
│   ├── message_handler.py # Message processing
│   └── utils.py         # Utility functions
├── logs/                # Log files directory
├── main.py             # Main entry point
└── requirements.txt    # Project dependencies
```

## Safety and Rate Limiting

The tool includes several safety features:
- Random delays between requests
- Configurable maximum request limits
- Logging of all operations for monitoring
- Error handling and recovery

## Logging

Logs are stored in the `logs` directory:
- `linkedin_api.log`: API operations and connection requests
- `linkedin_auth.log`: Authentication events
- `main.log`: General application logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with LinkedIn's terms of service. Automated actions on LinkedIn may be against their user agreement.
