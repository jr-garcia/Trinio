import os
import sys
from importlib import import_module


def resolve_import(local=False):
    try:
        if local or not import_module('e3d'):
            raise ImportError('')
        else:
            print('Engendro3D is installed.')
    except ImportError:
        if local:
            print('Forcing local copy.')
        else:
            print('Engendro3D not installed. Setting local copy.')
        module_path = os.path.abspath('../Engendro3D')
        if module_path not in sys.path:
            sys.path.append(module_path)

