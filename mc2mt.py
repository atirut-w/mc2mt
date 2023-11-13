import zipfile
from argparse import ArgumentParser, Namespace
from os import path


def main(args: Namespace) -> int:
    if not zipfile.is_zipfile(args.input):
        print("Input is not a zip file")
        return 1

    return 0


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="mc2mt",
        description="Convert Minecraft resource packs to Minetest texture packs",
    )

    parser.add_argument("input", help="Input resource pack")
    parser.add_argument("-o", "--output", help="Output texture pack")

    exit(main(parser.parse_args()))
