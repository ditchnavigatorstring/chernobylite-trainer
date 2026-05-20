import unittest
from unittest.mock import MagicMock, patch
from src.trainer_core import ChernobyliteTrainer

class TestChernobyliteTrainer(unittest.TestCase):
    """Unit tests for the ChernobyliteTrainer class."""

    def setUp(self):
        self.trainer = ChernobyliteTrainer()
        # Mock the memory reader to avoid actual process attachment
        self.trainer.memory = MagicMock()
        self.trainer.memory.attach.return_value = True

    def test_attach_to_game_success(self):
        """Test successful attachment to game process."""
        result = self.trainer.attach_to_game()
        self.assertTrue(result)
        self.trainer.memory.attach.assert_called_once()

    def test_attach_to_game_failure(self):
        """Test failed attachment to game process."""
        self.trainer.memory.attach.return_value = False
        result = self.trainer.attach_to_game()
        self.assertFalse(result)

    def test_toggle_feature_on(self):
        """Test toggling a feature from off to on."""
        self.trainer.features["god_mode"] = False
        result = self.trainer.toggle_feature("god_mode")
        self.assertTrue(result)
        self.assertTrue(self.trainer.features["god_mode"])

    def test_toggle_feature_off(self):
        """Test toggling a feature from on to off."""
        self.trainer.features["infinite_stamina"] = True
        result = self.trainer.toggle_feature("infinite_stamina")
        self.assertFalse(result)
        self.assertFalse(self.trainer.features["infinite_stamina"])

    def test_toggle_invalid_feature(self):
        """Test toggling a non-existent feature returns False."""
        result = self.trainer.toggle_feature("invalid_feature")
        self.assertFalse(result)

    def test_set_feature_valid(self):
        """Test setting a valid feature to a specific state."""
        self.trainer.set_feature("max_resources", True)
        self.assertTrue(self.trainer.features["max_resources"])
        self.trainer.set_feature("max_resources", False)
        self.assertFalse(self.trainer.features["max_resources"])

    def test_set_feature_invalid(self):
        """Test setting an invalid feature does nothing."""
        self.trainer.set_feature("nonexistent", True)
        self.assertNotIn("nonexistent", self.trainer.features)

    def test_start_and_stop(self):
        """Test starting and stopping the trainer loop."""
        self.assertFalse(self.trainer.active)
        self.trainer.start()
        self.assertTrue(self.trainer.active)
        self.assertIsNotNone(self.trainer.thread)
        self.trainer.stop()
        self.assertFalse(self.trainer.active)
        self.assertIsNone(self.trainer.thread)

    def test_cleanup(self):
        """Test cleanup stops thread and detaches memory."""
        self.trainer.start()
        self.trainer.cleanup()
        self.assertFalse(self.trainer.active)
        self.trainer.memory.detach.assert_called_once()

if __name__ == "__main__":
    unittest.main()
