#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga


from PyQt4.QtGui import (QVBoxLayout, QMenu, QIcon, QGridLayout, QTableWidgetItem)

from datetime import datetime
from PyQt4.QtCore import Qt
from Common.models import Organization
from models import Collection

from export_pdf_encaissement import pdFview
from Common.ui.util import formatted_number, is_int, uopen_file
from Common.ui.common import (FWidget, Button, LineEdit)
from Common.ui.table import FTableWidget

from configuration import Config

from ui.collection_edit_add import EditOrAddCollectionDialog


class CollectionViewWidget(FWidget):

    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(CollectionViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parent = parent
        self.parentWidget().setWindowTitle(
            Organization.get(id=1).name_orga + u" Gestion encaissement")

        vbox = QVBoxLayout(self)
        self.now = datetime.now().strftime(Config.DATEFORMAT)
        self.encaise_table = EncaiseTableWidget(parent=self)

        self.collection_btt = Button("&Encaisement")
        self.collection_btt.setMaximumHeight(60)
        self.collection_btt.setIcon(QIcon(u"{img_media}{img}".format(
            img_media=Config.img_media, img="in.png")))
        self.collection_btt.clicked.connect(self.add_encaise)

        self.search_coll_field = LineEdit()
        self.search_coll_field.textChanged.connect(self.search)
        self.search_coll_field.setPlaceholderText(u"& Rechercher.")
        self.search_coll_field.setMaximumHeight(400)

        collectionbox = QGridLayout()
        collectionbox.addWidget(self.search_coll_field, 0, 1)
        collectionbox.addWidget(self.collection_btt, 0, 3)
        collectionbox.setColumnStretch(1, 3)

        vbox.addLayout(collectionbox)
        vbox.addWidget(self.encaise_table)
        self.setLayout(vbox)

    def search(self):
        self.encaise_table.refresh_(self.search_coll_field.text())

    def printer_pdf(self):
        pdf_report = pdFview("encaissement", self.invoice)
        uopen_file(pdf_report)

    def add_encaise(self):
        self.open_dialog(EditOrAddCollectionDialog, modal=True,
                         collection=None, table_p=self.encaise_table)


class EncaiseTableWidget(FTableWidget):

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
        qs = Collection.select().where(
            Collection.deleted==False).order_by(Collection.created_date.asc())
        if search:
            qs = qs.where(Collection.description.contains(search) |
                          Collection.num_client.contains(search) |
                          Collection.number.contains(search))

        self.data = [("", collect.number, collect.num_client,
                      collect.description, collect.date.strftime("%Y-%m-%d"),
                      collect.amount, collect.id) for collect in qs.iterator()]

    def _item_for_data(self, row, column, data, context=None):

        if column == 0:
            return QTableWidgetItem(
                QIcon(u"{img_media}{img}".format(
                    img_media=Config.img_cmedia, img="pdf.png")), (u"voir"))
        return super(EncaiseTableWidget, self)._item_for_data(row, column,
                                                              data, context)

    def click_item(self, row, column, *args):
        if column == 0:
            pdf_report = pdFview("encaissement", Collection.get(id=self.data[row][-1]))
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
        collection = Collection.get(id=self.data[row][-1])
        if action == editaction:
            self.parent.open_dialog(EditOrAddCollectionDialog, modal=True,
                                    collection=collection, table_p=self)
        if action == delaction:
            self.parent.open_dialog(DeleteViewWidget, modal=True,
                                    table_p=self, obj=collection, trash=False)

    def extend_rows(self):
        pass
