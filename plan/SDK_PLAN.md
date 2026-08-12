# Paperclip - Autonomous Computer AI Assistant

## Executive Summary

Paperclip is an advanced Autonomous Computer AI Assistant built using the OpenHands Software Agent SDK. It transforms any computer into an intelligent, interactive, and self-operating system powered by **Gemini 2.5 Flash**.

---

## 1. Architecture Overview

### 1.1 Core Components

```
┌─────────────────────────────────────────────────────────────────┐
│                      Paperclip Agent                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Gemini 2.5   │  │   Agent      │  │   Skills &   │          │
│  │ Flash LLM    │──▶│   Core       │──▶│   Context    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                           │                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Tool System                           │   │
│  ├──────────────────────────────────────────────────────────┤   │
│  │ Computer │ OS     │ File   │ Browser │ Terminal │ More... │   │
│  │ Automation│ Auto   │ Manage │ Auto    │ / Dev    │         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Technology Stack

- **LLM**: Gemini 2.5 Flash (via Google AI API)
- **Framework**: OpenHands Software Agent SDK
- **Language**: Python 3.13+
- **Architecture**: Modular tool-based system

---

## 2. Module Specifications

### 2.1 Core AI Module

**File**: `output/paperclip/core/ai_module.py`

| Capability | Implementation |
|------------|----------------|
| LLM Integration | Gemini 2.5 Flash via `google-generativeai` or LiteLLM |
| Planning | Multi-step task decomposition |
| Reasoning | Chain-of-thought reasoning |
| Memory | Long-context conversation history |
| Decision Making | Context-aware intelligent decisions |

### 2.2 Computer Automation Module

**File**: `output/paperclip/modules/computer_automation.py`

| Tool | Description |
|------|-------------|
| Mouse Control | Move, click, scroll operations |
| Keyboard Control | Type, hotkeys, shortcuts |
| Screenshot | Capture and analyze screen |
| Window Management | Focus, move, resize windows |
| OCR | Extract text from images/screens |

### 2.3 OS Automation Module

**File**: `output/paperclip/modules/os_automation.py`

| Tool | Description |
|------|-------------|
| App Launcher | Launch applications by name |
| App Closer | Close applications gracefully |
| Process Manager | List, kill, manage processes |
| System Settings | Configure OS preferences |
| Service Manager | Start/stop system services |

### 2.4 File Management Module

**File**: `output/paperclip/modules/file_management.py`

| Tool | Description |
|------|-------------|
| Smart Search | Find files by name/content |
| File Operations | Copy, move, rename, delete |
| Folder Navigation | Open folders, create directories |
| File Organization | Sort, categorize files |

### 2.5 Browser Automation Module

**File**: `output/paperclip/modules/browser_automation.py`

| Tool | Description |
|------|-------------|
| Web Navigation | Navigate URLs, click links |
| Form Filling | Auto-fill web forms |
| Search | Google, Bing, DuckDuckGo |
| Tab Management | Open, close, switch tabs |
| Content Extraction | Scrape web content |

### 2.6 Document Processing Module

**File**: `output/paperclip/modules/document_processing.py`

| Tool | Description |
|------|-------------|
| PDF Reader | Extract text from PDFs |
| Word Analyzer | Read .docx files |
| Spreadsheet | Read/write Excel/CSV |
| Report Generator | Create summaries |

### 2.7 Terminal & Development Module

**File**: `output/paperclip/modules/terminal_dev.py`

| Tool | Description |
|------|-------------|
| Bash/PowerShell | Execute shell commands |
| Git Operations | Clone, commit, push, pull |
| Python Runner | Execute Python scripts |
| Package Manager | Install/update packages |

### 2.8 System Monitoring Module

**File**: `output/paperclip/modules/system_monitoring.py`

| Tool | Description |
|------|-------------|
| CPU Monitor | Track processor usage |
| Memory Tracker | Monitor RAM usage |
| Disk Analyzer | Check storage |
| Battery Info | Power status |

### 2.9 Communication Module

**File**: `output/paperclip/modules/communication.py`

| Tool | Description |
|------|-------------|
| WhatsApp | Send/receive messages |
| Email | (Future extension point) |

### 2.10 Power Management Module

**File**: `output/paperclip/modules/power_management.py`

| Tool | Description |
|------|-------------|
| Shutdown | Power off system |
| Restart | Reboot system |
| Sleep/Hibernate | Power saving modes |
| Lock | Lock screen |

---

## 3. Implementation Plan

### Phase 1: Core Infrastructure (Day 1)
- [ ] Set up project structure
- [ ] Configure Gemini 2.5 Flash LLM
- [ ] Implement base agent with skills
- [ ] Create logging system

### Phase 2: Essential Tools (Day 1-2)
- [ ] Terminal tool (built-in)
- [ ] File editor tool (built-in)
- [ ] Browser tool set
- [ ] Custom computer automation tools

### Phase 3: Advanced Modules (Day 2-3)
- [ ] OS automation module
- [ ] Document processing
- [ ] System monitoring
- [ ] Communication tools

### Phase 4: Integration & Testing (Day 3-4)
- [ ] Combine all modules
- [ ] End-to-end testing
- [ ] Error handling
- [ ] Documentation

---

## 4. File Structure

```
paperclip/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── core/
│   ├── __init__.py
│   ├── agent.py           # Core PaperclipAgent class
│   ├── config.py          # Configuration
│   └── skills/
│       ├── __init__.py
│       ├── system.md      # System instructions
│       └── capabilities.md # Capability descriptions
├── modules/
│   ├── __init__.py
│   ├── computer_automation.py
│   ├── os_automation.py
│   ├── file_management.py
│   ├── browser_automation.py
│   ├── document_processing.py
│   ├── terminal_dev.py
│   ├── system_monitoring.py
│   ├── communication.py
│   ├── power_management.py
│   └── utilities.py
└── tools/
    ├── __init__.py
    └── custom_tools.py    # Custom tool definitions
