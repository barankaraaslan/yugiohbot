import shlex
import subprocess

def shrun(command_str, throw_on_error=True, *run_args, **run_kwargs):
    args = shlex.split(command_str)
    proc = subprocess.run(args, *run_args, **run_kwargs)
    if throw_on_error:
        if proc.returncode != 0:
            raise Exception("'{}' returned {}".format(command_str, proc.returncode))    
    return proc
