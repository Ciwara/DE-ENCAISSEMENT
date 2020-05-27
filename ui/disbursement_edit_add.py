#!usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad


from PyQt4.QtGui import (
    QHBoxLayout, QDialog, QGroupBox, QLineEdit, QTextEdit,
    QFormLayout, QVBoxLayout)
from PyQt4.QtCore import QDate

from models import (Disbursement)
from Common.ui.util import check_is_empty, date_to_datetime
from Common.ui.common import (FWidget, IntLineEdit, ButtonSave, FloatLineEdit,
                              FormLabel, FormatDate)


class EditOrAddDisbursementDialog(QDialog, FWidget):

    def __init__(self, table_p, parent, disbursement, *args, **kwargs):
        # super(EditOrAddDisbursementDialog, self).__init__(parent=parent, *args, **kwargs)
        QDialog.__init__(self, parent, *args, **kwargs)
        title = "DECAISSEMENT"
        self.setWindowTitle(title)
        # self.setFixedWidth(self.parentWidget().width() - 10)
        # self.setFixedHeight(self.parentWidget().height())

        self.table_p = table_p
        self.disbursement = disbursement
        vbox = QHBoxLayout()
        self.decaisement_group_box()
        vbox.addWidget(self.topLeftGroupBox)
        self.setLayout(vbox)

    def decaisement_group_box(self):

        self.topLeftGroupBox = QGroupBox(self.tr("Formulaire Decaissement"))
        self.description_field = QTextEdit(self.disbursement.description if self.disbursement else "")
        self.number_field = IntLineEdit(str(self.disbursement.number) if self.disbursement else "{}".format(Disbursement.select().count() + 1))
        self.number_field.setToolTip(u"Le numéro decaisement")
        self.number_field.setMaximumSize(80, 40)
        if self.disbursement:
            self.number_field.setReadOnly(True)
        self.date_disb_field = FormatDate(self.disbursement.date if self.disbursement else QDate.currentDate())
        self.num_client_field = IntLineEdit(str(self.disbursement.num_client) if self.disbursement else "")
        self.taux_field = FloatLineEdit(str(self.disbursement.taux) if self.disbursement else "")
        self.valeur_field = FloatLineEdit(str(self.disbursement.valeur) if self.disbursement else "")
        self.recever_name_field = QLineEdit(str(self.disbursement.recever_name) if self.disbursement else "")
        self.amount_field = IntLineEdit(str(self.disbursement.amount) if self.disbursement else "")
        self.butt = ButtonSave(u"Enregistrer")
        self.butt.released.connect(self.save)
        formbox1 = QFormLayout()
        formbox1.addRow(FormLabel("N° : *"), self.number_field)
        formbox1.addRow(FormLabel("Designation"), self.description_field)
        formbox1.addRow(FormLabel("Taux"), self.taux_field)
        formbox1.addRow(FormLabel("Valeur"), self.valeur_field)
        formbox = QFormLayout()
        formbox.addRow(FormLabel("Date : *"), self.date_disb_field)
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
        # if check_is_empty(self.taux_field):
        #     return
        # if check_is_empty(self.valeur_field):
        #     return
        if check_is_empty(self.num_client_field):
            return
        if check_is_empty(self.recever_name_field):
            return
        if check_is_empty(self.amount_field):
            return

        if not self.disbursement:
            self.disb = Disbursement()
        self.disbursement.description = str(self.description_field.toPlainText())
        self.disbursement.number = int(self.number_field.text())
        self.disbursement.taux = float(self.taux_field.text().replace(
            ",", ".").replace(" ", "").replace('\xa0', ''))
        self.disbursement.valeur = float(self.valeur_field.text().replace(
            ",", ".").replace(" ", "").replace('\xa0', ''))
        self.disbursement.date = date_to_datetime(str(self.date_disb_field.text()))
        self.disbursement.num_client = str(self.num_client_field.text())
        self.disbursement.recever_name = str(self.recever_name_field.text())
        self.disbursement.amount = int(self.amount_field.text())
        self.disbursement.save()
        self.table_p.refresh_()
        self.close()
