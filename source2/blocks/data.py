from byte_io import ByteIO
from .dummy import Dummy
from .header import InfoBlock
from .binary_keyvalue import BinaryKeyValue
from ..valve_file import ValveFile


class Data(Dummy):
    def __init__(self, valve_file:ValveFile):
        self.valve_file = valve_file
        self.data = {}
        self.info_block = None
    def read(self, reader: ByteIO,block_info:InfoBlock = None):
        self.info_block = block_info
        with reader.save_current_pos():
            fourcc = reader.read_bytes(4)
        if tuple(fourcc) == (0x56, 0x4B, 0x56, 0x03):
            kv = BinaryKeyValue(self.info_block)
            kv.read(reader)
            self.data = kv.kv
        else:
            for struct in self.valve_file.nrto.structs[:1]:
                self.data[struct.name] = struct.read_struct(reader)