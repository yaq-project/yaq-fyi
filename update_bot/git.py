"""tooling for update-bot to interact with git."""


import json
import os
import pathlib
import subprocess


__here__ = pathlib.Path(__file__).parent


def open_mr(kind, version):
    os.chdir(__here__ / "yaq-fyi")
    # ensure starting on main
    subprocess.check_call(["git", "checkout", "main"])
    subprocess.check_call(["git", "fetch", "--all"])  # pull all remote branches
    # create branch
    branch = f"bullocky-{kind}-{version}"
    try:
        subprocess.check_call(["git", "checkout", "-b", branch])
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
        subprocess.check_call(["git", "push", "--set-upstream", "origin", branch, "--push-option=merge_request.create", "--push-option=merge_request.remove_source_branch"])
    except:
        pass
    # return to main
    subprocess.check_call(["git", "checkout", "main"])


def setup():
    os.chdir(__here__)
    subprocess.check_call(["git", "clone", "git@gitlab.com:yaq/yaq-fyi.git"])
