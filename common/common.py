#!/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import socket
import os
import re
import sys

class Config:
    def __init__(self,cfg_path="./cfg.json"):
        self.__cfg_path=cfg_path
    
    def get_endpoint_name(self):
        ret = socket.gethostname()
        if not os.path.isfile(self.__cfg_path):
            return ret
        cfg = open(self.__cfg_path,"r")
        try:
            content = cfg.read()
            config_obj = json.loads(content)
            ret = config_obj.get("hostname")
            return ret
        except:
            return ret

if __name__ == '__main__':
    config = Config()
    print config.get_endpoint_name()
