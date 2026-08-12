# Paperclip - Autonomous Computer AI Assistant

<p align="center">
  <strong>Paperclip</strong> is an advanced <strong>Autonomous Computer AI Assistant</strong> designed to transform your computer into an intelligent, interactive, and self-operating system.
</p>

## 🎯 Overview

Paperclip is built using a modular architecture where each major capability is implemented as an independent module. It leverages the power of **Gemini 2.5 Flash** for intelligent reasoning and planning, combined with the **OpenHands SDK** for robust agent orchestration.

### Key Features

- 🤖 **Powered by Gemini 2.5 Flash** - Advanced AI with planning and reasoning
- 🖥️ **Complete Computer Automation** - Mouse, keyboard, screenshots, OCR
- 🌐 **Browser Automation** - Web browsing, form filling, content extraction
- 📂 **Smart File Management** - Search, organize, open files by name
- 💻 **Development Tools** - Terminal, Git, Python execution
- 📊 **System Monitoring** - CPU, memory, disk, battery tracking
- 🔋 **Power Management** - Shutdown, restart, sleep, lock

## 📁 Project Structure

```
output/paperclip/
├── main.py                    # Entry point
├── config.yaml                # Configuration file
├── requirements.txt           # Dependencies
├── core/
│   ├── agent.py              # Core PaperclipAgent class
│   ├── config.py             # Configuration management
│   └── skills/               # Agent skills and context
├── modules/                   # 12 specialized modules
│   ├── computer_automation.py
│   ├── os_automation.py
│   ├── file_management.py
│   ├── browser_automation.py
│   ├── document_processing.py
│   ├── terminal_dev.py
│   ├── system_monitoring.py
│   ├── communication.py
│   ├── power_management.py
│   ├── utilities.py
│   ├── internet_services.py
│   └── multimedia.py
└── tools/                    # Custom tools
```

## 🚀 Quick Start

```bash
cd output/paperclip

# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Run interactive mode
python main.py

# Run single task
python main.py --task "Open Chrome and search for news"
```

## 📋 Modules Overview

| Module | Description |
|--------|-------------|
| **Computer Automation** | Mouse control, keyboard, screenshots, OCR, window management |
| **OS Automation** | App launching, process management, system settings |
| **File Management** | Search, copy, move, organize files |
| **Browser Automation** | Web browsing, scraping, form filling |
| **Document Processing** | PDF, Word, Excel, CSV handling |
| **Terminal/Dev** | Shell commands, Git, Python execution |
| **System Monitoring** | CPU, memory, disk, battery tracking |
| **Communication** | WhatsApp messaging |
| **Power Management** | Shutdown, restart, sleep, lock |
| **Utilities** | Calculator, OCR, QR codes, conversions |
| **Internet Services** | IP lookup, speed test, DNS |
| **Multimedia** | Video/audio playback, YouTube |

## 📖 Documentation

See [output/paperclip/README.md](output/paperclip/README.md) for full documentation.

## 📄 License

MIT License
