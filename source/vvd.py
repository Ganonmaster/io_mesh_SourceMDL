import sys
import os
from io_mesh_SourceMDL.byte_io import ByteIO
from .vvd_data import SourceVvdFileData
from io_mesh_SourceMDL.utils import case_insensitive_file_resolution


class SourceVvdFile49:
    def __init__(self, path=None, file=None):
        if path:
            full_path = path + ".vvd"
            if not os.path.isfile(full_path):
                full_path = case_insensitive_file_resolution(full_path)
                if full_path is None:
                    raise NotImplementedError('VVD file could not be found')

            self.reader = ByteIO(path=full_path)
        elif file:
            self.reader = file
        self.file_data = SourceVvdFileData()
        self.file_data.read(self.reader)

    def get_full_path(self, path):
        return path + ".vvd"

    def case_insensitive_file_resolution(self, path):
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if filename.lower() == name.lower():
                    print(os.path.join(root, name))
                    return os.path.join(root, name)

    def test(self):
        for v in self.file_data.vertexes:
            print(v)
