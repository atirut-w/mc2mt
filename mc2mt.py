from argparse import ArgumentParser, Namespace


def main(args: Namespace) -> int:
    return 0


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="mc2mt",
        description="Convert Minecraft resource packs to Minetest texture packs",
    )

    exit(main(parser.parse_args()))
