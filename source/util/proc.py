"""
Functions to simplify working with processes.
"""
import subprocess
import os
import signal
import sys


def run_shell_command(cmd, cwd=None, timeout=15, print_out=False):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out = []
    err = []

    if(print_out):
        while True:
            line = proc.stdout.readline().decode('utf8')
            if not line:
                break
            print(line.replace('\n', ''))
            out.append(line)

    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        kill(proc.pid)

    for line in proc.stdout.readlines():
        out.append(line.decode())

    for line in proc.stderr.readlines():
        err.append(line)

    return out, err, proc.pid


def kill(proc_id: int) -> None:
    """
    :param proc_id: ID of the system process
    :return: Void function
    """
    os.kill(proc_id, signal.SIGINT)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
