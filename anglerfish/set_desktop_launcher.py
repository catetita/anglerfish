#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Add to autostart or launcher icon on the Desktop."""


import logging as log
import os
import sys

from pathlib import Path


def set_desktop_launcher(app, desktop_file_content, autostart=False):
    """Add to autostart or launcher icon on the Desktop."""
    if not sys.platform.startswith("linux"):
        return  # .desktop files are Linux only AFAIK.
    if not isinstance(str, app) or not isinstance(str, desktop_file_content):
        raise TypeError("app or desktop_file_content are not String Types.")
    app, desktop_file_txt = app.strip().lower(), desktop_file_content.strip()
    if not len(app) or not len(desktop_file_txt):
        raise ValueError("app or desktop_file_content can not be Empty value.")
    # Auto-Start file below.
    config_dir = Path.home() / ".config" / "autostart"
    config_dir.mkdir(parents=True, exist_ok=True)
    fyle = config_dir / app + ".desktop"
    if config_dir.is_dir() and not fyle.is_file():
        if bool(autostart):
            log.info("Writing Auto-Start file: {0} ({0!r}).".format(fyle))
            fyle.write_text(desktop_file_txt, encoding="utf-8")
        fyle.chmod(0o776) if fyle.is_file() else log.debug("chmod: NO.")
    # Desktop Launcher file below.
    apps_dir = Path.home() / ".local" / "share" / "applications"  # paths XDG.
    apps_dir.mkdir(parents=True, exist_ok=True)
    desktop_file = apps_dir / app + ".desktop"
    if apps_dir.is_dir() and not desktop_file.is_file():
        log.info("Writing Launcher file: {0} ({0!r}).".format(desktop_file))
        desktop_file.write_text(desktop_file_txt, encoding="utf-8")
        fyle.chmod(0o776) if fyle.is_file() else log.debug("chmod: NO.")
    return desktop_file
