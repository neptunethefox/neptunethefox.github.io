# Author: NeptuneTheFox
# License: MIT
import os, re
from yaml import load
import json
import glob
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


EMOJI_DATA = []
EMOJI_REGEX = r":([a-zA-Z0-9_]+):"
MARKDOWN_TEMPLATE = '<img alt="{}" src="{}" width="24">'

def get_emojis(markdown: str) -> list[str]:
    emojis = re.findall(EMOJI_REGEX, markdown)
    return emojis

def get_emoji_data(emoji_name: str) -> dict[str]:
    for emoji in EMOJI_DATA:
        if emoji["short"] == emoji_name:
            # Found it!
            return emoji
    
    return {}


def replace_emojis(markdown: str, hand_type: str, asset_path: str) -> list[str]:
    emojis = get_emojis(markdown)
    processed_markdown = markdown

    for emoji in emojis:
        data = get_emoji_data(emoji+"")
        if data != {}:
            processed_markdown = processed_markdown.replace(":{}:".format(emoji), MARKDOWN_TEMPLATE.format(data["desc"], "{}{}".format(asset_path, data["src"])))

    return processed_markdown

def render_document(markdown: str, config: dict[str]) -> str:
    parsed = replace_emojis(markdown, config["emoji"]["hand_type"], "/assets/emoji/")
    return parsed
    

if __name__ == "__main__":
    print("[Rendr] Hiya!")
    bigandscarymarkdown = ""
    config = load(open('./rendr.yml'), Loader=Loader)
    EMOJI_DATA = json.load(open(config["assets"]["emoji"]["data_file"]))
    
    markdown_dirs = config["rendr"]["markdown_dirs"]

    for markdown_dir in markdown_dirs:
        files = glob.glob(markdown_dir)

        for file in files:
            print("Processing {}...".format(file))
            content = ""
            with open(file, 'r') as f:
                content = render_document(f.read(), config)
                f.close()

            with open(file, 'w') as f:
                f.write(content)
                f.close()

    print("[Rendr] Done rendering!")
