# Paperclip - Autonomous Computer AI Assistant

<p align="center">
  <strong>Paperclip</strong> is an advanced <strong>Autonomous Computer AI Assistant</strong> designed to transform your computer into an intelligent, interactive, and self-operating system.
</p>

## 🎯 Overview

Paperclip is built using a **fully modular capability-based architecture**. **Every capability is implemented as its own independent source code package (`src/<capability_name>/`) with dedicated classes, utilities, configuration files, prompts, tests, and execution logic.** No capability shares implementation code with another capability. This architecture enables independent development, testing, deployment, upgrading, security auditing, and future expansion of each feature.

### Key Features

- 🤖 **Powered by Gemini AI** - Gemini 2.5 Flash for reasoning, Gemini 1.5 Flash for processing
- 🖥️ **Complete Computer Automation** - Mouse, keyboard, screenshots, OCR
- 🌐 **Browser Automation** - Web browsing, form filling, content extraction
- 📂 **Smart File Management** - Search, organize, open files by name
- 💻 **Development Tools** - Terminal, Git, Python execution
- 📊 **System Monitoring** - CPU, memory, disk, battery tracking
- 🔋 **Power Management** - Shutdown, restart, sleep, lock

## 🏗 Architecture

### One Capability = One Source Code Module

Each capability has its own dedicated module with:
- `__init__.py` - Module initialization
- `main.py` - Main execution logic
- `utils.py` - Utility functions
- `config.yaml` - Module configuration
- `prompts.md` - System prompts
- `tests.py` - Unit tests
- `README.md` - Module documentation

## 📁 Project Structure

```
paperclip/
├── main.py                      # Entry point
├── config.yaml                  # Configuration file
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── src/
│   ├── autonomous_execution_engine/  # Core execution engine
│   ├── model_router/            # AI task routing
│   ├── gemini_25_flash/         # Gemini 2.5 Flash module
│   ├── gemini_15_flash/         # Gemini 1.5 Flash module
│   ├── advanced_planning/       # 113 independent capability modules
│   ├── task_decomposition/
│   ├── workflow_execution/
│   ├── memory_management/
│   ├── decision_engine/
│   ├── reasoning_engine/
│   ├── natural_language_understanding/
│   ├── adaptive_task_planning/
│   ├── mouse_control/
│   ├── keyboard_control/
│   ├── gui_navigation/
│   ├── ocr_processing/
│   ├── screenshot_understanding/
│   ├── window_management/
│   ├── multi_monitor_support/
│   ├── clipboard_management/
│   ├── application_launcher/
│   ├── application_controller/
│   ├── system_settings/
│   ├── startup_management/
│   ├── process_management/
│   ├── service_management/
│   ├── notification_management/
│   ├── audio_control/
│   ├── display_control/
│   ├── network_configuration/
│   ├── storage_management/
│   ├── file_search/
│   ├── folder_search/
│   ├── folder_navigation/
│   ├── file_operations/
│   ├── file_organization/
│   ├── archive_management/
│   ├── download_management/
│   ├── file_indexing/
│   ├── document_retrieval/
│   ├── pdf_processing/
│   ├── word_processing/
│   ├── spreadsheet_processing/
│   ├── excel_automation/
│   ├── csv_processing/
│   ├── database_interaction/
│   ├── report_generation/
│   ├── document_summarization/
│   ├── content_extraction/
│   ├── browser_automation/
│   ├── web_search/
│   ├── website_navigation/
│   ├── search_engine_automation/
│   ├── information_extraction/
│   ├── form_automation/
│   ├── online_research/
│   ├── tab_management/
│   ├── bookmark_management/
│   ├── terminal_execution/
│   ├── powershell_automation/
│   ├── cmd_automation/
│   ├── python_execution/
│   ├── git_automation/
│   ├── package_management/
│   ├── environment_configuration/
│   ├── software_installation/
│   ├── dev_workflow_automation/
│   ├── youtube_control/
│   ├── video_playback/
│   ├── audio_playback/
│   ├── media_download/
│   ├── music_library/
│   ├── playlist_management/
│   ├── whatsapp_automation/
│   ├── group_messaging/
│   ├── contact_management/
│   ├── social_media_automation/
│   ├── messaging_platforms/
│   ├── internet_research/
│   ├── wikipedia_search/
│   ├── ip_lookup/
│   ├── speed_testing/
│   ├── location_detection/
│   ├── cloud_services/
│   ├── battery_monitoring/
│   ├── cpu_monitoring/
│   ├── memory_monitoring/
│   ├── disk_monitoring/
│   ├── gpu_monitoring/
│   ├── system_diagnostics/
│   ├── hardware_information/
│   ├── performance_monitoring/
│   ├── reminder_management/
│   ├── calendar_management/
│   ├── task_organization/
│   ├── productivity_planning/
│   ├── intelligent_notifications/
│   ├── login_automation/
│   ├── logout_automation/
│   ├── signup_automation/
│   ├── multi_account_management/
│   ├── session_management/
│   ├── qr_generation/
│   ├── text_generation/
│   ├── ocr_text_extraction/
│   ├── calculator_engine/
│   ├── unit_conversion/
│   ├── utility_clipboard/
│   ├── screenshot_processing/
│   ├── shutdown_control/
│   ├── restart_control/
│   ├── sleep_control/
│   ├── hibernate_control/
│   ├── lock_control/
│   ├── signout_control/
│   ├── standby_control/
│   └── wake_voice_control/
└── tests/
    └── (test files)
```

## 🤖 AI Architecture

Paperclip uses only Google Gemini models:

### Gemini 2.5 Flash
**Primary Engineering Intelligence Engine**
- Advanced reasoning
- Multi-step planning
- Software architecture design
- Source code generation
- Debugging and optimization
- Autonomous decision making

### Gemini 1.5 Flash
**High-Speed Processing Engine**
- Fast context processing
- File analysis
- Information extraction
- Document parsing
- Workspace scanning

### Model Router
Automatically routes tasks to the appropriate model based on task type.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export GEMINI_API_KEY="your-api-key-here"

# Run interactive mode
python main.py

# Run single task
python main.py --task "Open Chrome and search for news"
```

## 📋 Module Categories

| Category | Modules |
|----------|---------|
| AI Reasoning | 8 modules |
| Computer Interaction | 8 modules |
| Operating System | 11 modules |
| File Management | 9 modules |
| Document Processing | 9 modules |
| Browser | 9 modules |
| Development | 9 modules |
| Multimedia | 6 modules |
| Communication | 5 modules |
| Internet Services | 6 modules |
| Monitoring | 8 modules |
| Productivity | 5 modules |
| Account | 5 modules |
| Utilities | 7 modules |
| Power | 8 modules |

**Total: 113 independent capability modules**

## ⚙ Configuration

Enable/disable individual capabilities in `config.yaml`:

```yaml
capabilities:
  # AI Reasoning
  advanced_planning: true
  task_decomposition: true
  
  # Computer Interaction
  mouse_control: true
  keyboard_control: true
  
  # ... and more
```

## 🏆 Core Philosophy

Paperclip is more than a virtual assistant—it is a capability-oriented autonomous computer operator where **every feature is an independent software component with its own source code, configuration, documentation, and test suite**. By combining AI reasoning, computer vision, operating system automation, browser automation, and autonomous orchestration, Paperclip transforms any computer into an intelligent, self-operating digital workspace capable of completing real-world tasks from start to finish with minimal human supervision.

## 📄 License

MIT License
