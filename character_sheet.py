import math
import os
import argparse
from os import path

from pyparsing import basestring
from reportlab.lib import colors
from reportlab.lib.colors import black, Color
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame, BaseDocTemplate, Paragraph, HRFlowable, Image, \
    PageBreak, Spacer, Table


def format_modifier(value):
    return str(value) if (value < 0) else "+" + str(value)

def attribute_modifier(value):
    return math.floor((value-10)/2)

def humanize(s):
    return s.replace("_", " ").title()

def batch_list(list, batch_size):
    return [ list[i:i + batch_size] for i in range(0, len(list), batch_size) ]

class CharacterSheet:

    BODY_FONT = "Helvetica"
    MARGIN = 0.15 * inch
    WIDTH, HEIGHT = (10.5*inch, 8.0*inch)
    SIDEBAR_WIDTH = 3.0*inch

    NORMAL_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=10)
    TITLE_STYLE = ParagraphStyle("title", fontName="Helvetica", fontSize=11, leading=13, textColor=colors.darkblue)
    SECTION_HEADER_STYLE = ParagraphStyle("section_header", fontName="Helvetica", fontSize=9, leading=9, alignment=TA_CENTER)
    SIDEBAR_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=11, alignment=TA_RIGHT)
    SIDEBAR_TITLE_STYLE = ParagraphStyle("normal", fontName="Times-Roman", fontSize=9, leading=13, alignment=TA_RIGHT)
    GENESYS_SYMBOLS_STYLE = ParagraphStyle("normal", fontName="Genesys", fontSize=9, leading=13, alignment=TA_RIGHT)

    ATTRIBUTE_CODES = { "AG": "Agility", "BR": "Brawn", "CUN": "Cunning",
                        "INT": "Intellect", "PR": "Presence", "WILL": "Willpower" }

    def register_font_family(self, name):
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        normal = pdfmetrics.registerFont(TTFont("%s" % name, '%s.ttf' % name))
        bold = pdfmetrics.registerFont(TTFont('%sBd' % name, '%s Bold.ttf' % name))
        italic = pdfmetrics.registerFont(TTFont('%sIt' % name, '%s Italic.ttf' % name))
        bold_italic = pdfmetrics.registerFont(TTFont('%sBI' % name, '%s Bold Italic.ttf' %name))
        pdfmetrics.registerFontFamily(name, normal=normal, bold=bold, italic=italic, boldItalic = bold_italic)

    def register_fonts(self):
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        #self.register_font_family('Arial')
        #self.register_font_family('Arial Narrow')
        normal = pdfmetrics.registerFont(TTFont("Arial-Regular", 'Arial.ttf'))
        bold = pdfmetrics.registerFont(TTFont('Arial-Bold', 'Arial Bold.ttf'))
        pdfmetrics.registerFontFamily("Arial", normal=bold, bold=bold, italic=normal, boldItalic=bold)
        genesysFont = pdfmetrics.registerFont(TTFont("genesys", 'genesys.ttf'))


    def prepare_page_fn(self, canvas, doc):
        self.canvas.drawImage()

    def horizontal_line(self):
        return HRFlowable(width="100%", color=black, hAlign="CENTER")

    def title(self, name, archetype, career):
        #return [Paragraph(text, self.TITLE_STYLE)]
        return [Paragraph("<b>%s</b> (%s %s)" % (name, archetype, career), self.TITLE_STYLE), self.horizontal_line()]

    def ability_scores(self, data):
        codes = {"str": "S", "dex": "D", "con": "C", "wis": "W", "int": "I", "cha": "Ch"}
        scores = data["attributes"]
        def format_attribute(code, value):
            return "<b>%s</b><font size='5'>%s</font> (%s)" % (code, value, format_modifier(attribute_modifier(value)))

        text = ' '.join([format_attribute(code, scores[name]) for name, code in codes.items()])
        return Paragraph(text, self.NORMAL_STYLE)

    def senses(self, data):
        other_senses = data["senses"] if "senses" in data else "--"
        return [ self.list_item("Senses", other_senses + "; PP " + str(data["passive_perception"])) ]

    def characteristics(self, data):
        return [
            Paragraph(" ".join([ "%s: %d" % item for item in data["characteristics"].items() ]), self.NORMAL_STYLE),
            self.horizontal_line() ]

    PROFICIENCY_SYMBOL = "\uE90B"
    ABILITY_SYMBOL = "\uE905"

    def format_skill(self, name, rank, characteristic, career_skills):
        proficiencies = min(rank, characteristic)
        abilities = max(rank, characteristic) - proficiencies
        return[ Paragraph("<b>%s</b>" % name, self.NORMAL_STYLE),
          Paragraph("%d" % rank, self.NORMAL_STYLE),
          Paragraph("<font color='#fff201'>%s</font><font color='#02a652'>%s</font>" % (self.PROFICIENCY_SYMBOL * proficiencies, self.ABILITY_SYMBOL * abilities), self.GENESYS_SYMBOLS_STYLE) ]

    def skills(self, data):
        characteristics = data["characteristics"]
        return [
            Table([ self.format_skill(name, int(skill["rank"]), characteristics[skill["characteristic"]], [])
                    for (name, skill) in data["skills"].items() ]) ]

    def list_item(self, name, text):
        return Paragraph("<b>%s</b> %s" % (name, text), self.NORMAL_STYLE)

    def standard_features(self, data):
        features = [ "saves", "skills", "vulnerabilities", "damage_resistances", "damage_immunities",
            "condition_immunities", "languages" ]
        return [ self.list_item(humanize(feature), data[feature]) for feature in features if feature in data ]

    def list_section(self, subtitle, items):
        story = []
        if subtitle is not None:
            story.extend([self.horizontal_line(), Paragraph(subtitle, self.SECTION_HEADER_STYLE), self.horizontal_line()])
        return story + [ self.list_item(item["name"], item["text"]) for item in items ]

    def sidebar(self, data):
        return [
            Paragraph("<b>CR</b> %s" % data["cr"], self.SIDEBAR_TITLE_STYLE),
            Spacer(1,2),
            Paragraph("<b>AC</b> %s" % data["ac"], self.SIDEBAR_STYLE),
            Paragraph("<b>HP</b> %s" % data["hp"], self.SIDEBAR_STYLE),
        ]

    def picture(self, image_path, width, height):
        """scales the image to fill the area but retain its proportions"""
        from reportlab.lib import utils

        if image_path is None:
            image_path = os.path.join(os.path.dirname(__file__), "images/orange_hex.png")

        img = utils.ImageReader(image_path)
        w, h = img.getSize()
        reduction = 0.96
        img_aspect =  h / float(w)
        page_aspect = height / width
        if img_aspect > page_aspect:
            ws, hs = (width * page_aspect / img_aspect, height)
        else:
            ws, hs = (width, height * img_aspect / page_aspect)

        return [Spacer(0, (self.CONTENT_HEIGHT-hs*reduction)/2), Image(image_path, width=ws * reduction, height=hs * reduction)]

    def build_story(self, character_data):
        from reportlab.platypus import FrameBreak
        story = []
        story.extend(self.title(character_data["name"], character_data['archetype']["name"], character_data['career']["name"]))
        story.extend(self.characteristics(character_data))
        story.append(FrameBreak())
        story.extend(self.skills(character_data))
        return story

