#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Import a module from file path string."""


import errno
import importlib.util
import logging as log
import os

from pathlib import Path


def path2import(pat: str, name: str=None, ignore_exceptions: bool=False,
                check_namespace: bool=True) -> object:
    """Import a module from file path string.

    This is "as best as it can be" way to load a module from a file path string
    that I can find from the official Python Docs, for Python 3.6+.
    """
    module, pat = None, Path(pat)
    if not pat.is_file():
        if not ignore_exceptions:
            raise ModuleNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), pat.as_posix())
    elif not os.access(pat.as_posix(), os.R_OK):
        if not ignore_exceptions:
            raise PermissionError(pat.as_posix())
    else:
        try:
            name = name or pat.stem
            exists = importlib.util.find_spec(name)
            if check_namespace and name in set(globals().keys()) and exists:
                if not ignore_exceptions:
                    raise ImportWarning(
                        f"Module {name} already exist on the Global namespace")
            else:
                spec = importlib.util.spec_from_file_location(name,
                                                              pat.as_posix())
                if spec is None:
                    if not ignore_exceptions:
                        raise ImportError(f"Failed to load {name} from {pat}.")
                module = spec.loader.load_module()
        except Exception as error:
            log.warning(f"Failed to load the module {name} from {pat}.")
            log.warning(error)
            if not ignore_exceptions:
                raise
            module = None
        else:
            log.debug(f"Loading the module {name} from {pat} ({pat!r}).")
    return module
