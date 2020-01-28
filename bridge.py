#!/usr/bin/env python3
import json
import importlib
with open('modules.json', 'r') as f:
    modnames = json.load(f)

platforms = [ importlib.import_module(module) for module in modnames ]

def send(sending_platform, user, message):
    for platform in platforms:
        if platform.__name__ != sending_platform:
            platform.send(sending_platform, user, message)
