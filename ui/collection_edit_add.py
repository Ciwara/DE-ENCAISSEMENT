#!usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt4.QtGui import (
    QHBoxLayout, QDialog, QGroupBox, QLineEdit, QTextEdit,
    QFormLayout, QVBoxLayout)
from PyQt4.QtCore import QDate

from models import (Collection)
from Common.ui.util import check_is_empty, date_to_datetime
from Common.ui.common import (FWidget, IntLineEdit, ButtonSave, FloatLineEdit,
                              FormLabel, FormatDate)


class EditOrAddCollectionDialog(QDialog, FWidget):

    def __init__(self, table_p, parent, collection, payment=None, *args, **kwargs):
        # super(EditOrAddCollectionDialog, self).__init__(parent=parent, *args, **kwargs)
        QDialog.__init__(self, parent, *args, **kwargs)
        title = "ENCAISSEMENT"
        self.setWindowTitle("EN-DE {}".format(title))
        # self.setFixedWidth(self.parentWidget().width() - 10)
        # self.setFixedHeight(self.parentWidget().height())
        self.table_p = table_p
        self.collection = collection
        vbox = QHBoxLayout()
        self.encaissement_group_box()
        vbox.addWidget(self.topLeftGroupBox)
        self.setLayout(vbox)

    def encaissement_group_box(self):
        self.topLeftGroupBox = QGroupBox(self.tr("Formulaire Encaissement"))
        self.description_field = QTextEdit(self.collection.description if self.collection else "")
        self.number_field = IntLineEdit(str(self.collection.number) if self.collection else "{}".format(Collection.select().count() + 1))
        self.number_field.setToolTip(u"Le numéro du d'encaissement")
        self.number_field.setMaximumSize(80, 40)
        if self.collection:
            self.number_field.setReadOnly(True)
        self.date_encais_field = FormatDate(self.collection.date if self.collection else QDate.currentDate())
        self.num_client_field = IntLineEdit(str(self.collection.num_client) if self.collection else "")
        self.taux_field = FloatLineEdit(str(self.collection.taux) if self.collection else "")
        self.valeur_field = FloatLineEdit(str(self.collection.valeur) if self.collection else "")
        self.recever_name_field = QLineEdit(str(self.collection.recever_name) if self.collection else "")
        self.amount_field = IntLineEdit(str(self.collection.amount) if self.collection else "")
        self.butt = ButtonSave(u"Enregistrer")
        self.butt.released.connect(self.save)
        formbox1 = QFormLayout()
        formbox1.addRow(FormLabel("N° : *"), self.number_field)
        formbox1.addRow(FormLabel("Designation"), self.description_field)
        formbox1.addRow(FormLabel("Taux"), self.taux_field)
        formbox1.addRow(FormLabel("Valeur"), self.valeur_field)
        formbox = QFormLayout()
        formbox.addRow(FormLabel("Date : *"), self.date_encais_field)
        formbox.addRow(FormLabel("Numéro Client : *"), self.num_client_field)
        formbox.addRow(FormLabel("A l'ordre de : *"), self.recever_name_field)
        formbox.addRow(FormLabel("Montant : *"), self.amount_field)
        formbox.addRow("", self.butt)
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addLayout(formbox1)
        hbox.addLayout(formbox)
        vbox.addLayout(hbox)
        # vbox.addWidget(self.butt)
        self.topLeftGroupBox.setLayout(vbox)

    def save(self):

        ''' add operation '''
        if check_is_empty(self.description_field):
            return
        if check_is_empty(self.number_field):
            return
        if check_is_empty(self.num_client_field):
            return
        if check_is_empty(self.recever_name_field):
            return
        if check_is_empty(self.amount_field):
            return

        if not self.collection:
            self.collection = Collection()
        self.collection.description = str(self.description_field.toPlainText())
        self.collection.number = int(self.number_field.text())
        self.collection.taux = float(self.taux_field.text().replace(",", "."))
        self.collection.valeur = float(self.valeur_field.text().replace(",", "."))
        self.collection.date = date_to_datetime(str(self.date_encais_field.text()))
        self.collection.num_client = str(self.num_client_field.text())
        self.collection.recever_name = str(self.recever_name_field.text())
        self.collection.amount = int(self.amount_field.text())
        self.collection.save()
        self.table_p.refresh_()
        self.close()
