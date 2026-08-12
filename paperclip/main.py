#!/usr/bin/env python3
"""
Paperclip - Autonomous Computer AI Assistant
=============================================
An advanced autonomous computer AI assistant powered by Gemini AI.
Transforms computers into intelligent, interactive, and self-operating systems.

Usage:
    python main.py                        # Interactive mode
    python main.py --task "..."          # Single task mode
    python main.py --config config.yaml   # Custom config
"""

import argparse
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger

from src.autonomous_execution_engine.main import AutonomousExecutionEngine
from src.model_router.main import ModelRouter


def setup_logging(verbose: bool = False):
    """Configure logging for Paperclip."""
    log_level = "DEBUG" if verbose else "INFO"
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
    )
    logger.add(
        "paperclip.log",
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
    )


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Paperclip - Autonomous Computer AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Start interactive session
  python main.py --task "Open Chrome and search for news"  # Run single task
  python main.py --config custom.yaml              # Use custom config
  python main.py --verbose                         # Enable verbose logging
        """,
    )
    parser.add_argument(
        "--task", "-t",
        type=str,
        help="Single task to execute (exits after completion)",
    )
    parser.add_argument(
        "--config", "-c",
        type=str,
        default="config.yaml",
        help="Configuration file path (default: config.yaml)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging",
    )
    parser.add_argument(
        "--workspace", "-w",
        type=str,
        default=None,
        help="Working directory for the agent",
    )
    return parser.parse_args()


def main():
    """Main entry point for Paperclip."""
    args = parse_args()
    setup_logging(args.verbose)

    logger.info("=" * 60)
    logger.info("Paperclip - Autonomous Computer AI Assistant")
    logger.info("Powered by Gemini 2.5 Flash + Gemini 1.5 Flash")
    logger.info("=" * 60)

    # Set workspace directory
    workspace = args.workspace or os.getcwd()
    logger.info(f"Working directory: {workspace}")

    # Initialize model router
    model_router = ModelRouter()

    # Initialize autonomous execution engine
    engine = AutonomousExecutionEngine(
        model_router=model_router,
        workspace=workspace,
        config_path=args.config
    )

    try:
        if args.task:
            # Single task mode
            logger.info(f"Executing single task: {args.task}")
            result = engine.execute_task(args.task)
            logger.info("Task completed!")
            logger.info(f"Result: {result}")
            print(f"\nPaperclip: {result}\n")
        else:
            # Interactive mode
            logger.info("Starting interactive session (Ctrl+C to exit)")
            print("\n" + "=" * 60)
            print("🤖 Paperclip is ready! Type your instructions below.")
            print("Type 'exit' to quit\n" + "=" * 60 + "\n")
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    if not user_input:
                        continue
                    if user_input.lower() in ["exit", "quit", "bye"]:
                        logger.info("Shutting down Paperclip...")
                        break
                    
                    result = engine.execute_task(user_input)
                    print(f"\nPaperclip: {result}\n")
                    
                except KeyboardInterrupt:
                    logger.info("\nShutting down Paperclip...")
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    print(f"\nPaperclip: I encountered an error: {e}\n")

    except Exception as e:
        logger.exception(f"Failed to start Paperclip: {e}")
        print(f"\n❌ Error starting Paperclip: {e}")
        sys.exit(1)

    logger.info("Paperclip session ended")


if __name__ == "__main__":
    main()
