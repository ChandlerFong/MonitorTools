#!/bin/env python
#-*- coding:utf-8 -*-

import json
import time
import socket
import os
import re
import sys
import commands

class Config:
    def __init__(self,cfg_path="./cfg.json"):
        self.__cfg_path=cfg_path
    
    def get_endpoint_name(self):
        ret = socket.gethostname()
        if not os.path.isfile(self.__cfg_path):
            return ret        
        try:
            cfg = open(self.__cfg_path,"r")
            content = cfg.read()
            config_obj = json.loads(content)
            ret = config_obj.get("hostname")
            return ret
        except:
            return ret
            
class Resource():
    def __init__(self, proc_name):
        config = Config() 
        self.host = config.get_endpoint_name()
        self.proc_name=proc_name
        self.pid = self.get_pid_by_name(proc_name)
        
        
    def get_pid_by_name(self, proc_name):
        pids = commands.getoutput('ps aux|grep %s|grep -v grep|awk \'{print $2}\'' % proc_name).split('\n')
        if len(pids) > 0:
            return pids[0]
        else:
            return -1


    def get_cpu_user(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $14+$16}'"
        return os.popen(cmd).read().strip("\n")

    def get_cpu_sys(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $15+$17}'"
        return os.popen(cmd).read().strip("\n")

    def get_cpu_all(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $14+$15+$16+$17}'"
        return os.popen(cmd).read().strip("\n")

    def get_mem(self):
        cmd="cat /proc/" + str(self.pid)  +  "/status |grep VmRSS |awk '{print $2*1024}'"
        return os.popen(cmd).read().strip("\n")

    def get_swap(self):
        cmd="cat /proc/" + str(self.pid)  +  "/stat |awk '{print $(NF-7)+$(NF-8)}' "
        return os.popen(cmd).read().strip("\n")

    def get_fd(self):
        cmd="cat /proc/" + str(self.pid)  +  "/status |grep FDSize |awk '{print $2}'"
        return os.popen(cmd).read().strip("\n")

    def run(self):
        if not os.path.isdir("/proc/" + str(self.pid)):
            return
        self.resources_d={
            'process.cpu.user':[self.get_cpu_user,'COUNTER'],
            'process.cpu.sys':[self.get_cpu_sys,'COUNTER'],
            'process.cpu.all':[self.get_cpu_all,'COUNTER'],
            'process.mem':[self.get_mem,'GAUGE'],
            'process.swap':[self.get_swap,'GAUGE'],
            'process.fd':[self.get_fd,'GAUGE']
        }

        if not os.path.isdir("/proc/" + str(self.pid)):
            return

        output = []
        for resource in  self.resources_d.keys():
                t = {}
                t['endpoint'] = self.host
                t['timestamp'] = int(time.time())
                t['step'] = 60
                t['counterType'] = self.resources_d[resource][1]
                t['metric'] = resource
                t['value']= self.resources_d[resource][0]()
                t['tags'] = 'pid=%s, name=%s' %(self.pid,self.proc_name)

                output.append(t)

        return output

class Util():
    @staticmethod
    def get_pid_by_name(proc_name):
        pids = commands.getoutput('ps aux|grep %s|grep -v grep|awk \'{print $2}\'' % proc_name).split('\n')
        if len(pids) > 0:
            return pids[0]

if __name__ == '__main__':
    config = Config()
    print config.get_endpoint_name()
    resource = Resource('falcon-agent')
    data = resource.run()
    print data
    
