#!/usr/bin/env python
# -*- coding: utf-8 -*-
# git update-index --chmod=+x <file>
import os
import sys
import zipfile


def zipdir(filepath, z):
    for root, dirs, files in os.walk(filepath):
        for f in files:
            z.write(os.path.join(root, f))

if __name__ == '__main__':
    zipf = zipfile.ZipFile(sys.argv[1], 'w')
    for path in sys.argv[2:]:
        zipdir(path, zipf)
    zipf.close()