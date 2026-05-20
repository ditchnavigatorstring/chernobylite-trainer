#!/usr/bin/env python3
"""Entry point for the Chernobylite Trainer application."""

import sys
from src.ui import TrainerUI

def main() -> None:
    """Main function to launch the trainer UI."""
    try:
        ui = TrainerUI()
        ui.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
