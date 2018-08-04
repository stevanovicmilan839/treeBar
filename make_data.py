#!/usr/bin/env python
# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os

BASE_DIR = os.path.dirname(__file__)
BWIPP_PATH = os.path.join(BASE_DIR, 'treepoem', 'postscriptbarcode', 'barcode.ps')
BARCODE_TYPES_PATH = os.path.join(BASE_DIR, 'treepoem', 'data.py')


def main():
    print('Loading barcode types from {}'.format(BWIPP_PATH))
    all_barcode_types = load_barcode_types()

    print('Writing out {}'.format(BARCODE_TYPES_PATH))
    write_out_barcode_types(all_barcode_types)

    print('Done')


def load_barcode_types():
    barcode_types = []
    type_code = description = None
    with open(BWIPP_PATH) as fp:
        for line in fp:
            if line.startswith('% --BEGIN ENCODER ') and line.endswith('--\n'):
                type_code = line[:-3].split()[3]
                description = None
            elif line.startswith('% --DESC: '):
                description = line[:-1].split(None, 2)[2]
            elif line.startswith('% --END ENCODER ') and line.endswith('--\n'):
                barcode_types.append((type_code, description))
                type_code = description = None

    return sorted(barcode_types)


def write_out_barcode_types(all_barcode_types):
    with open(BARCODE_TYPES_PATH, 'w') as fp:
        fp.write('# -*- encoding:utf-8 -*-\n')
        fp.write('from __future__ import absolute_import, division, print_function, unicode_literals\n')
        fp.write('\n\n')
        fp.write('class BarcodeType:\n')
        fp.write('    def __init__(self, type_code, description):\n')
        fp.write('        self.type_code = type_code\n')
        fp.write('        self.description = description\n')
        fp.write('\n\n')
        fp.write('# All supported barcode types, extracted from barcode.ps\n')
        fp.write('barcode_types = {\n')
        for tc, d in all_barcode_types:
            fp.write('    {0!r}: BarcodeType({0!r}, {1!r}),\n'.format(tc, tc, d))
        fp.write('}\n')


if __name__ == '__main__':
    main()
