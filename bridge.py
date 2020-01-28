#!/usr/bin/env python3
import json
import importlib
import inspect
with open('modules.json', 'r') as f:
    modnames = json.load(f)

platforms = [ importlib.import_module(module) for module in modnames ]

def send(user, message):

    frm = inspect.stack()[1]
    sending_platform = inspect.getmodule(frm[0]).__name__
    for platform in platforms:
        if platform.__name__ != sending_platform:
            platform.send(sending_platform, user, message)
