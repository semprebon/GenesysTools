from reportlab.lib.units import inch

import card_page_layout

def test_card_init():
    layout = card_page_layout.CardPageLayout(card_size = [2.0*inch,3.0*inch], page_size=[8.0*inch, 11*inch],
                                             page_margin = [0, 0])
    assert layout.counts == [4, 3]
    assert layout.initial_offset == [0.0*inch, 1.0*inch]

def test_card_offset_no_gutter():
    layout = card_page_layout.CardPageLayout(card_size = [2.0*inch,3.0*inch], page_size=[8.0*inch, 11*inch],
                                             page_margin = [0, 0])
    assert layout.counts == [4, 3]
    assert layout.initial_offset == [0.0*inch, 1.0*inch]
    assert layout.offset([0,0]) == [0*inch, 1.0*inch]
    assert layout.offset(col=1,row=2) == [2*inch, 7.0*inch]

def test_card_offset_with_gutter():
    layout = card_page_layout.CardPageLayout(card_size = [2.0*inch,3.0*inch], page_size=[8.0*inch, 11*inch],
                                             page_margin=1*inch, gutter=0.5*inch)
    assert layout.counts == [2, 2]
    assert layout.initial_offset == [1.75*inch, 2.25*inch]
    assert layout.offset([0,0]) == [1.75*inch, 2.25*inch]
    assert layout.offset(col=1,row=1) == [4.25*inch, 5.75*inch]

def test_card_page_layout_page_template():
    layout = card_page_layout.CardPageLayout(card_size = [2.0*inch,3.0*inch], page_size=[8.0*inch, 11*inch],
                                             page_margin=1*inch, gutter=0.5*inch)
    assert layout.initial_offset == [1.75*inch, 2.25*inch]
    assert len(layout.page_template(id="test").frames) == 4
