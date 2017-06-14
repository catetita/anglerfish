#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Tiny Template Engine that Render and Runs native Python."""
# Renamed from Templar to TemplatePython for easy of use.
# Was about to use TemplateString, but will confuse with string.Template


import re

from pathlib import Path


class TemplatePython(str):

    """Tiny Template Engine that Render and Runs native Python."""

    def __init__(self, template):
        """Init the Template class."""
        self.tokens = self.compile(template.strip())

    @classmethod
    def from_file(cls, fl):
        """Load template from file.A str/file-like object supporting read()."""
        return cls(Path(fl).read_text() if isinstance(fl, str) else fl.read())

    def compile(self, t):
        """Parse and Compile all Tokens found on the template string t."""
        tokens = []
        for i, p in enumerate(re.compile("\{\%(.*?)\%\}", re.DOTALL).split(t)):
            if not p or not p.strip():
                continue
            elif i % 2 == 0:
                tokens.append((False, p.replace("{\\%", "{%")))
            else:
                lines = tuple(p.replace("%\\}", "%}").replace(
                    "{{", "spit(").replace("}}", "); ") .splitlines())
                mar = min(len(_) - len(_.lstrip()) for _ in lines if _.strip())
                tmplt = "\n".join(line_of_code[mar:] for line_of_code in lines)
                tokens.append((True, compile(tmplt, f"<tpl {tmplt}>", "exec")))
        return tokens

    def render(__self, __namespace={}, mini=False, **kw):
        """Render template from __namespace dict + **kw added to namespace."""
        html = []
        html_append = html.append  # Optimization.
        __namespace.update(kw, **globals())

        def spit(*args, **kwargs):
            for _ in args:
                html_append(str(_))
            if kwargs:
                for _ in tuple(kwargs.items()):
                    html_append(str(_))

        __namespace["spit"] = spit
        for is_code, value in __self.tokens:
            eval(value, __namespace) if is_code else html_append(value)
        return re.sub('>\s+<', '> <', "".join(html)) if mini else "".join(html)

    __call__ = render  # shorthand
