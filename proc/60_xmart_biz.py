#!/bin/env python
#-*- coding:utf-8 -*-

import json
sys.path.append('plugin/common/')
from common import Resource

def main():
    resource = Resource('xmart-biz-boot')
    data = resource.run()
    print json.dumps(data)

if __name__ == '__main__':
    main()
