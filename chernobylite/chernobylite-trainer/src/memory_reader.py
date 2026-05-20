import pymem
import pymem.process

class ChernobyliteMemoryReader:
    """Handles reading and writing to the Chernobylite game process memory."""

    def __init__(self):
        self.pm = None
        self.process = None
        self.base_address = None

    def attach(self) -> bool:
        """Attach to the Chernobylite process. Returns True if successful."""
        try:
            self.pm = pymem.Pymem("Chernobylite.exe")
            self.process = pymem.process.module_from_name(self.pm.process_handle, "Chernobylite.exe")
            self.base_address = self.process.lpBaseOfDll
            return True
        except pymem.exception.ProcessNotFound:
            return False

    def read_float(self, offset: int) -> float:
        """Read a float from memory relative to base address."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        addr = self.base_address + offset
        return self.pm.read_float(addr)

    def write_float(self, offset: int, value: float) -> None:
        """Write a float to memory relative to base address."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        addr = self.base_address + offset
        self.pm.write_float(addr, value)

    def read_int(self, offset: int) -> int:
        """Read an integer from memory relative to base address."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        addr = self.base_address + offset
        return self.pm.read_int(addr)

    def write_int(self, offset: int, value: int) -> None:
        """Write an integer to memory relative to base address."""
        if not self.pm:
            raise RuntimeError("Not attached to process")
        addr = self.base_address + offset
        self.pm.write_int(addr, value)

    def detach(self) -> None:
        """Detach from the process."""
        if self.pm:
            self.pm.close_process()
            self.pm = None
            self.process = None
            self.base_address = None
