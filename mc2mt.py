import json
import os
import zipfile
from argparse import ArgumentParser, Namespace
from os import path

from PIL import Image


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

        specials_dir = path.join(args.output, "specials")
        if not path.exists(specials_dir):
            os.mkdir(specials_dir)
        hud_dir = path.join(args.output, "hud")
        if not path.exists(hud_dir):
            os.mkdir(hud_dir)

        rp_textures_dir = "assets/minecraft/textures/"

        # Generate special textures
        with pack.open(path.join(rp_textures_dir, "gui/sprites/hud/heart/container.png")) as heart_gone:
            heart_gone = Image.open(heart_gone)
            heart_gone.save(path.join(specials_dir, "heart_gone.png"))

            with pack.open(path.join(rp_textures_dir, "gui/sprites/hud/heart/full.png")) as heart:
                heart = Image.open(heart)
                heart_gone.paste(heart, (0, 0), heart)
                heart_gone.save(path.join(specials_dir, "heart.png"))
        
        # HUD textures
        with pack.open(path.join(rp_textures_dir, "gui/sprites/hud/hotbar.png")) as hotbar:
            hotbar = Image.open(hotbar)
            hotbar.save(path.join(hud_dir, args.prefix + "hotbar.png"))
        with pack.open(path.join(rp_textures_dir, "gui/sprites/hud/hotbar_selection.png")) as hotbar_selection:
            hotbar_selection = Image.open(hotbar_selection)
            hotbar_selection.save(path.join(hud_dir, args.prefix + "hotbar_selection.png"))

    return 0


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="mc2mt",
        description="Convert Minecraft resource packs to Minetest texture packs",
    )

    parser.add_argument("input", help="Input resource pack")
    parser.add_argument("-o", "--output", help="Output texture pack")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite output")
    parser.add_argument("-p", "--prefix", help="Texture prefix", default="")

    exit(main(parser.parse_args()))
