#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Get a random pastel color as string, useful for HTML/CSS styling."""


# This 2 groups have been tested on HTML/CSS with one each other,
# they look pretty good on all combinations, we are not Designers,
# but this is useful for quick templating and boilerplates styling.


import re
from collections import namedtuple
from colorsys import rgb_to_hls, rgb_to_hsv, rgb_to_yiq
from random import choice
from types import MappingProxyType as frozendict


NAMED2HEX = frozendict({
    'aqua': '#00ffff',
    'black': '#000000',
    'blue': '#0000ff',
    'fuchsia': '#ff00ff',
    'green': '#008000',
    'gray': '#808080',
    'lime': '#00ff00',
    'maroon': '#800000',
    'navy': '#000080',
    'olive': '#808000',
    'purple': '#800080',
    'red': '#ff0000',
    'silver': '#c0c0c0',
    'teal': '#008080',
    'white': '#ffffff',
    'yellow': '#ffff00',
    'orange': '#ffa500',
    'aliceblue': '#f0f8ff',
    'antiquewhite': '#faebd7',
    'aqua': '#00ffff',
    'aquamarine': '#7fffd4',
    'azure': '#f0ffff',
    'beige': '#f5f5dc',
    'bisque': '#ffe4c4',
    'black': '#000000',
    'blanchedalmond': '#ffebcd',
    'blue': '#0000ff',
    'blueviolet': '#8a2be2',
    'brown': '#a52a2a',
    'burlywood': '#deb887',
    'cadetblue': '#5f9ea0',
    'chartreuse': '#7fff00',
    'chocolate': '#d2691e',
    'coral': '#ff7f50',
    'cornflowerblue': '#6495ed',
    'cornsilk': '#fff8dc',
    'crimson': '#dc143c',
    'cyan': '#00ffff',
    'darkblue': '#00008b',
    'darkcyan': '#008b8b',
    'darkgoldenrod': '#b8860b',
    'darkgray': '#a9a9a9',
    'darkgrey': '#a9a9a9',
    'darkgreen': '#006400',
    'darkkhaki': '#bdb76b',
    'darkmagenta': '#8b008b',
    'darkolivegreen': '#556b2f',
    'darkorange': '#ff8c00',
    'darkorchid': '#9932cc',
    'darkred': '#8b0000',
    'darksalmon': '#e9967a',
    'darkseagreen': '#8fbc8f',
    'darkslateblue': '#483d8b',
    'darkslategray': '#2f4f4f',
    'darkslategrey': '#2f4f4f',
    'darkturquoise': '#00ced1',
    'darkviolet': '#9400d3',
    'deeppink': '#ff1493',
    'deepskyblue': '#00bfff',
    'dimgray': '#696969',
    'dimgrey': '#696969',
    'dodgerblue': '#1e90ff',
    'firebrick': '#b22222',
    'floralwhite': '#fffaf0',
    'forestgreen': '#228b22',
    'fuchsia': '#ff00ff',
    'gainsboro': '#dcdcdc',
    'ghostwhite': '#f8f8ff',
    'gold': '#ffd700',
    'goldenrod': '#daa520',
    'gray': '#808080',
    'grey': '#808080',
    'green': '#008000',
    'greenyellow': '#adff2f',
    'honeydew': '#f0fff0',
    'hotpink': '#ff69b4',
    'indianred': '#cd5c5c',
    'indigo': '#4b0082',
    'ivory': '#fffff0',
    'khaki': '#f0e68c',
    'lavender': '#e6e6fa',
    'lavenderblush': '#fff0f5',
    'lawngreen': '#7cfc00',
    'lemonchiffon': '#fffacd',
    'lightblue': '#add8e6',
    'lightcoral': '#f08080',
    'lightcyan': '#e0ffff',
    'lightgoldenrodyellow': '#fafad2',
    'lightgray': '#d3d3d3',
    'lightgrey': '#d3d3d3',
    'lightgreen': '#90ee90',
    'lightpink': '#ffb6c1',
    'lightsalmon': '#ffa07a',
    'lightseagreen': '#20b2aa',
    'lightskyblue': '#87cefa',
    'lightslategray': '#778899',
    'lightslategrey': '#778899',
    'lightsteelblue': '#b0c4de',
    'lightyellow': '#ffffe0',
    'lime': '#00ff00',
    'limegreen': '#32cd32',
    'linen': '#faf0e6',
    'magenta': '#ff00ff',
    'maroon': '#800000',
    'mediumaquamarine': '#66cdaa',
    'mediumblue': '#0000cd',
    'mediumorchid': '#ba55d3',
    'mediumpurple': '#9370db',
    'mediumseagreen': '#3cb371',
    'mediumslateblue': '#7b68ee',
    'mediumspringgreen': '#00fa9a',
    'mediumturquoise': '#48d1cc',
    'mediumvioletred': '#c71585',
    'midnightblue': '#191970',
    'mintcream': '#f5fffa',
    'mistyrose': '#ffe4e1',
    'moccasin': '#ffe4b5',
    'navajowhite': '#ffdead',
    'navy': '#000080',
    'oldlace': '#fdf5e6',
    'olive': '#808000',
    'olivedrab': '#6b8e23',
    'orange': '#ffa500',
    'orangered': '#ff4500',
    'orchid': '#da70d6',
    'palegoldenrod': '#eee8aa',
    'palegreen': '#98fb98',
    'paleturquoise': '#afeeee',
    'palevioletred': '#db7093',
    'papayawhip': '#ffefd5',
    'peachpuff': '#ffdab9',
    'per': '#cd853f',
    'pink': '#ffc0cb',
    'plum': '#dda0dd',
    'powderblue': '#b0e0e6',
    'purple': '#800080',
    'red': '#ff0000',
    'rosybrown': '#bc8f8f',
    'royalblue': '#4169e1',
    'saddlebrown': '#8b4513',
    'salmon': '#fa8072',
    'sandybrown': '#f4a460',
    'seagreen': '#2e8b57',
    'seashell': '#fff5ee',
    'sienna': '#a0522d',
    'silver': '#c0c0c0',
    'skyblue': '#87ceeb',
    'slateblue': '#6a5acd',
    'slategray': '#708090',
    'slategrey': '#708090',
    'snow': '#fffafa',
    'springgreen': '#00ff7f',
    'steelblue': '#4682b4',
    'tan': '#d2b48c',
    'teal': '#008080',
    'thistle': '#d8bfd8',
    'tomato': '#ff6347',
    'turquoise': '#40e0d0',
    'violet': '#ee82ee',
    'wheat': '#f5deb3',
    'white': '#ffffff',
    'whitesmoke': '#f5f5f5',
    'yellow': '#ffff00',
    'yellowgreen': '#9acd32',
    'rebeccapurple': '#663399',
})
# HEX2NAMED = frozendict({value: key for key, value in NAMED2HEX.items()})