```

---

## 5. Skills & Prompts

### 5.1 System Prompt
The agent will have a comprehensive system prompt explaining its role as Paperclip, an autonomous computer assistant with all the capabilities listed in the specification.

### 5.2 Capability Skills
Each major capability area will have associated skills that provide:
- Detailed instructions on when to use tools
- Best practices for specific tasks
- Error handling guidance

---

## 6. LLM Configuration

### 6.1 Gemini 2.5 Flash Setup

```python
from openhands.sdk import LLM

llm = LLM(
    model="gemini/gemini-2.5-flash",  # Using LiteLLM format
    api_key=os.getenv("GEMINI_API_KEY"),
    # Alternative: use base_url for Google AI
    # base_url="https://generativelanguage.googleapis.com/v1beta",
)
```

### 6.2 Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| Model | LLM model name | gemini/gemini-2.5-flash |
| API Key | Gemini API key | From environment |
| Temperature | Response randomness | 0.7 |
| Max Tokens | Maximum response length | 8192 |

---

## 7. Tool Registration

Tools will be registered using the OpenHands SDK's `register_tool` decorator, with custom executors for each capability area.

```python
from openhands.sdk.tool import register_tool

@register_tool("paperclip.computer_automation")
class ComputerAutomationToolset(ToolDefinition):
    # Tool implementation
    pass
```

---

## 8. Running Paperclip

### 8.1 Command Line Usage

```bash
# Set API key
export GEMINI_API_KEY="your-api-key"

# Run interactive session
python paperclip/main.py

# Run single task
python paperclip/main.py --task "Open Chrome and search for weather"
```

### 8.2 Configuration File

```yaml
# config.yaml
llm:
  model: gemini/gemini-2.5-flash
  temperature: 0.7
  
capabilities:
  computer_automation: true
  browser_automation: true
  file_management: true
  
logging:
  level: INFO
  file: paperclip.log
```

---

## 9. Success Criteria

- [ ] Agent can understand natural language instructions
- [ ] Agent can execute multi-step tasks autonomously
- [ ] Agent can recover from errors gracefully
- [ ] All 15 capability modules are functional
- [ ] Agent can work with files, browser, and system
- [ ] Comprehensive logging and error handling
- [ ] Clean, maintainable code structure

---

## 10. Future Enhancements

- Multi-agent coordination
- Persistent memory across sessions
- Learning from user preferences
- Custom plugin system
- Mobile companion app
- Voice interaction
