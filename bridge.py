#!/usr/bin/env python3
import json
import importlib
import inspect
from multiprocessing import Process
with open('modules.json', 'r') as f:
    modnames = json.load(f)


platforms = [ importlib.import_module(module) for module in modnames ]
def send(user, message, action = False):

    frm = inspect.stack()[1]
    sending_platform = inspect.getmodule(frm[0]).__name__
    for platform in platforms:
        if platform.__name__ != sending_platform:
            platform.send(sending_platform, user, message, action)
if __name__ == '__main__':

    for platform in platforms:
        Process(target=platform.main, args=()).start()
