"""
Capability Manager
=================
Manages loading and coordination of all capability modules.
"""

import importlib
import os
from typing import Any, Dict, List, Optional
from pathlib import Path

from loguru import logger


class CapabilityManager:
    """
    Manages all capability modules in the system.
    
    Each capability is loaded independently and can be
    enabled/disabled without affecting other capabilities.
    """

    # List of all capability module names
    CAPABILITIES = [
        # AI Reasoning
        "advanced_planning",
        "task_decomposition",
        "workflow_execution",
        "memory_management",
        "decision_engine",
        "reasoning_engine",
        "natural_language_understanding",
        "adaptive_task_planning",
        
        # Computer Interaction
        "mouse_control",
        "keyboard_control",
        "gui_navigation",
        "ocr_processing",
        "screenshot_understanding",
        "window_management",
        "multi_monitor_support",
        "clipboard_management",
        
        # Operating System
        "application_launcher",
        "application_controller",
        "system_settings",
        "startup_management",
        "process_management",
        "service_management",
        "notification_management",
        "audio_control",
        "display_control",
        "network_configuration",
        "storage_management",
        
        # File Management
        "file_search",
        "folder_search",
        "folder_navigation",
        "file_operations",
        "file_organization",
        "archive_management",
        "download_management",
        "file_indexing",
        "document_retrieval",
        
        # Document Processing
        "pdf_processing",
        "word_processing",
        "spreadsheet_processing",
        "excel_automation",
        "csv_processing",
        "database_interaction",
        "report_generation",
        "document_summarization",
        "content_extraction",
        
        # Browser
        "browser_automation",
        "web_search",
        "website_navigation",
        "search_engine_automation",
        "information_extraction",
        "form_automation",
        "online_research",
        "tab_management",
        "bookmark_management",
        
        # Development
        "terminal_execution",
        "powershell_automation",
        "cmd_automation",
        "python_execution",
        "git_automation",
        "package_management",
        "environment_configuration",
        "software_installation",
        "dev_workflow_automation",
        
        # Multimedia
        "youtube_control",
        "video_playback",
        "audio_playback",
        "media_download",
        "music_library",
        "playlist_management",
        
        # Communication
        "whatsapp_automation",
        "group_messaging",
        "contact_management",
        "social_media_automation",
        "messaging_platforms",
        
        # Internet Services
        "internet_research",
        "wikipedia_search",
        "ip_lookup",
        "speed_testing",
        "location_detection",
        "cloud_services",
        
        # Monitoring
        "battery_monitoring",
        "cpu_monitoring",
        "memory_monitoring",
        "disk_monitoring",
        "gpu_monitoring",
        "system_diagnostics",
        "hardware_information",
        "performance_monitoring",
        
        # Productivity
        "reminder_management",
        "calendar_management",
        "task_organization",
        "productivity_planning",
        "intelligent_notifications",
        
        # Account
        "login_automation",
        "logout_automation",
        "signup_automation",
        "multi_account_management",
        "session_management",
        
        # Utilities
        "qr_generation",
        "text_generation",
        "ocr_text_extraction",
        "calculator_engine",
        "unit_conversion",
        "utility_clipboard",
        "screenshot_processing",
        
        # Power
        "shutdown_control",
        "restart_control",
        "sleep_control",
        "hibernate_control",
        "lock_control",
        "signout_control",
        "standby_control",
        "wake_voice_control",
    ]

    def __init__(self, enabled_capabilities: Optional[List[str]] = None):
        """
        Initialize the capability manager.
        
        Args:
            enabled_capabilities: List of enabled capability names.
                                  If None, all capabilities are enabled.
        """
        self.enabled_capabilities = set(enabled_capabilities) if enabled_capabilities else set(self.CAPABILITIES)
        self.loaded_capabilities: Dict[str, Any] = {}
        
        logger.info(f"Capability Manager initialized with {len(self.enabled_capabilities)} capabilities")

    def load_capability(self, capability_name: str) -> Optional[Any]:
        """
        Load a specific capability module.
        
        Args:
            capability_name: Name of the capability to load
            
        Returns:
            Loaded capability module or None if not available
        """
        if capability_name not in self.enabled_capabilities:
            logger.debug(f"Capability '{capability_name}' is disabled")
            return None
        
        if capability_name in self.loaded_capabilities:
            return self.loaded_capabilities[capability_name]
        
        try:
            module = importlib.import_module(f"src.{capability_name}")
            self.loaded_capabilities[capability_name] = module
            logger.debug(f"Loaded capability: {capability_name}")
            return module
        except ImportError as e:
            logger.warning(f"Failed to load capability '{capability_name}': {e}")
            return None

    def load_all_capabilities(self) -> Dict[str, Any]:
        """
        Load all enabled capabilities.
        
        Returns:
            Dictionary of loaded capabilities
        """
        for capability in self.enabled_capabilities:
            self.load_capability(capability)
        
        return self.loaded_capabilities

    def get_capability(self, capability_name: str) -> Optional[Any]:
        """
        Get a loaded capability.
        
        Args:
            capability_name: Name of the capability
            
        Returns:
            Capability module or None
        """
        if capability_name not in self.loaded_capabilities:
            return self.load_capability(capability_name)
        return self.loaded_capabilities.get(capability_name)

    def execute_capability(self, capability_name: str, method: str, *args, **kwargs) -> Any:
        """
        Execute a method on a capability.
        
        Args:
            capability_name: Name of the capability
            method: Method name to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Result of the method execution
        """
        capability = self.get_capability(capability_name)
        
        if not capability:
            return {"error": f"Capability '{capability_name}' not available"}
        
        try:
            if hasattr(capability, method):
                return getattr(capability, method)(*args, **kwargs)
            elif hasattr(capability, 'main'):
                if hasattr(capability.main, method):
                    return getattr(capability.main, method)(*args, **kwargs)
            
            return {"error": f"Method '{method}' not found in '{capability_name}'"}
        except Exception as e:
            logger.error(f"Error executing {capability_name}.{method}: {e}")
            return {"error": str(e)}

    def is_capability_enabled(self, capability_name: str) -> bool:
        """Check if a capability is enabled."""
        return capability_name in self.enabled_capabilities

    def is_capability_loaded(self, capability_name: str) -> bool:
        """Check if a capability is loaded."""
        return capability_name in self.loaded_capabilities

    def get_capability_status(self) -> Dict[str, str]:
        """
        Get status of all capabilities.
        
        Returns:
            Dictionary mapping capability names to their status
        """
        status = {}
        for capability in self.CAPABILITIES:
            if capability in self.loaded_capabilities:
                status[capability] = "loaded"
            elif capability in self.enabled_capabilities:
                status[capability] = "available"
            else:
                status[capability] = "disabled"
        return status

    def enable_capability(self, capability_name: str) -> bool:
        """
        Enable a capability.
        
        Args:
            capability_name: Name of the capability to enable
            
        Returns:
            True if successful
        """
        if capability_name in self.CAPABILITIES:
            self.enabled_capabilities.add(capability_name)
            logger.info(f"Enabled capability: {capability_name}")
            return True
        return False

    def disable_capability(self, capability_name: str) -> bool:
        """
        Disable a capability.
        
        Args:
            capability_name: Name of the capability to disable
            
        Returns:
            True if successful
        """
        if capability_name in self.CAPABILITIES:
            self.enabled_capabilities.discard(capability_name)
            self.loaded_capabilities.pop(capability_name, None)
            logger.info(f"Disabled capability: {capability_name}")
            return True
        return False
