import json
import os
import zipfile
from argparse import ArgumentParser, Namespace
from os import path


def main(args: Namespace) -> int:
    if not zipfile.is_zipfile(args.input):
        print("Input is not a zip file")
        return 1

    if not args.output:
        args.output = path.splitext(args.input)[0]
    if path.exists(args.output):
        if not args.force:
            print("Output already exists")
            return 1
    else:
        os.mkdir(args.output)

    with zipfile.ZipFile(args.input) as pack:
        with pack.open("pack.mcmeta") as mcmeta:
            try:
                data = json.load(mcmeta)

                with open(path.join(args.output, "texture_pack.conf"), "w") as conf:
                    conf.write(f"title = {path.basename(args.output)}\n")
            except KeyError as e:
                print(f"Malformed `pack.mcmeta`")
                return 1

    return 0


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="mc2mt",
        description="Convert Minecraft resource packs to Minetest texture packs",
    )

    parser.add_argument("input", help="Input resource pack")
    parser.add_argument("-o", "--output", help="Output texture pack")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")

    exit(main(parser.parse_args()))
