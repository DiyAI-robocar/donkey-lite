"""
Functions to simplify working with processes.
"""
import subprocess
import os
import signal
import sys


def run_shell_command(cmd: str, cwd: object=None, timeout: int=15, print_out: bool=False) -> tuple:
    """
    Execute the shell command
    :param cmd: Command string
    :param cwd: Command working directory
    :param timeout: Value of the timeout in seconds
    :param print_out: Value if the print out should be or not
    :return: Tuple of output, error and process id
    """
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out = []
    err = []

    if(print_out):
        while True:
            line = process.stdout.readline().decode('utf8')
            if not line:
                break
            print(line.replace('\n', ''))
            out.append(line)

    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        kill(process.pid)

    for line in process.stdout.readlines():
        out.append(line.decode())

    for line in process.stderr.readlines():
        err.append(line)

    return out, err, process.pid


def kill(process_id: int) -> None:
    """
    Kill the process ID
    :param process_id: ID of the system process
    :return: Void function
    """
    os.kill(process_id, signal.SIGINT)


def eprint(*args, **kwargs) -> None:
    """
    Pint the message
    :param args: ToDo
    :param kwargs: ToDo
    :return: Void function
    """
    print(*args, file=sys.stderr, **kwargs)
