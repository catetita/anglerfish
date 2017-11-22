#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Tinyslations, smallest possible Translations from Internet with fallback."""


from locale import getdefaultlocale
from urllib import parse, request


try:
    from ujson import loads
except ImportError:
    from json import loads


def tinyslation(strin: str, to: str=getdefaultlocale()[0][:2],
                frm: str="en", fallback_dict: dict={},
                fallback_value: str=None, timeout: int=5) -> str:
    """Translate from internet via API from mymemory.translated.net,legally."""
    if frm.lower() == to.lower():  # 'PLEASE SELECT TWO DISTINCT LANGUAGES'
        raise AttributeError(f"2 different languages required: {frm} == {to}.")
    st = parse.quote(strin)
    api = f"https://mymemory.translated.net/api/get?q={st}&langpair={frm}|{to}"
    req = request.Request(url=api, headers={'User-Agent': '', 'DNT': 1})
    try:
        responze = request.urlopen(req, timeout=timeout).read().decode("utf-8")
        return loads(responze)['responseData']['translatedText']
    except Exception:
        return fallback_dict.get(strin.lower().strip(),
                                 fallback_value if fallback_value else strin)
