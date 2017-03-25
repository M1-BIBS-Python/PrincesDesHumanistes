# coding: utf-8
from __future__ import absolute_import
from __future__ import unicode_literals

import itertools
import functools
import string


def parse_pdb_atom_line(line):

    schema = {
        'serial': (6, 11), 'name': (12, 16), 'altLoc': (16, 17), 'resName': (17, 20),
        'chainID': (21, 22), 'resSeq': (22, 26), 'iCode': (26, 27), 'x': (30, 38),
        'y': (38, 46), 'z': (46, 54),
    }

    # Decode a binary string to a unicode/str object
    decode = lambda s: s.decode('utf-8')

    # callback to be called after the value field  is isolated from the line,
    # either to transtype or to decode a binary string
    callbacks = {
        'serial': int, 'name': decode, 'altLoc': decode, 'resName': decode,
        'chainID': decode, 'resSeq': int, 'iCode': decode, 'x': float,
        'y': float, 'z': float,
    }

    return {
        key: callbacks.get(key)(line[i:j].strip())
            for key,(i,j) in schema.items()
    }
