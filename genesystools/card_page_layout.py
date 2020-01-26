import math

from reportlab.lib.units import inch
from reportlab.platypus import Frame, PageTemplate


class CardPageLayout:
    PAGE_MIN_MARGIN =  0.16 * inch

    def __init__(self, card_size, page_size=[8.5*inch, 11*inch], gutter=0,
                 page_margin=PAGE_MIN_MARGIN, card_margin=0.15*inch):
        self.card_size = card_size
        self.page_size = page_size
        self.gutter = self.to_extents(gutter)
        self.page_margin = self.to_extents(page_margin)
        self.card_margin = card_margin

        (x_offset, columns) = self.fit_cards(page_size[0], card_size[0], self.gutter[0], self.page_margin[0])
        (y_offset, rows) = self.fit_cards(page_size[1], card_size[1], self.gutter[1], self.page_margin[1])
        self.initial_offset = [x_offset, y_offset]
        self.counts = [columns, rows]
        self.cards_per_page = columns * rows

    def to_extents(self, value):
        if isinstance(value, list):
            return value
        elif isinstance(value, tuple):
            return list(value)
        elif isinstance(value, int):
            return [float(value), float(value)]
        elif isinstance(value, float):
            return [value, value]
        else:
            raise ValueError("Value should be list, tuple, or number, was %s", str(value))

    def compute_extents(self, page_extent, card_extent, gutter, bleed):
        max_gutter = page_extent - 2 * (self.PAGE_MIN_MARGIN + bleed) - 2 * card_extent

        if gutter == None:
            gutter = max_gutter

        if gutter > max_gutter:
            raise ValueError("Gutter size exceeds maximum of ", max_gutter)

        return (gutter, (page_extent - (2 * card_extent + gutter)) / 2)

    # compute the number of items that fit into a given extent, and the offset
    def fit_cards(self, page_extent, card_extent, gutter, margin):
        page_extent = page_extent - margin*2
        count = math.floor((page_extent + gutter) / (card_extent + gutter))
        initial_offset = (page_extent - (count * (card_extent + gutter) - gutter)) / 2
        return (margin+initial_offset, count)

    def offset(self, pos=None, col=0, row=0):
        if pos == None:
            pos = [col, row]
        return [ self.initial_offset[i] + (self.card_size[i] + self.gutter[i])*pos[i] for i in [0,1] ]

    def create_frame(self, offset, id=id):
        return Frame(offset[0], offset[1], self.card_size[0], self.card_size[1],
              leftPadding=self.card_margin, rightPadding=self.card_margin,
              topPadding=self.card_margin, bottomPadding=self.card_margin,
              showBoundary=True, id=id)

    # returns a page template with frames laid out for each card
    def page_template(self, id='card', on_page=lambda *args: None):
        frames = []
        for row in range(0, self.counts[1]):
            for col in range(0, self.counts[0]):
                frames.append(
                    self.create_frame(offset=self.offset([col, row]), id="card_%d_%d" % (col,row)))
        return PageTemplate(id="card", frames=frames, onPage=on_page)
