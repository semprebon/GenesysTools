import sys
import argparse

from reportlab.lib.units import inch

import genesys_common
import card_page_layout
from pdf_generator import PDFGenerator

parser = argparse.ArgumentParser()
parser.add_argument("--type", "-t", choices=['i', 'a'], default="a",
                    help="type of file (i=item, a=adversary)")
parser.add_argument("--setting", "-s", default="BadaarSetting", help="setting yaml file")
parser.add_argument("files", help="input files", nargs="*")
args = parser.parse_args()

setting = genesys_common.load_setting(args.setting)


if args.type == "i":
    import item_card
    data = genesys_common.load_data(args.files)
    card = item_card.ItemCard()
    layout = card_page_layout.CardPageLayout(
        card_size=[2.49*inch,3.49*inch], page_size=[8.5*inch, 11*inch],
        gutter=0*inch,
        page_margin=0.25*inch)
elif args.type == "a":
    #data_file = genesys_common.data_filename(sys.argv, default_filename="test_adversaries")
    import adversary_card
    data = genesys_common.load_data(args.files)
    card = adversary_card.AdversaryCard(setting)
    layout = card_page_layout.CardPageLayout(
        card_size=[2.49*inch,3.49*inch], page_size=[8.5*inch, 11*inch],
        gutter=0*inch,
        page_margin=0.25*inch)

generator = PDFGenerator()

generator.generate("x.pdf", data, layout, card)


