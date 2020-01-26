from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, HRFlowable, Table, TableStyle

import genesys_common

# Defines what is appearing on each card.
class AdversaryCard:

    TYPE_DELIMITER = '/'
    COMMON_FEATURES = ["name", "encumbrance", "description", "type", "rarity", "mp", "price"]

    DARK = "#523213"
    BLACK = "#19110B"
    LIGHT = "#FAECA2"
    MIDTONE = "#BD8C12"
    CONTRAST = "#2F6F67"
    LIGHT_CONTRAST = "#C7D6D5"
    NORMAL_STYLE = ParagraphStyle("normal", fontName="RobotoCondensed", fontSize=9, leading=11,
                                  textColor=DARK, backColor=LIGHT)
    INVERSE_STYLE = ParagraphStyle("normal", fontName="RobotoCondensed", fontSize=9, leading=11,
                                   textColor=DARK)
    CENTERED_STYLE = ParagraphStyle("centered", fontName="RobotoCondensed", fontSize=9, leading=9, alignment=TA_CENTER)
    RIGHT_ALIGN_STYLE = ParagraphStyle("right_align", fontName="RobotoCondensed", fontSize=9, leading=9, alignment=TA_RIGHT)
    LABEL_STYLE = ParagraphStyle("label", fontName="RobotoCondensed", fontSize=8, leading=8, textColor=colors.white, alignment=TA_CENTER)
    SECTION_HEADER_STYLE = ParagraphStyle("section_header", fontName="RobotoCondensed", fontSize=9, leading=9, alignment=TA_CENTER)
    GENESYS_SYMBOLS_STYLE = ParagraphStyle("genesys", fontName="Genesys", fontSize=9, leading=13, alignment=TA_RIGHT)

    def __init__(self, setting):
        self.setting = setting
        genesys_common.register_fonts()

    def power_str(self, name, power):
        symbols = {
            "combat": genesys_common.COMBAT_SYMBOL,
            "social": genesys_common.SOCIAL_SYMBOL,
            "general":genesys_common.GENERAL_SYMBOL}
        return f"{symbols[name]}{power}"

    CELL_DEFAULT_STYLE = {
        'fontName': 'RobotoCondensed', 'fontSize': 9, 'leading': 9,
        'alignment': TA_CENTER, 'space_before': 2 }

    def cell(self, text="", **style):
        style = { **self.CELL_DEFAULT_STYLE, **style }
        return Paragraph(text, ParagraphStyle("cell", **style))

    def divided_texts(self, texts, color=colors.silver, symbol='|'):
        divider = f"<font color='{color}'>{symbol}</font>"
        return divider.join(texts)

    def title(self, data):
        name_style = ParagraphStyle("title", fontName="RobotoCondensed", fontSize=12, leading=12,
                                     spaceBefore=0, spaceAfter=1, textColor=self.CONTRAST)
        power_style = ParagraphStyle("title", fontName="RobotoCondensed", fontSize=8, leading=8,
                                     spaceBefore=0, spaceAfter=1, textColor=self.DARK, alignment=TA_RIGHT)
        powers = data.get("power_levels", { 'combat': '?', 'social': '?', 'general': '?'})
        power_levels = [ self.power_str(k, v) for k, v in powers.items() ]
        table = Table([[
            Paragraph(f"<b>{data['name']}</b>", name_style),
            Paragraph(data["type"] + "<br/>" + self.divided_texts(power_levels, color=self.DARK), power_style)]],
            colWidths=[None,0.69*inch])
        table.setStyle(TableStyle([
            # title
            ('TEXTCOLOR',       (0,0), (0,0), self.CONTRAST),
            ('ALIGN',           (0,0), (0,0), 'LEFT'),
            # power levels
            ('TEXTCOLOR',       (1,0), (1,0), self.DARK),
            ('ALIGN',           (1,0), (1,0), 'RIGHT'),
            # all
            ('RIGHTPADDING',    (0,0), (-1,-1), 0),
            ('LEFTPADDING',     (0,0), (-1,-1), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 0),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 2),
            ('BACKGROUND',      (0,0), (-1,-1), colors.white),
            #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.silver),
            #('BOX', (0, 0), (-1, -1), 0.25, colors.silver),
            ('VALIGN',          (0, 0), (-1, -1), 'TOP')]))
        return table

    def characteristics(self, data):
        table = Table([
            [ data['characteristics'][char] for char in genesys_common.CHARACTERISTICS ],
            [ "%s" % char for char in genesys_common.CHARACTERISTICS ]],
        colWidths=[0.366*inch])
        table.setStyle(TableStyle([
            # values
            ('BACKGROUND',      (0,0), (-1,0), self.LIGHT),
            ('TEXTCOLOR',       (0,0), (-1,0), self.DARK),
            ('FONTSIZE',        (0,0), (-1,0), 9),
            ('LEADING',         (0, 1), (-1, 1), 9),
            # labels
            ('BACKGROUND',      (0,1), (-1,1), self.DARK),
            ('TEXTCOLOR',       (0,1), (-1,1), self.LIGHT),
            ('FONTSIZE',        (0, 1), (-1, 1), 7),
            ('LEADING',         (0, 1), (-1, 1), 8),
            # all
            ('FONT',            (0,0), (-1,-1), "RobotoCondensedBd"),
            ('RIGHTPADDING',    (0,0), (-1,-1), 0),
            ('LEFTPADDING',     (0,0), (-1,-1), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 1),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 1),
            ('ALIGN',           (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',          (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID',       (0,1), (-1,1), 0.25, self.LIGHT),
            #    ('BOX',             (0,0), (-1,-1), 0.25, colors.silver)
        ]))
        return table

    def defenses(self, data):
        table = Table([
            [ "%s" % name for name in ['Soak', 'Wound', 'Melee', 'Ranged'] ],
            [ data.get(value, 0) for value in ['soak_value', 'wound_threshold', 'melee_defense', 'ranged_defense']]],
            colWidths=[0.55*inch])
        table.setStyle(TableStyle([
            # labels
            ('BACKGROUND',      (0,0), (-1,0), self.CONTRAST),
            ('TEXTCOLOR',       (0,0), (-1,0), self.LIGHT),
            ('FONTSIZE',        (0,0), (-1,0), 7),
            ('LEADING',         (0,0), (-1,0), 7),
            # values
            ('BACKGROUND',      (0,1), (-1,1), self.LIGHT),
            ('TEXTCOLOR',       (0,1), (-1,1), self.DARK),
            ('FONTSIZE',        (0,1), (-1,1), 9),
            # all
            ('FONT',            (0,0), (-1,-1), "RobotoCondensedBd"),
            ('RIGHTPADDING',    (0,0), (2,0), 0),
            ('LEFTPADDING',     (0,0), (2,0), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 1),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 1),
            ('ALIGN',           (0,0), (3,1), 'CENTER'),
            ('VALIGN',          (0,0), (3,1), 'MIDDLE'),
            ('INNERGRID',       (0,0), (-1,0), 0.25, self.LIGHT),
            ('INNERGRID',       (1,1), (2, 1), 0.25, self.CONTRAST),
        ]))

        return table

    SYMBOL_CODES = {
        '[BO]': genesys_common.BOOST_SYMBOL,
        '[SB]': genesys_common.SETBACK_SYMBOL,
        '[AB]': genesys_common.ABILITY_SYMBOL,
        '[DI]': genesys_common.DIFFICULTY_SYMBOL,
        '[PR]': genesys_common.PROFICIENCY_SYMBOL,
        '[CH]': genesys_common.CHALLENGE_SYMBOL,

        '[SU]': genesys_common.SUCCESS_SYMBOL,
        '[AD]': genesys_common.ADVANTAGE_SYMBOL,
        '[TR]': genesys_common.TRIUMPH_SYMBOL,
        '[FA]': genesys_common.FAILURE_SYMBOL,
        '[TH]': genesys_common.THREAT_SYMBOL,
        '[DE]': genesys_common.DESPAIR_SYMBOL,
    }
    def translate_symbols(self, s):
        for code, sym  in self.SYMBOL_CODES.items():
            s = s.replace(code, sym)
        return s

    def dice_pool(self, characteristic, skill):
        if skill == None:
            skill = characteristic
        proficiencies = min(skill, characteristic)
        abilities = max(skill, characteristic) - proficiencies
        return "%s%s" % (genesys_common.PROFICIENCY_SYMBOL * proficiencies, genesys_common.ABILITY_SYMBOL * abilities)

    def format_skill(self, name, rank, data, setting):
        skill = setting["skills"].get(name)
        if skill == None:
            raise ValueError(f"Skill {name} not found in setting skills")
        characteristic = skill['characteristic']
        characteristic_rank = data['characteristics'][characteristic]
        pool = self.dice_pool(characteristic_rank, rank)
        rank_str = ("" if rank == None else f"&nbsp;{rank}")
        return f"<font color='{self.CONTRAST}'><b>{name}</b></font>{rank_str}&nbsp;({pool})"

    def label(self, text, color=MIDTONE):
        #return f"<style color='{color}'><b>{text}</b></style>"
        return f"<b>{text}</b>"

    def skills(self, data, setting):
        skills = data['skills']
        if isinstance(skills, list):
            skills = { name: None for name in skills }
        skills_str = "; ".join([ self.format_skill(name, rank, data, setting) for name, rank in skills.items() ])
        return Paragraph(skills_str, self.INVERSE_STYLE)

    def format_ability(self, name, description):
        name_str = f"<font color='{self.CONTRAST}'><b>{name}</b></font>"
        return name_str + "{ {self.translate_symbols(description)}" if description else name_str

    def abilities(self, abilities):
        return Paragraph("; ".join([ self.format_ability(k, v) for k, v in abilities.items() ]), self.INVERSE_STYLE)

    def talents_to_abilities(self, talents):
        return { talent: None for talent in talents }

    def format_spell(self,adversary, spell):
        if not isinstance(spell, dict):
            return ""
        else:
            short_skills = {'Sorcery': 'Sc', 'Thaumaturgy': 'Th', 'Whichcraft': 'Wi'}
            skill = short_skills.get(spell["skill"], spell["skill"])
            details = self.translate_symbols(spell['effect'])
            pool = self.translate_symbols(spell['pool'])
            return f"<font color='{self.CONTRAST}'><b>{spell['name']}</b></font> ({skill}): <b>R</b> {spell['range']} {details}<br/>"

    def format_attack(self,adversary, weapon):
        if not isinstance(weapon, dict):
            return ""
        else:
            short_skills = {'Brawl': 'B', 'Melee (Heavy)': 'M/H', 'Melee (Light)': 'M/L', 'Ranged': 'R'}
            skill = short_skills.get(weapon["skill"], weapon["skill"])
            details = ", ".join(weapon.get("qualities", []))
            crit = weapon.get("crit", 10)
            return f"<font color='{self.CONTRAST}'><b>{weapon['name']}</b></font> ({skill}): <b>Dam</b> {weapon['damage']} <b>Crit</b> {crit} {details}<br/>"

    def attacks(self, adversary):
        return Paragraph("".join([ self.format_attack(adversary, item) for item in adversary["equipment"]]),
                         self.NORMAL_STYLE)

    def horizontal_line(self):
        return HRFlowable(width="100%", color=colors.black, hAlign="CENTER")

    def list_item(self, name, text):
        return Paragraph("<b>%s</b> %s" % (name, text), self.NORMAL_STYLE)

    def format_action(self, action, adversary):
        if action['type'] == 'spell':
            return Paragraph(self.format_spell(adversary, action), self.NORMAL_STYLE)
        elif action['type'] == 'attack':
            return Paragraph(self.format_attack(adversary, action), self.NORMAL_STYLE)
        return None

    def card_face(self, adversary):
        story = []

        if "name" in adversary:
            story.append(self.title(adversary))
        story.append(self.characteristics(adversary))
        story.append(self.defenses(adversary))
        story.append(self.skills(adversary, self.setting))
        features = adversary.get('abilities', {})
        features.update(self.talents_to_abilities(adversary.get('talents', [])))
        if 'equipment' in adversary:
            story.append(self.attacks(adversary))
        if 'actions' in adversary:
            for action in adversary['actions']:
                story.append(self.format_action(action, adversary))
        if not len(features) == 0:
            story.append(self.abilities(features))
        # for type in types:
        #     if len(types) > 1:
        #         story.append(Paragraph(genesys_common.humanize(type), self.SECTION_HEADER_STYLE))
        #     story.extend(self.features(adversary[type]))
        return story