class Page:

    def __init__(self, width=8.5*inch, height=11*inch, min_margin=0.16*inch):
        self.width = width
        self.height = height
        self.min_margin = min_margin

    @classmethod
    def from_dict(cls, d):
        cls(width=d["width"], height=d["height"], min_margin=d["min_margin"])

class LandscapePage(PageTemplate):

    (PAGE_MARGIN_X, PAGE_MARGIN_Y) = (0.5*inch, 0.5*inch)
    (WIDTH, HEIGHT) = (11*inch, 8.5*inch)
    (CONTENT_WIDTH, CONTENT_HEIGHT) = (WIDTH - 2*PAGE_MARGIN_X, HEIGHT-2*PAGE_MARGIN_Y)

    GUTTER_WIDTH = 0.5 * inch
    LEFT_SIDE_WIDTH = 5*inch
    RIGHT_SIDE_X = LEFT_SIDE_WIDTH + GUTTER_WIDTH
    RIGHT_SIDE_WIDTH = CONTENT_WIDTH - RIGHT_SIDE_X

    def __init__(self, character_sheet):
        self.character_sheet = character_sheet


        leftFrame = Frame(self.PAGE_MARGIN_X, self.PAGE_MARGIN_Y,
                          width = self.LEFT_SIDE_WIDTH, height = self.CONTENT_HEIGHT,
                          id="main")
        rightFrame = Frame(self.RIGHT_SIDE_X, self.PAGE_MARGIN_Y,
                           width = self.LEFT_SIDE_WIDTH, height = self.CONTENT_HEIGHT,
                           showBoundary=False, id="sidebar")
        # pictureFrame = Frame(self.back_offset + character_sheet.CARD_MARGIN, self.content_offset_y,
        #                      character_sheet.CONTENT_WIDTH, character_sheet.CONTENT_HEIGHT, showBoundary=False, id="pictureFrame")

        PageTemplate.__init__(self, id="CharacterFront", frames=[leftFrame, rightFrame])

    def draw_background(self, canvas, imagePath):

        canvas.saveState()
        canvas.drawImage(imagePath, self.PAGE_MARGIN_X, self.PAGE_MARGIN_Y, width=self.CONTENT_WIDTH + 2 * self.bleed,
                         height=self.CARD_HEIGHT + 2 * self.bleed)
        canvas.setFillColor(Color(100, 100, 100, alpha=0.7))
        canvas.rect(self.content_offset_x - self.character_sheet.CONTENT_MARGIN, self.content_offset_y + self.character_sheet.CONTENT_MARGIN,
                    self.PAGE_MARGIN_X + 2 * self.character_sheet.CONTENT_MARGIN,
                    self.character_sheet.CONTENT_HEIGHT + 2 * card.CONTENT_MARGIN,
                    stroke=False, fill=True)

        canvas.restoreState()

