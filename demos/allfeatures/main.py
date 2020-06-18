import argparse
import os
import sys

# Don't need this insude a real package
sys.path.insert(0, ".")
from settings import bootstrap, config

def main():
    # Always bootstrap() as soon as possible
    parser = make_arg_parser()
    cmd_options = parser.parse_args()
    cmd_options.config_file.close()
    custom_options_path = cmd_options.config_file.name
    os.environ["CUSTOM_OPTIONS_FILE"] = custom_options_path
    bootstrap()
    print(config)

def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config-file", type=argparse.FileType(mode="r"),
                        help="Custom configuration file")
    return parser

if __name__ == "__main__":
    main()
