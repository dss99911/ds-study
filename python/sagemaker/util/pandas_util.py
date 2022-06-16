# todo modify path properly.
# from util.common import *
from common import *


def install_dependency(*dependencies):
    import sys
    import subprocess

    subprocess.check_call([
        sys.executable, "-m", "pip", "install", *dependencies
    ])
