import sys

from reportlab.lib.units import inch

import genesys_common
import item_card
import adversary_card
import card_page_layout
from pdf_generator import PDFGenerator

setting_file = genesys_common.data_filename(sys.argv, default_filename="BadaarSetting")
setting = genesys_common.load_data(setting_file)

if False:
    data_file = genesys_common.data_filename(sys.argv, default_filename="Implements")
    data = genesys_common.load_data(data_file)
    card = item_card.ItemCard()
    layout = card_page_layout.CardPageLayout(
        card_size=[3.99*inch,3.49*inch], page_size=[8.5*inch, 11*inch],
        gutter=0*inch,
        page_margin=0.25*inch)
else:
    data_file = genesys_common.data_filename(sys.argv, default_filename="test_adversaries")
    data = genesys_common.load_data(data_file)
    card = adversary_card.AdversaryCard(setting)
    layout = card_page_layout.CardPageLayout(
        card_size=[3.99*inch,3.49*inch], page_size=[8.5*inch, 11*inch],
        gutter=0*inch,
        page_margin=0.25*inch)

generator = PDFGenerator()

generator.generate("x.pdf", data, layout, card)


