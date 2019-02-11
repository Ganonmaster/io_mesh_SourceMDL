import os
from .vtx_data import *
from io_mesh_SourceMDL.utils import case_insensitive_file_resolution


def split(array, n=3):
    return [array[i:i + n] for i in range(0, len(array), n)]


class SourceVtxFile49:
    def __init__(self, path=None, file=None):
        self.final = False
        if path:
            full_path = path + ".dx90.vtx"
            if not os.path.isfile(full_path):
                full_path = case_insensitive_file_resolution(full_path)
                if full_path is None:
                    raise NotImplementedError('VTX file could not be found')

            self.reader = ByteIO(path=full_path)
        elif file:
            self.reader = file
        # print('Reading VTX file')
        self.vtx = SourceVtxFileData()
        self.read_source_vtx_header()
        # self.read_source_vtx_body_parts()

    def read_source_vtx_header(self):
        self.vtx.read(self.reader)

    def test(self):
        v_acc = 0
        i_acc = 0
        t_acc = 0
        for body_part in self.vtx.vtx_body_parts:
            print(body_part)
            for model in body_part.vtx_models:
                print('\t' * 1, model)
                for lod in model.vtx_model_lods:
                    print('\t' * 2, lod)
                    for mesh in lod.vtx_meshes:
                        print('\t' * 3, mesh)
                        for strip_group in mesh.vtx_strip_groups:
                            v_acc += strip_group.vertex_count
                            i_acc += strip_group.index_count
                            t_acc += strip_group.topology_indices_count
                            print('\t' * 4, strip_group)
                            # pprint(split(strip_group.vtx_indexes))
                            topo_shit = split(list(strip_group.topology), 176)
                            print(len(topo_shit))
                            for topo in topo_shit:
                                print(topo)
                            # print(split(topo_shit, 176))
                            # with open('topology.bin', 'wb+') as fp:
                            #     fp.write(strip_group.topology)
                            for strip in strip_group.vtx_strips:
                                print('\t' * 5, strip)
                                # strip.vertex_count
                                if StripHeaderFlags.STRIP_IS_QUADLIST_EXTRA in strip.flags or StripHeaderFlags.STRIP_IS_QUADLIST_REG in strip.flags:
                                    pass

                                # return
        print('total_verts', v_acc)
        print('total_inds', i_acc)
        print('total_topology', t_acc)
