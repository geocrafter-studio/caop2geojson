# -*- coding: utf-8 -*-

import os
from tqdm import *

def mkgroupdir(rootpath, code):
    if not os.path.exists(os.path.join(rootpath, code)):
        os.makedirs(os.path.join(rootpath, code))


def removefile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


def progressbar(total):
    return tqdm(total=total)
