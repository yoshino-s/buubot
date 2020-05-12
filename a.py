import time  
import subprocess

def cmd(c, timeout=3):
    c = c.split(' ')
    try:
        p = subprocess.run(c, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=timeout)
        return p.stdout.decode()
    except subprocess.TimeoutExpired as e:
        return e.output.decode() + '\nTimeout'
    except Exception:
        return 'Fail'

print(cmd('ls'))