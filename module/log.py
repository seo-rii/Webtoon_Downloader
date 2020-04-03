import sys


def log(str, lv=2):
    if lv > 1:
        print(str)
        sys.stdout.flush()
