import argparse


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Available commands:')
        self.args = None

    def parse(self):
        self.args = self.parser.parse_args()
