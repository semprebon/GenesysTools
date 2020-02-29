import argparse
from os import path

import genesys_common

def format_spell(spell):
    if not isinstance(spell, dict):
        return ""
    else:
        parts = []
        name = f"<h3>{spell['name']}  (<i>{spell['skill']}</i>)</h3>"
        range = f"<b>Range</b> {spell.get('range', 'engaged')}"
        difficulty = f"<b>difficulty</b> {spell.get('difficulty', '???')}"
        concentration = f"<b>Concentration</b> {spell.get('concentration', None)}"
        effect = f"<p>{genesys_common.translate_symbols(spell.get('effect', '???'))}</p>\n"
        return "\n".join([s for s in [ name, range, difficulty, concentration, effect] if s is not None ])

parser = argparse.ArgumentParser()
parser.add_argument("--type", "-t", choices=['i', 'a', 's'], default="a",
                    help="type of file (i=item, a=adversary, s=spell)")
parser.add_argument("--setting", "-s", default="BadaarSetting", help="setting yaml file")
parser.add_argument("--out", "-o", help="output file", default=None)
parser.add_argument("files", help="input files", nargs="*")

args = parser.parse_args()

setting = genesys_common.load_setting(args.setting)
output_base = "genesys.html" if args.out is None else args.out
output = path.splitext(output_base)[0] + ".html"

data = []
for datasets in genesys_common.load_data(args.files):
    for name, info in datasets['spells'].items():
        data.append({ **info, **{ "name": name } })

with open(output, "w") as f:
    f.write("<html><body>\n")
    f.write(f"<h2>{output_base}</h2>\n")
    for spell_info in data:
        f.write(format_spell(spell_info))
    f.write("</body></html>\n")
