import time
import threading
from src.memory_reader import ChernobyliteMemoryReader

# Memory offsets (example, would need real offsets from reverse engineering)
OFFSET_HEALTH = 0x00A1B2C0
OFFSET_STAMINA = 0x00A1B2C4
OFFSET_RESOURCES = 0x00B3D4E8
OFFSET_SUIT_DURABILITY = 0x00C5D6F0

class ChernobyliteTrainer:
    """Core trainer logic providing cheats for Chernobylite."""

    def __init__(self):
        self.memory = ChernobyliteMemoryReader()
        self.active = False
        self.thread = None
        self.features = {
            "god_mode": False,
            "infinite_stamina": False,
            "max_resources": False,
            "unlimited_suit": False
        }
        self._health_value = 100.0
        self._stamina_value = 100.0
        self._resource_value = 9999
        self._suit_value = 100.0

    def attach_to_game(self) -> bool:
        """Attempt to attach to the Chernobylite process."""
        return self.memory.attach()

    def toggle_feature(self, feature_name: str) -> bool:
        """Toggle a cheat feature on/off. Returns new state."""
        if feature_name not in self.features:
            return False
        self.features[feature_name] = not self.features[feature_name]
        return self.features[feature_name]

    def set_feature(self, feature_name: str, state: bool) -> None:
        """Set a cheat feature to a specific state."""
        if feature_name in self.features:
            self.features[feature_name] = state

    def _apply_cheats_loop(self) -> None:
        """Background loop that continuously applies cheats while active."""
        while self.active:
            try:
                if self.features["god_mode"]:
                    self.memory.write_float(OFFSET_HEALTH, self._health_value)
                if self.features["infinite_stamina"]:
                    self.memory.write_float(OFFSET_STAMINA, self._stamina_value)
                if self.features["max_resources"]:
                    self.memory.write_int(OFFSET_RESOURCES, self._resource_value)
                if self.features["unlimited_suit"]:
                    self.memory.write_float(OFFSET_SUIT_DURABILITY, self._suit_value)
            except Exception:
                pass  # Silently continue if read/write fails
            time.sleep(0.1)

    def start(self) -> None:
        """Start the trainer background thread."""
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self._apply_cheats_loop, daemon=True)
            self.thread.start()

    def stop(self) -> None:
        """Stop the trainer background thread."""
        self.active = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None

    def cleanup(self) -> None:
        """Clean up resources."""
        self.stop()
        self.memory.detach()
