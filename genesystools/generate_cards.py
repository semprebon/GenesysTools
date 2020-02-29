import os.path
import argparse
from os import path
from pathlib import Path
home = str(Path.home())

from reportlab.lib.units import inch

import genesys_common
import card_page_layout
from pdf_generator import PDFGenerator

parser = argparse.ArgumentParser()
parser.add_argument("--type", "-t", choices=['i', 'a', 's'], default="a",
                    help="type of file (i=item, a=adversary, s=spell)")
parser.add_argument("--setting", "-s", default="BadaarSetting", help="setting yaml file")
parser.add_argument("--width", default="2.5", help="width", type=float)
parser.add_argument("--height", default="3.5", help="height", type=float)
parser.add_argument("files", help="input files", nargs="*")
parser.add_argument("--imagedir", "-i", default=path.join(home, "images"))
parser.add_argument("--out", "-o", help="output file", default=None)

args = parser.parse_args()

setting = genesys_common.load_setting(args.setting)
output_base = args.files[0] if args.out is None else args.out
output = path.splitext(output_base)[0] + ".pdf"
card_size = [args.width*inch, args.height*inch]

if args.type == "i":
    import item_card
    data = genesys_common.load_data(args.files)
    card = item_card.ItemCard()
    layout = card_page_layout.CardPageLayout(
        card_size=card_size, page_size=[8.5*inch, 11*inch],
        gutter=0*inch,
        page_margin=0.25*inch)
elif args.type == "a":
    #data_file = genesys_common.data_filename(sys.argv, default_filename="test_adversaries")
    import adversary_card
    data = genesys_common.load_data(args.files)
    card = adversary_card.AdversaryCard(setting, args.imagedir, size=card_size)
    layout = card_page_layout.CardPageLayout(
        #card_size=card_size, page_size=[8.5*inch, 11*inch],
        card_size=card_size, page_size=[11*inch, 8.5*inch],
        gutter=0*inch,
        page_margin=0.25*inch)
elif args.type == "s":
    import spell_card
    data = []
    for datasets in genesys_common.load_data(args.files):
        for name, info in datasets['spells'].items():
            data.append({ **info, **{ "name": name } })
    card = spell_card.SpellCard(setting, size=card_size)
    layout = card_page_layout.CardPageLayout(
        card_size=card_size, page_size=[8.5*inch, 11*inch],
        gutter=0*inch,
        page_margin=0.25*inch)

generator = PDFGenerator()

print("Saving to " + output)
generator.generate(output, data, layout, card)


