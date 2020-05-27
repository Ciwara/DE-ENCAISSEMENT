#!/usr/bin/env python
# -*- coding= UTF-8 -*-
# Fad

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# setup the empty canvas
from io import FileIO as file
from reportlab.platypus import Flowable
# from Common.pyPdf import PdfFileWriter, PdfFileReader
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
# from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from num2words import num2words
# from configuration import Config
from Common.ui.util import formatted_number
from Common.ui.util import get_temp_filename


class flowable_rect(Flowable):
    def __init__(self, text, text2="", chck=0):
        Flowable.__init__(self)
        self.width = 10
        self.height = 10
        self.text = text
        self.text2 = text2
        self.chck = 0

    def draw(self):
        self.canv.rect(0, 0, self.width, self.height, fill=0)
        self.canv.drawString(13, 0, self.text)
        if self.text2 != "":
            self.canv.rect(0, 15, self.width, self.height, fill=0)
            self.canv.drawString(13, 15, self.text2)


def pdFview(filename, invoice):
    """
        cette views est cree pour la generation du PDF
    """
    styles = getSampleStyleSheet()
    # styleN = styles["BodyText"]
    styleBH = styles["Normal"]
    if not filename:
        filename = get_temp_filename('pdf')

    PDFSOURCE = 'static/encaissement_source.pdf'
    TMP_FILE = 'static/tmp.pdf'

    DEFAULT_FONT_SIZE = 11
    FONT_BOLD = 'Helvetica-Bold'
    FONT = 'Helvetica'

    # FONT = 'Courier-Bold'
    # A simple function to return a leading 0 on any single digit int.
    # PDF en entrée
    input1 = PdfFileReader(file(PDFSOURCE, "rb"))

    # PDF en sortie
    output = PdfFileWriter()
    # Récupération du nombre de pages
    n_pages = input1.getNumPages()
    # Pour chaque page

    y = 750
    x = 40
    recever_name = Paragraph('''{}'''.format(invoice.recever_name), styleBH)
    # number = Paragraph('''<b></b> {}'''.format(, styleBH)
    date_valeur = invoice.date.strftime("%d - %b - %Y")

    for i in range(n_pages):
        # Récupération de la page du doc initial (input1)
        page = input1.getPage(i)
        p = canvas.Canvas(TMP_FILE, pagesize=A4)
        p.setFont(FONT_BOLD, 12)
        p.drawString(x + 300, y - 60, "ENCAISEMENT N° :")
        p.drawString(x + 300, y - 80, "BAMAKO le ")
        p.setFont(FONT, 12)
        p.drawString(x + 420, y - 60, invoice.number)
        p.drawString(x + 380, y - 80, date_valeur)
        # p.drawString(x + 355, y - 30, str(invoice.date.strftime("%d/%m/%Y")))
        rect_usd = flowable_rect("USD")
        rect_euro = flowable_rect("EUROS")
        rect_v_r = flowable_rect("VERSEMENT", "RETRAIT")
        rect_other = flowable_rect("AUTRE")
        ldata = []
        ht = invoice.amount
        amount = str(formatted_number(ht))
        ldata.append(
            ['', rect_usd, rect_euro, rect_v_r, rect_other, 'MONTANT', 'NOM'])
        ldata.append(
            ["MONTANT", "", "", "", "", amount, recever_name])
        ldata.append(["TAUX", "", "", "", "", "", "MONTANT"])
        ldata.append(["VALEUR", "", "", "", "", "", amount])
        row = 0.8
        col = 1
        btable = Table(
            ldata,
            colWidths=[col * inch, 0.8 * inch, col * inch, col * 1.5 * inch,
                       col * inch, 1.1 * inch, col * inch, col * inch],
            rowHeights=[0.5 * inch, row * inch, row * inch, row * inch])
        btable.setStyle(
            TableStyle(
                [("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                 ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                 ('ALIGN', (0, 1), (-1, -1), "RIGHT"),
                 ('BACKGROUND', (0, 0), (-1, 0), colors.white),
                 ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                 ('FONTSIZE', (0, 0), (-1, 0), 14),
                 ('FONTNAME', (0, 0), (-1, -1), FONT_BOLD),
                 # ('BACKGROUND', (1, 1), (1, 1), colors.black),
                 ('ALIGN', (1, 0), (1, -1), 'LEFT')])
        )
        # data_len = len(ldata)
        # for each in range(1, data_len):
        #     if each % 2 == 0:
        #         bg_color = colors.whitesmoke
        #     else:
        #         bg_color = colors.lightgrey
        #     btable.setStyle(TableStyle([('BACKGROUND', (0, each), (-1, each), bg_color)]))

        a_w = 800
        a_h = y - 320

        w, h = btable.wrap(a_w, a_h)
        btable.drawOn(p, 40, a_h)

        ht_en_lettre = num2words(ht, lang='fr')
        y = a_h - 15
        ht_en_lettre1, ht_en_lettre2 = controle_caratere(ht_en_lettre + " franc CFA", 55, 40)
        p.drawString(x, y - 30, "Arrêté la présente facture à la somme de : {}".format(ht_en_lettre1.title()))
        # p.drawString(x + 155, y - 30, (ht_en_lettre1.title()))
        p.drawString(x, y - 45, (ht_en_lettre2))
        y -= 90

        p.drawString(x + 230, y - 20, str(invoice.num_client))
        p.setFont(FONT_BOLD, 12)
        p.drawString(x, y, "Signature Client")
        p.drawString(x + 220, y, "Numéro Client")
        p.drawString(x + 440, y, "Signature")
        p.showPage()
        # Sauvegarde de la page
        p.save()
        # Création du watermark
        watermark = PdfFileReader(file(TMP_FILE, "rb"))
        # Création page_initiale+watermark
        page.mergePage(watermark.getPage(0))
        # Création de la nouvelle page
        output.addPage(page)
    # Nouveau pdf
    file_dest = filename + ".pdf"
    output_stream = file(file_dest, u"wb")
    output.write(output_stream)
    output_stream.close()

    return file_dest


def controle_caratere(lettre, nb_controle, nb_limite):
    """
        cette fonction decoupe une chaine de caratere en fonction
        du nombre de caratere donnée et conduit le reste à la ligne
    """
    lettre = lettre
    if len(lettre) <= nb_controle:
        ch = lettre
        ch2 = u""
        return ch, ch2
    else:
        ch = ch2 = u""
        for n in lettre.split(u" "):
            if len(ch) <= nb_limite:
                ch = ch + u" " + n
            else:
                ch2 = ch2 + u" " + n
        return ch, ch2
