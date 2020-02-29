import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, HRFlowable, Table, TableStyle

import genesys_common

# Defines what is appearing on each card.
class SpellCard:

    TYPE_DELIMITER = '/'
    COMMON_FEATURES = ["name", "difficulty", "description", "spell", "effects"]

    DARK = "#523213"
    BLACK = "#19110B"
    LIGHT = "#FAECA2"
    MIDTONE = "#BD8C12"
    CONTRAST = "#2F6F67"
    LIGHT_CONTRAST = "#C7D6D5"

    SKILL_COLOR = {
        "Sorcery": "#0078bd",
        "Thaumaturgy": "#720085",
#        "Witchcraft": "#a10000",
        "Witchcraft": colors.darkred,
    }

    NORMAL_STYLE = ParagraphStyle("normal", fontName="RobotoCondensed", fontSize=9, leading=11)
    RIGHT_ALIGN_STYLE = ParagraphStyle("normal", fontName="RobotoCondensed", fontSize=10, leading=12, alignment=TA_RIGHT)

    def __init__(self, setting, image_dir=os.getcwd(), size=None):
        self.setting = setting
        self.image_dir = image_dir
        self.size = size
        genesys_common.register_fonts()

    def titlex(self, spell):
        table = Table([["name", "difficulty"]],
                      colWidths=[2*inch, self.size[0]-2*inch])
        table.setStyle(TableStyle([
            # title
            ('TEXTCOLOR',       (0,0), (0,0), colors.lightgrey),
            ('BACKGROUND',      (0,0), (0,0), colors.darkred),
            ('ALIGN',           (0,0), (0,0), 'LEFT'),
            ('FONT', (0, 0), (0, 0), "RobotoCondensedBd"),
            # difficulty dice
            ('TEXTCOLOR', (1, 0), (1, 0), self.DARK),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        return [table]

    def title(self, spell):
        #return [Paragraph(text, self.TITLE_STYLE)]

        #short_skills = {'Sorcery': 'Sc', 'Thaumaturgy': 'Th', 'Wichcraft': 'WC'}
        #skill = short_skills.get(spell["skill"], spell["skill"])
        skill = spell["skill"]

        colWidths = [0.7, 0.3]
        table = Table([[spell["name"], skill]],
                      colWidths=[ w*self.size[0] for w in colWidths])
        table.setStyle(TableStyle([
            # title
            ('ALIGN',           (0,0), (0,0), 'LEFT'),
            ('FONT',            (0,0), (0,0), "RobotoCondensedBd"),
            ('FONTSIZE',        (1,0), (1,0), 11),
            # skill
            ('ALIGN',           (1,0), (1,0), 'RIGHT'),
            ('FONT',            (1,0), (1,0), "RobotoCondensedIt"),
            ('FONTSIZE',        (1,0), (1,0), 7),
            # all
            ('TEXTCOLOR',       (0,0), (-1,-1), colors.white),
            ('RIGHTPADDING',    (0,0), (-1,-1), 2),
            ('LEFTPADDING',     (0,0), (-1,-1), 2),
            ('TOPPADDING',      (0,0), (-1,-1), 2),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 2),
            ('BACKGROUND',      (0,0), (-1,-1), self.SKILL_COLOR[spell['skill']]),
            #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.silver),
            #('BOX', (0, 0), (-1, -1), 0.25, colors.silver),
            ('VALIGN',          (0, 0), (-1, -1), 'TOP')]))
        return [table]

    def databar(self, spell):
        #return [Paragraph(text, self.TITLE_STYLE)]
        difficulty = genesys_common.DIFFICULTY_SYMBOL * spell["difficulty"]

        colWidths = [0.5, 0.5]
        range = spell["range"].capitalize()
        action = spell["action"].capitalize()
        concentration_code = "Concentration" if spell.get("concentration", False) else ""

        table = Table([[action, range],
                       [Paragraph(difficulty, self.NORMAL_STYLE), concentration_code]],
                      colWidths=[w*self.size[0] for w in colWidths])
        table.setStyle(TableStyle([
            # action
            ('TEXTCOLOR',       (0,0), (0,0), self.DARK),
            ('ALIGN',           (0,0), (0,0), 'LEFT'),
            ('FONT',            (0,0), (0,0), "RobotoCondensedBd"),
            ('FONTSIZE',        (0,0), (0,0), 7),

            # range
            ('TEXTCOLOR',       (1,0), (1,0), self.DARK),
            ('ALIGN',           (1,0), (1,0), 'RIGHT'),
            ('FONT',            (1,0), (1,0), "RobotoCondensed"),
            ('FONTSIZE',        (1,0), (1,0), 7),
            # difficulty
            ('TEXTCOLOR',       (0,1), (0,1), self.DARK),
            ('ALIGN',           (0,1), (0,1), 'LEFT'),
            ('FONT',            (0,1), (0,1), "RobotoCondensed"),
            ('FONTSIZE',        (0,1), (0,1), 7),
            # concentration
            ('TEXTCOLOR',       (1,1), (1,1), self.DARK),
            ('ALIGN',           (1,1), (1,1), 'RIGHT'),
            ('FONT',            (1,1), (1,1), "RobotoCondensedBd"),
            ('FONTSIZE',        (1,1), (1,1), 7),
            # all
            ('RIGHTPADDING',    (0,0), (-1,-1), 0),
            ('LEFTPADDING',     (0,0), (-1,-1), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 0),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 0),
            ('BACKGROUND',      (0,0), (-1,-1), colors.white),
            #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.silver),
            #('BOX', (0, 0), (-1, -1), 0.25, colors.silver),
            ('VALIGN',          (0, 0), (-1, -1), 'MIDDLE')]))
        return [table, self.horizontal_line()]

    def horizontal_line(self):
        return HRFlowable(width="100%", color=colors.black, hAlign="CENTER")

    test = False

    def card_face(self, spell, content_size=[]):
        story = []

        self.size = content_size
        story.extend(self.titlex(spell) if self.test else self.title(spell))
        story.extend(self.databar(spell))
        story.append(Paragraph(genesys_common.translate_symbols(spell["effect"]),
                               self.NORMAL_STYLE))
        #self.test = not self.test
        return story
