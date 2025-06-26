import os
import sys

from shiva.common.commands import CommandHelper

ch = CommandHelper()
sys.path.append(os.getcwd())
ch.load_common()
ch.load_user()


def main():
    ch.command()


if __name__ == '__main__':
    ch.command()
