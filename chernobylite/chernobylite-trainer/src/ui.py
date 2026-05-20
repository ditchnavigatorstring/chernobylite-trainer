import keyboard
from src.trainer_core import ChernobyliteTrainer

class TrainerUI:
    """Simple console-based UI for the Chernobylite Trainer."""

    def __init__(self):
        self.trainer = ChernobyliteTrainer()
        self.running = False
        self.hotkeys = {
            "F1": "god_mode",
            "F2": "infinite_stamina",
            "F3": "max_resources",
            "F4": "unlimited_suit"
        }

    def print_status(self) -> None:
        """Print current cheat status to console."""
        print("\n=== Chernobylite Trainer ===")
        print(f"Attached: {self.trainer.memory.pm is not None}")
        print(f"Active: {self.trainer.active}")
        print("Features:")
        for name, enabled in self.trainer.features.items():
            status = "ON" if enabled else "OFF"
            print(f"  {name}: {status}")
        print("\nHotkeys: F1=God, F2=Stamina, F3=Resources, F4=Suit")
        print("Press ESC to quit.\n")

    def _handle_hotkey(self, hotkey: str) -> None:
        """Handle a hotkey press."""
        if hotkey in self.hotkeys:
            feature = self.hotkeys[hotkey]
            new_state = self.trainer.toggle_feature(feature)
            status = "enabled" if new_state else "disabled"
            print(f"[+] {feature} {status}")

    def run(self) -> None:
        """Main loop for the UI."""
        print("Attempting to attach to Chernobylite.exe...")
        if not self.trainer.attach_to_game():
            print("[-] Failed to attach. Make sure the game is running.")
            return
        print("[+] Attached successfully.")

        self.trainer.start()
        self.running = True
        self.print_status()

        # Register hotkeys
        for hotkey in self.hotkeys.keys():
            keyboard.add_hotkey(hotkey, self._handle_hotkey, args=(hotkey,))

        print("Trainer running. Press ESC to exit.")
        keyboard.wait("esc")

        # Cleanup
        keyboard.unhook_all()
        self.trainer.cleanup()
        print("Trainer stopped.")

    def start_without_hotkeys(self) -> None:
        """Start trainer with manual feature setting (no hotkeys)."""
        print("Attempting to attach to Chernobylite.exe...")
        if not self.trainer.attach_to_game():
            print("[-] Failed to attach.")
            return
        print("[+] Attached.")
        self.trainer.start()
        print("Trainer started. Use set_feature() method programmatically.")
