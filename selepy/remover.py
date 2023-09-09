#%%
from time import sleep
import signal
import os
import sys
import psutil
import shutil
from os.path import join, dirname
from threading import Thread
import tempfile

def del_extension_proxy():
    try:
        temp_dir = tempfile.gettempdir()
        subdirectories = [f.name for f in os.scandir(temp_dir) if f.is_dir()]
        for subdir in subdirectories:
            if 'extension_proxy' in subdir:
                try:
                    shutil.rmtree(join(temp_dir, subdir))
                except:
                    pass
    except:
        pass

def waiting_exit(tp_path, ppid):
    try:
        counter = 0
        print('ppid', ppid)
        print('tp_path', tp_path)
        ppid = int(ppid)
        this_pid = os.getpid()
        while True:
            if counter > 5:
                try:
                    Thread(target=del_extension_proxy).start()
                    if 'temp_profiles' in tp_path and os.path.exists(tp_path):
                        ls_tp = os.listdir(tp_path)
                        count = 0
                        for tp in ls_tp:
                            rm_path = join(tp_path, tp)
                            for i in range(10):
                                try:
                                    shutil.rmtree(rm_path)
                                except Exception as e:
                                    if os.path.exists(rm_path) is False:
                                        break
                                    else:
                                        sleep(1)
                                finally:
                                    if os.path.exists(rm_path) is False:
                                        break
                            count+=1
                finally:
                    os.kill(this_pid, signal.SIGTERM) 
            if psutil.pid_exists(ppid) is False:
                counter += 1
            else:
                sleep(.2)
    except:
        pass

waiting_exit(sys.argv[1], sys.argv[2])
