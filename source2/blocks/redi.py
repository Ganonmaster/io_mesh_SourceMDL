from typing import List

from .dummy import Dummy
from .header import InfoBlock
from .redi_data import *
from ..valve_file import ValveFile
from ValveFileSystem.byte_io import ByteIO

redi_blocks = [InputDependencies,
               AdditionalInputDependencies,
               ArgumentDependencies,
               SpecialDependencies,
               CustomDependencies,
               AdditionalRelatedFiles,
               ChildResourceList,
               ExtraIntData,
               ExtraFloatData,
               ExtraStringData
               ]


class REDI(Dummy):

    def __init__(self, valve_file: ValveFile):
        self.valve_file = valve_file
        self.blocks = []  # type:List[Dependencies]
        self.info_block = None

    def read(self, reader: ByteIO, block_info: InfoBlock = None):
        self.info_block = block_info
        for redi_block in redi_blocks:
            block = redi_block()
            entry = reader.tell()
            block.offset = reader.read_int32()
            block.size = reader.read_int32()
            with reader.save_current_pos():
                reader.seek(entry + block.offset)
                block.read(reader)
                self.blocks.append(block)
