#!/usr/bin/python3
import subprocess
import os
import sys
import datetime
import time
import psutil

# --- set the time limit below (minutes)
max_balance = 70
# --- set the process name to limit below
apps = ["steam", "dota"] # apps to limit

uselog = "/home/pavel/Documents/limit/uselog.txt"


def find_midnight_before():
    t = time.time()
    date = list(datetime.datetime.fromtimestamp(t).timetuple())
    for i in range(len(date) - 4):
        date[3 + i] = 0
    return time.mktime(tuple(date))

def get_curr_day():
    return list(datetime.datetime.fromtimestamp(time.time()).timetuple())[2]

def reset_balance(max_balance, uselog, curr_day):
    current_balance = max_balance
    file_write = open(uselog, "w+")
    file_write.write(str((current_balance, curr_day)))
    file_write.close()
    return current_balance

def set_balance(new_balance, uselog):
    curr_day = get_curr_day()
    file_write = open(uselog, "w+")
    file_write.write(str((new_balance, curr_day)))
    file_write.close()

def get_pids(apps):
    pids = []
    for i in range(len(apps)):
        try:
            p = str(subprocess.check_output(["pgrep", apps[i]]).decode("utf-8").strip()).split('\n')
            for j in range(len(p)):
                pids.append(p[j])
        except:
            pass
    return pids


if os.stat(uselog).st_size == 0: # if the log is empty (first time run)
    curr_day = get_curr_day()
    current_balance = reset_balance(max_balance, uselog, curr_day)
else:
    file_read = open(uselog, "r+")
    tpl = eval(file_read.read().split('\n')[0])
    current_balance = tpl[0] # get the balance from the log
    day = tpl[1] # get the day the balance was valid
    file_read.close()
    curr_day = get_curr_day()
    if (curr_day != day): #reset if there is another day
        current_balance = reset_balance(max_balance, uselog, curr_day)

prev_midnight = find_midnight_before()

while True:
    time.sleep(60)
    t = time.time()
    # check if the day has changed, to reset the used quantum
    if t >= prev_midnight + 24 * 60 * 60: #if the computer has been running for more than 24 hours
        # reset
        curr_day = get_curr_day()
        current_balance = reset_balance(max_balance, uselog, curr_day)
        prev_midnight = find_midnight_before()
        
    pids = get_pids(apps)

    if len(pids) != 0:
        current_balance -= 1  # when the balance is below zero kill the process
        set_balance(current_balance, uselog)
        if current_balance <= 0:
            for pid in (pids):
                print(pid)
                p = psutil.Process(int(pid))
                p.kill()
                # subprocess.Popen(["kill", pid])