def hex2rgb(hex_color: str) -> namedtuple:
    s = re.search(r"#([a-f0-9]+)", str(hex_color)[:7].lower()).group(1)
    return namedtuple("RGB", "red green blue")(
        int(s[:2], 16), int(s[2:4], 16), int(s[4:], 16))


def _process_color(colors_tuple: tuple, black_list: list) -> namedtuple:
    if black_list:
        colors_tuple = tuple(set(colors_tuple).difference(set(black_list)))
    color = choice(colors_tuple)
    hexa = NAMED2HEX[color]
    rgb = hex2rgb(hexa)
    hls = rgb_to_hls(rgb.red, rgb.green, rgb.blue)
    hsv = rgb_to_hsv(rgb.red, rgb.green, rgb.blue)
    yiq = rgb_to_yiq(rgb.red, rgb.green, rgb.blue)
    hls = namedtuple("HLS", "h l s")(  # Round bcause default precision is huge
        round(hls[0], 2), round(hls[1], 2), round(hls[2], 2))
    hsv = namedtuple("HSV", "h s v")(
        round(hsv[0], 2), round(hsv[1], 2), round(hsv[2], 2))
    yiq = namedtuple("YIQ", "y i q")(
        round(yiq[0], 2), round(yiq[1], 2), round(yiq[2], 2))
    per = lambda value: int(value * 100 / 255)  # To Percentage, 0~255 > 0~100%
    return namedtuple("PastelColor", "name hex rgb hls hsv yiq css css_prcnt")(
        color, hexa, rgb, hls, hsv, yiq,
        f"rgb({rgb.red},{rgb.green},{rgb.blue})",  # rgb(int, int, int)
        f"rgb({per(rgb.red)}%,{per(rgb.green)}%,{per(rgb.blue)}%)")  # rgb(%,%)


def get_random_pastelight_color(black_list: list=None) -> namedtuple:
    """Get a random pastel light color as string, useful for CSS styling."""
    colors_tuple = (
        'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige',
        'cornsilk', 'floralwhite', 'ghostwhite', 'grey', 'honeydew', 'ivory',
        'lavender', 'lavenderblush', 'lemonchiffon', 'lightcyan',
        'lightgoldenrodyellow', 'lightgrey', 'lightpink', 'lightskyblue',
        'lightyellow', 'linen', 'mint', 'mintcream', 'oldlace', 'papayawhip',
        'peachpuff', 'seashell', 'skyblue', 'snow', 'thistle', 'white')
    return _process_color(colors_tuple, black_list)


def get_random_pasteldark_color(black_list: list=None) -> namedtuple:
    """Get a random dark color as string, useful for CSS styling."""
    colors_tuple = (
        'brown', 'chocolate', 'crimson', 'darkblue', 'darkgoldenrod',
        'darkgray', 'darkgreen', 'darkolivegreen', 'darkorange', 'darkred',
        'darkslateblue', 'darkslategray', 'dimgray', 'dodgerblue',
        'firebrick', 'forestgreen', 'indigo', 'maroon', 'mediumblue',
        'midnightblue', 'navy', 'olive', 'olivedrab', 'royalblue',
        'saddlebrown', 'seagreen', 'sienna', 'slategray', 'teal')
    return _process_color(colors_tuple, black_list)


def get_random_pastel_color(black_list: list=None) -> namedtuple:
    """Get a random dark or light color as string, useful for CSS styling."""
    colors_tuple = (get_random_pastelight_color().name,
                    get_random_pasteldark_color().name)
    return _process_color(colors_tuple, black_list)
