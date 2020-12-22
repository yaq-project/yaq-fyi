"""tooling for update-bot to interact with git."""


import json
import os
import pathlib
import subprocess


__here__ = pathlib.Path(__file__).parent


def open_mr(kind, version):
    os.chdir(__here__ / "yaq-fyi")
    # ensure starting on master
    subprocess.check_call(["git", "checkout", "master"])
    subprocess.check_call(["git", "fetch", "--all"])  # pull all remote branches
    # create branch
    try:
        subprocess.check_call(["git", "checkout", "-b", f"bullocky-{kind}-{version}"])
    except subprocess.CalledProcessError:  # branch probably already exists
        return
    # update avpr
    new_avpr = json.loads(subprocess.check_output([f"yaqd-{kind}", "--protocol"]).decode())
    with open(__here__ / "yaq-fyi" / "daemons" / f"{kind}.avpr", "w") as f:
        json.dump(new_avpr, f, indent=4, sort_keys=True)
    try:
        # commit
        subprocess.check_call(["git", "commit", "-am", f"[BOT] update {kind} to version {version}"])
        # push and open merge request
        subprocess.check_call(["git", "push", "--push-option=merge_request.create"])
    except:
        pass
    # return to master
    subprocess.check_call(["git", "checkout", "master"])


def setup():
    os.chdir(__here__)
    subprocess.check_call(["git", "clone", "git@gitlab.com:yaq/yaq-fyi.git"])
