from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, HRFlowable, Table, TableStyle

import genesys_common

# Defines what is appearing on each card.
class AdversaryCard:

    TYPE_DELIMITER = '/'
    COMMON_FEATURES = ["name", "encumbrance", "description", "type", "rarity", "mp", "price"]

    NORMAL_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=10)
    TITLE_STYLE = ParagraphStyle("title", fontName="Helvetica", fontSize=11, leading=13, textColor=colors.darkblue)
    SECTION_HEADER_STYLE = ParagraphStyle("section_header", fontName="Helvetica", fontSize=9, leading=9, alignment=TA_CENTER)
    RIGHT_ALIGN_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=10, alignment=TA_RIGHT)
    SKILL_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=10)
    GENESYS_SYMBOLS_STYLE = ParagraphStyle("normal", fontName="Genesys", fontSize=9, leading=13, alignment=TA_RIGHT)

    PROFICIENCY_SYMBOL = "k"
    ABILITY_SYMBOL = "l"

    def __init__(self, setting):
        self.setting = setting
        genesys_common.register_fonts()

    def title(self, data):
        return [Paragraph(data["name"], self.TITLE_STYLE), self.horizontal_line()]

    def characteristics(self, data):
        table = Table([
            [ data['characteristics'][char] for char in genesys_common.CHARACTERISTICS ],
            genesys_common.CHARACTERISTICS ])
        table.setStyle(TableStyle([
            ('RIGHTPADDING', (0,0),(2,0), 0),
            ('LEFTPADDING',  (0,0),(2,0), 0),
            ('ALIGN', (0,0),(5,1), 'CENTER')]))
        return table

    def defenses(self, data):
        table = Table([
            [ data[value] for value in ['soak_value', 'wound_threshold', 'melee_defense', 'ranged_defense'] ],
            [ 'Soak Value', 'Wound Threshold', 'Melee', 'Ranged'] ])
        table.setStyle(TableStyle([
            ('RIGHTPADDING', (0,0),(2,0), 0),
            ('LEFTPADDING',  (0,0),(2,0), 0),
            ('ALIGN', (0,0),(3,1), 'CENTER')]))
        return table

    def format_skill(self, name, rank, data, setting):
        characteristic = setting["skills"][name]['characteristic']
        characteristic_rank = data['characteristics'][characteristic]
        proficiencies = min(rank, characteristic_rank)
        abilities = max(rank, characteristic_rank) - proficiencies
        return Paragraph(name + (": %d =>        " % rank) +
                ("<font name='Genesys'><font color='#fff201'>%s</font><font color='#02a652'>%s</font></font>"
                    % (self.PROFICIENCY_SYMBOL * proficiencies, self.ABILITY_SYMBOL * abilities)),
            self.SKILL_STYLE)

    def skills(self, data, setting):

        if data["type"] == "minion":
            skills = [ self.format_skill(name, 0, data, setting) for name in data['skills'] ]
        else:
            skills = [ self.format_skill(name, rank, data, setting) for name, rank in data['skills'] ]
        return skills


    def features(self, data):
        return [self.list_item(genesys_common.humanize(key), feature) for key, feature in data.items()]

    def horizontal_line(self):
        return HRFlowable(width="100%", color=colors.black, hAlign="CENTER")

    def list_item(self, name, text):
        return Paragraph("<b>%s</b> %s" % (name, text), self.NORMAL_STYLE)

    def card_face(self, adversary):
        story = []

        if "name" in adversary:
            story.extend(self.title(adversary))
        story.append(self.characteristics(adversary))
        story.append(self.defenses(adversary))
        story.extend(self.skills(adversary, self.setting))
        # if "descripion" in adversary:
        #     story.append(Paragraph(adversary["description"], self.NORMAL_STYLE))
        # if adversary.get("type") == None:
        #     types = []
        # else:
        #     types = adversary["type"].split(self.TYPE_DELIMITER)
        #
        # base_features = {key: value for key, value in adversary.items() if key not in self.COMMON_FEATURES + types}
        # story.extend(self.features(base_features))
        # for type in types:
        #     if len(types) > 1:
        #         story.append(Paragraph(genesys_common.humanize(type), self.SECTION_HEADER_STYLE))
        #     story.extend(self.features(adversary[type]))
        return story
