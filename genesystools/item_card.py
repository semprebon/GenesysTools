from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, HRFlowable, Table, TableStyle

import genesys_common

# Defines what is appearing on each card.
class ItemCard:

    TYPE_DELIMITER = '/'
    COMMON_FEATURES = ["name", "encumbrance", "description", "type", "rarity", "mp", "price"]

    NORMAL_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=10)
    TITLE_STYLE = ParagraphStyle("title", fontName="Helvetica", fontSize=11, leading=13, textColor=colors.darkblue)
    SECTION_HEADER_STYLE = ParagraphStyle("section_header", fontName="Helvetica", fontSize=9, leading=9, alignment=TA_CENTER)
    RIGHT_ALIGN_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=10, alignment=TA_RIGHT)

    def title(self, item):
        #return [Paragraph(text, self.TITLE_STYLE)]
        table = Table([[Paragraph(item["name"], self.TITLE_STYLE),
                        Paragraph("R" + str(item.get("rarity", "?")), self.NORMAL_STYLE),
                        Paragraph("OOOO"[:(item.get("mp", 0))], self.RIGHT_ALIGN_STYLE)]],
                      colWidths=[2*inch, None, None])
        table.setStyle(TableStyle([
            ('RIGHTPADDING', (0,0),(2,0), 0),
            ('LEFTPADDING',  (0,0),(2,0), 0),
            ('ALIGN', (2,0),(2,0), 'RIGHT')]))
        return [table, self.horizontal_line()]

    def features(self, data):
        return [self.list_item(genesys_common.humanize(key), feature) for key, feature in data.items()]

    def horizontal_line(self):
        return HRFlowable(width="100%", color=colors.black, hAlign="CENTER")

    def list_item(self, name, text):
        return Paragraph("<b>%s</b> %s" % (name, text), self.NORMAL_STYLE)

    def card_face(self, item):
        story = []

        if "name" in item:
            story.extend(self.title(item))
        if "descripion" in item:
            story.append(Paragraph(item["description"], self.NORMAL_STYLE))
        if item.get("type") == None:
            types = []
        else:
            types = item["type"].split(self.TYPE_DELIMITER)

        base_features = { key: value for key, value in item.items() if key not in self.COMMON_FEATURES + types }
        story.extend(self.features(base_features))
        for type in types:
            if len(types) > 1:
                story.append(Paragraph(genesys_common.humanize(type), self.SECTION_HEADER_STYLE))
            story.extend(self.features(item[type]))
        return story