class PDFGenerator:
    # Generates the PDF by applying data to the page layout and card layout

    def generate(self, output, data_file, name, page_template_class=LandscapePage, character_sheet=CharacterSheet):
        character_sheet = CharacterSheet()
        character_sheet.register_fonts()
        page_template_class = LandscapePage

        margin = min(page_template_class.PAGE_MARGIN_X, page_template_class.PAGE_MARGIN_Y)
        doc = BaseDocTemplate(output, pagesize=(page_template_class.WIDTH, page_template_class.HEIGHT),
                              rightMargin=margin, leftMargin=margin,
                              topMargin=margin, bottomMargin=margin)
        story = []
        data = self.load_data(data_file, filter)
        #data = self.arrange_images(data)
        page = page_template_class(character_sheet)
        doc.addPageTemplates([page])
        story.extend(character_sheet.build_story(data))
        doc.build(story)

    def resolve_file(self, filename, default_directory=os.getcwd()):
        if path.isfile(filename):
            return filename
        if path.isfile(path.join(default_directory, filename)):
            return path.join(default_directory, filename)

    def load_data(self, yamlfile, data_filter):
        """Read YAML file and return  2-dimensional list containing the data"""

        import yaml

        with open(yamlfile) as file:
            character_data = yaml.safe_load(file)
            if (isinstance(character_data["setting"], basestring)):
                character_data['setting'] = yaml.safeload(self.resolve_file(character_data['setting']))
            return character_data

parser = argparse.ArgumentParser(description="Generate Genesys character sheet PDF")
args = parser.parse_args()

generator = PDFGenerator()
generator.generate("output/test.pdf", "data/brutus.yaml", "data/test.pdf")
