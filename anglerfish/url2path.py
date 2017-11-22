#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Download accelerator with multiple concurrent downloads for 1 file."""


import logging as log
import os
import ssl
import threading
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.request import Request, urlopen

from anglerfish.bytes2human import bytes2human
from anglerfish.make_autochecksum import autochecksum
from anglerfish.seconds2human import datetime2human, now2human, timedelta2human


try:
    from tqdm import tqdm
except ImportError:
    tqdm = None


__all__ = ("url2path", )


def _get_context() -> object:
    """Return a context for the downloaders."""
    _context = ssl.create_default_context()
    _context.check_hostname = False  # Do NOT Check server Hostnames
    _context.verify_mode = ssl.CERT_NONE  # Do NOT Check server SSL Certificate
    return _context


def _download_simple(url: str, data: dict, timeout: int, filename: str) -> str:
    """Download without multiple concurrent downloads for the same file.

    urllib.request.urlretrieve() dont support 'context','timeout' arguments."""
    with urlopen(url, data=data, timeout=timeout, context=_get_context()
                 ) as urly, open(filename, 'wb') as fyle:
        fyle.write(urly.read())
        return filename


def _calculate_ranges(value: int, numsplits: int) -> tuple:
    """Calculate the number of ranges of bytes, return a list of ranges."""
    lst = []
    for i in range(numsplits):
        lst.append('{0}-{1}'.format(
            i if i == 0 else int(round(1 + i * value / (numsplits * 1.0), 0)),
            int(round(1 + i * value / (numsplits * 1.0) +
                      value / (numsplits * 1.0) - 1, 0))))
    return tuple(lst)


def _get_size(url: str, data: dict, timeout: int) -> int:
    """Get the file Size in bytes from a remote URL."""
    with urlopen(url, data=data, timeout=timeout, context=_get_context()) as u:
        size = int(u.headers.get('content-length', 0))
    log.info(f"Download Size: {bytes2human(size)} ({size} Bytes) Download.")
    log.info(f"Full HTTP Headers data:\n{ u.headers }.\n")
    return size


def _download_a_chunk(idx: int, irange: str, dataDict: dict, url: str,
                      data: dict, timeout: int, use_tqdm: bool) -> None:
    """Download a single chunk of binary data from arguments.

    This should print detailed progress to std out as multiple progress bars.
    This runs on multiple async Threads for simultaneous downloads."""
    req = Request(url, headers={'User-Agent': '', 'DNT': 1})
    req.headers['Range'] = f"bytes={ irange }"
    with urlopen(req, data=data, timeout=timeout, context=_get_context()) as u:
        if use_tqdm and tqdm:
            dataDict[idx] = bytes()  # Empty Bytes to fill up with data.
            totalb = int(int(irange.split("-")[1]) - int(irange.split("-")[0]))
            tota = int(totalb / 1_048_576)  # Number of expected iterations.
            with tqdm(total=tota, unit_scale=True, unit="Loop", position=idx,
                      desc=f"Thread {idx}⟿{req.headers['Range']}") as pbar:
                iteration = 0
                while True:
                    buffer = u.read(1_048_576)  # 1 MegaBytes chunks.
                    if not buffer:
                        break
                    else:
                        dataDict[idx] += buffer
                        iteration += 1
                        pbar.update(iteration)
        else:
            print(f"Thread {idx} is downloading {req.headers['Range']}.")
            dataDict[idx] = u.read()


def url2path(url: str, data: dict=None, timeout: int=None, filename: str=None,
             suffix: str=None, name_from_url: bool=False,
             concurrent_downloads: int=5, force_concurrent: bool=False,
             checksum: bool=False, use_tqdm: bool=True) -> Path:
    """Download accelerator with multiple concurrent downloads for 1 file."""
    if not url.lower().startswith(("https:", "http:", "ftps:", "ftp:")):
        return url  # URL is a file path?.
    start_time, dataDict = datetime.now(), {}
    if not filename and bool(name_from_url):  # Get the filename from the URL.
        filename = url.split('/')[-1]
    if not filename:  # Create a temporary file as the filename.
        filename = NamedTemporaryFile(suffix=suffix, prefix="angler_").name
    log.info(f"""Angler download accelerator.\nFrom: {url}.\nTo:   {filename}.
    Time: ~{ datetime2human(start_time).human } ({ start_time }).""")
    sizeInBytes = _get_size(url, data=data, timeout=timeout)
    # if sizeInBytes=0,Resume is not supported by server,use _download_simple()
    # if sizeInBytes < 1 Gigabytes,file is small,use _download_simple()
    if not int(sizeInBytes / 1024 / 1024 / 1024) >= 1 and not force_concurrent:
        log.info("Resume is Not supported by the server or file is too small.")
        filename = _download_simple(url, data=data,
                                    timeout=timeout, filename=filename)
        if checksum and autochecksum:
            log.info(f"Generating Anglers Auto-CheckSum using {autochecksum}.")
            filename = autochecksum(filename, update=True)
        return Path(filename)
    splitBy = concurrent_downloads if concurrent_downloads in range(11) else 10
    ranges = _calculate_ranges(int(sizeInBytes), int(splitBy))
    log.info(f"Using {splitBy} async concurrent downloads for the same file.")
    # multiple concurrent downloads for the same file.
    downloaders = [threading.Thread(
        target=_download_a_chunk, name="angler",
        args=(idx, irange, dataDict, url, data, timeout, use_tqdm), )
                   for idx, irange in enumerate(ranges)]
    for th in downloaders:
        th.start()
    for th in downloaders:
        th.join()
    with open(filename, 'wb') as fh:  # Reassemble file in correct order.
        for _idx, chunk in tuple(sorted(dataDict.items())):
            fh.write(chunk)
    if checksum and autochecksum:
        log.info(f"Generating Anglers Auto-CheckSum using {autochecksum}.")
        filename = autochecksum(filename, update=True)
    # Humanize units.
    fl_size, fl_time = os.path.getsize(filename), datetime.now() - start_time
    size = bytes2human(fl_size)
    time_elapsed = timedelta2human(fl_time)
    time_started = datetime2human(start_time)
    time_finished = now2human()
    # Log some nice info.
    log.info(f"Downloaded:   { len(dataDict) } binary data chunks total.")
    log.info(f"Outputs file: { filename }.")
    log.info(f"Size (human): { size.human } ({ fl_size } Bytes).")
    log.info(f"Time Elapsed: { time_elapsed.human }.")
    log.info(f"Time Started: { time_started.human }.")
    log.info(f"Time Elapsed: { time_finished.human }.")
    log.info(f"Time Timeout: { timeout }.")

    return namedtuple(
        "URL2Path",
        ("path string url chunks size time_elapsed "
         "time_started time_finished ranges data timeout suffix "
         "name_from_url concurrent_downloads force_concurrent checksum")
    )(
        Path(filename), str(filename), url, len(dataDict), size, time_elapsed,
        time_started, time_finished, ranges, data, timeout, suffix,
        name_from_url, concurrent_downloads, force_concurrent, checksum,
    )
