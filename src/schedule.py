#! /usr/bin/env python
#coding=utf-8
import time, os, sched 
    

schedule = sched.scheduler(time.time, time.sleep) 
    
def perform_command(cmd, inc): 
    schedule.enter(inc, 0, perform_command, (cmd, inc)) 
    os.system(cmd) 
        
def timming_exe(cmd, inc = 60): 
    schedule.enter(inc, 0, perform_command, (cmd, inc)) 
    schedule.run() 
        
    
timming_exe("python fetch_data.py &", 1)