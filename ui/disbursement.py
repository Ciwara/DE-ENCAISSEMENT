#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga


from PyQt4.QtGui import (QVBoxLayout,
                         QMenu, QIcon, QGridLayout, QTableWidgetItem)

from datetime import datetime
from PyQt4.QtCore import Qt
from Common.models import Organization
from models import Disbursement

from export_pdf_decaissement import pdFview
from Common.ui.util import formatted_number, uopen_file
from Common.ui.common import (FWidget, Button, LineEdit)
from Common.ui.table import FTableWidget

from configuration import Config

from ui.disbursement_edit_add import EditOrAddDisbursementDialog


class DisbursementViewWidget(FWidget):

    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DisbursementViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parent = parent
        self.parentWidget().setWindowTitle(
            Organization.get(id=1).name_orga + u" Gestion decaissement")

        vbox = QVBoxLayout(self)
        self.now = datetime.now().strftime(Config.DATEFORMAT)
        self.decaise_table = DecaiseTableWidget(parent=self)

        self.disbursement_btt = Button("&Decaisement")
        self.disbursement_btt.setMaximumHeight(60)
        # self.add_btt.setEnabled(False)
        self.disbursement_btt.clicked.connect(self.add_disbursement)
        self.disbursement_btt.setIcon(QIcon(u"{img_media}{img}".format(
            img_media=Config.img_media, img="in.png")))

        self.search_disb_field = LineEdit()
        self.search_disb_field.textChanged.connect(self.search)
        self.search_disb_field.setPlaceholderText(u"Rechercher.")
        self.search_disb_field.setMaximumHeight(560)

        disbursementbox = QGridLayout()
        disbursementbox.addWidget(self.search_disb_field, 0, 1)
        disbursementbox.addWidget(self.disbursement_btt, 0, 4)
        disbursementbox.setColumnStretch(2, 2)

        vbox.addLayout(disbursementbox)
        vbox.addWidget(self.decaise_table)
        self.setLayout(vbox)

    def search(self):
        self.decaise_table.refresh_(self.search_disb_field.text())

    def add_disbursement(self):
        self.open_dialog(EditOrAddDisbursementDialog, modal=True,
                         disbursement=None, table_p=self.decaise_table)


class DecaiseTableWidget(FTableWidget):

    def __init__(self, parent, *args, **kwargs):

        FTableWidget.__init__(self, parent=parent, *args, **kwargs)

        # self.hheaders = ["", u"Nom de collecte", u"Date debut", "Date fin",
        # u"Total Poids(g)", u"Pirx du gramme", u"Coût", "Status", ""]
        self.hheaders = ["", u"Numéro", "Client Numéro", u"Désignation",
                         "Date d'encaissement", "Montant", ""]
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popup)
        self.parent = parent
        self.sorter = False
        self.stretch_columns = [0, 1, 2, 3, 4, 5]
        self.align_map = {0: 'l', 1: 'l', 2: 'r', 3: 'r', 5: 'r'}
        self.ecart = -15
        self.display_vheaders = False
        self.refresh_()

    def refresh_(self, search=None):
        """ """
        self._reset()
        self.set_data_for(search=search)
        self.refresh()
        self.hideColumn(len(self.hheaders) - 1)

    def set_data_for(self, search=None):
        # print('search: {}'.format(search))
        qs = Disbursement.select().where(
            Disbursement.deleted==False).order_by(Disbursement.created_date.asc())
        if search:
            qs = qs.where(Disbursement.description.contains(search) |
                          Disbursement.num_client.contains(search) |
                          Disbursement.number.contains(search))

        self.data = [("", collect.number, collect.num_client,
                      collect.description, collect.date.strftime("%Y-%m-%d"),
                      collect.amount, collect.id) for collect in qs.iterator()]

    def _item_for_data(self, row, column, data, context=None):

        if column == 0:
            return QTableWidgetItem(
                QIcon(u"{img_media}{img}".format(
                    img_media=Config.img_cmedia, img="pdf.png")), (u"voir"))
        return super(DecaiseTableWidget, self)._item_for_data(row, column,
                                                              data, context)

    def click_item(self, row, column, *args):
        if column == 0:
            pdf_report = pdFview("decaissement", Disbursement.get(id=self.data[row][-1]))
            uopen_file(pdf_report)

    def popup(self, pos):

        # from ui.ligne_edit import EditLigneViewWidget
        from ui.deleteview import DeleteViewWidget

        if (len(self.data) - 1) < self.selectionModel().selection().indexes()[0].row():
            return False
        menu = QMenu()
        editaction = menu.addAction("Modifier cette ligne")
        delaction = menu.addAction("Supprimer cette ligne")
        action = menu.exec_(self.mapToGlobal(pos))
        row = self.selectionModel().selection().indexes()[0].row()
        disbursement = Disbursement.get(id=self.data[row][-1])
        if action == editaction:
            self.parent.open_dialog(EditOrAddDisbursementDialog, modal=True,
                                    disbursement=disbursement, table_p=self)
        if action == delaction:
            self.parent.open_dialog(DeleteViewWidget, modal=True,
                                    table_p=self, obj=disbursement, trash=False)

    def extend_rows(self):
        pass
