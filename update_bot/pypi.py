"""Install yaq daemon using Python."""


import subprocess
import sys


def install(url, kind):
    url = url.strip("/")
    package_name = url.rsplit('/', 1)[-1]
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", package_name])
    version = subprocess.check_output([f"yaqd-{kind}", "--version"]).decode()
    version = version.split("\n")[0]
    version = version.split()[-1]
    return version
