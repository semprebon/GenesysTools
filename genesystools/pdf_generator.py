import sys

from reportlab.platypus import BaseDocTemplate, FrameBreak

from genesys_common import batch_list


class PDFGenerator:
    # Generates the PDF by applying data to the page layout and card layout

    def generate(self, output, data, layout, card):
        doc = BaseDocTemplate(output, pagesize=tuple(layout.page_size),
                              rightMargin=layout.page_margin[0], leftMargin=layout.page_margin[0],
                              topMargin=layout.page_margin[1], bottomMargin=layout.page_margin[1])
        story = []
        for batch in batch_list(data, layout.cards_per_page):
            print("page includes ", [item.get("name") for item in batch])
            doc.addPageTemplates([layout.page_template()])
            for item in batch:
                try:
                    story.extend(card.card_face(item, content_size=layout.content_size()))
                except BaseException as err:
                    print(str(err))
                    raise Exception(f"Error with card {item.get('name')}")
                story.append(FrameBreak())
        doc.build(story)
