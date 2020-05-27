#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from datetime import datetime

from peewee import (DateTimeField, IntegerField, CharField, FloatField,
                    BooleanField, ForeignKeyField, TextField)
from Common.models import BaseModel, FileJoin, Owner

FDATE = u"%c"
NOW = datetime.now()


class ProviderOrClient(BaseModel):

    """ Represents the company emmiting the invoices
    """
    # class Meta:
    #     order_by = ('name',)

    CLT = 'Client'
    FSEUR = 'Fournisseur'
    TYPES = [CLT, FSEUR]

    name = CharField(unique=True, verbose_name=("Nom de votre entreprise"))
    address = TextField(
        null=True, verbose_name=("Adresse principale de votre société"))
    phone = CharField(
        verbose_name=("Numero de téléphone de votre entreprise"), default="")
    email = CharField(
        null=True, verbose_name=("Adresse électronique de votre entreprise"))
    legal_infos = TextField(
        null=True, verbose_name=("Informations légales"))
    type_ = CharField(max_length=30, choices=TYPES, default=CLT)
    picture = ForeignKeyField(
        FileJoin, null=True, related_name='file_joins_pictures',
        verbose_name=("image de la societe"))

    # def invoices(self):
    #     return Invoice.select().where(Invoice.client == self)

    # def buys(self):
    #     return Buy.select().where(Buy.provd_or_clt == self)

    # def invoices_items(self):
    #     return Report.select().where(Report.type_ == Report.S,
    #                                  Report.invoice.client == self)

    def is_indebted(self):
        flag = False
        if self.last_remaining() > 0:
            flag = True
        return flag

    # def last_refund(self):
    #     try:
    #         return Refund.select().where(Refund.provider_client == self).order_by(
    #             Refund.date.desc()).get()
    #     except Exception as e:
    #         return None

    def last_remaining(self):
        last_r = self.last_refund()
        return last_r.remaining if last_r else 0

    def __str__(self):
        return u"{}, {}".format(self.name, self.phone)

    def __unicode__(self):
        return self.__str__()

    @classmethod
    def get_or_create(cls, name, phone, typ):
        try:
            ctct = cls.get(name=name, phone=phone, type_=typ)
        except cls.DoesNotExist:
            ctct = cls.create(name=name, phone=phone, type_=typ)
        return ctct


class Disbursement(BaseModel):

    created_date = DateTimeField(verbose_name=("Date"), default=NOW)
    owner = ForeignKeyField(Owner, verbose_name=("Utilisateur"))
    # provider_clt = ForeignKeyField(ProviderOrClient)
    created_date = DateTimeField(verbose_name=("Date"), default=NOW)
    taux = FloatField(verbose_name=("Date"))
    valeur = FloatField(verbose_name=("Valeur"))
    description = CharField()
    number = CharField()
    date = DateTimeField(verbose_name=("Date decaissement"))
    num_client = CharField(default=0)
    recever_name = CharField()
    amount = IntegerField(default=0)
    registered_on = datetime.now()
    deleted = BooleanField(default=False)

    def __unicode__(self):
        return "{}{}".format(self.num_client, self.amount)

    def __str__(self):
        return self.__unicode__()

    def display_name(self):
        return self.__unicode__()

    def save(self):
        """
        Calcul du cost en stock après une operation."""
        self.owner = Owner.get(Owner.islog == True)

        super(Disbursement, self).save()


class Collection(BaseModel):

    """ docstring for Payment """

    USD = "U"
    EUR = "E"
    VER = "V"
    RET = "R"
    AUT = "A"
    TYPES = ((USD, "USD"), (EUR, "EUROS"),
             (VER, "VERSEMENT"), (RET, "RETRAIT"), (AUT, "AUTRES"))

    class Meta:
        order_by = ('date',)

    owner = ForeignKeyField(Owner, verbose_name=("Utilisateur"))
    # provider_clt = ForeignKeyField(ProviderOrClient)
    created_date = DateTimeField(verbose_name=("Date"), default=NOW)
    type_ = CharField(choices=TYPES, default=AUT)
    taux = FloatField(verbose_name=("Date"))
    valeur = FloatField(verbose_name=("Valeur"))
    description = CharField()
    number = CharField()
    date = DateTimeField(verbose_name=("Date Encaissement"))
    num_client = CharField(default=0)
    recever_name = CharField()
    amount = IntegerField(default=0)
    registered_on = datetime.now()
    deleted = BooleanField(default=False)

    def __unicode__(self):
        return "{}{}".format(self.num_client, self.amount)

    def __str__(self):
        return self.__unicode__()

    def display_name(self):
        return self.__unicode__()

    def save(self):
        """
        Calcul du cost en stock après une operation."""
        self.owner = Owner.get(Owner.islog == True)

        super(Collection, self).save()

    def carat24(self):
        return (self.carat * self.weight) / 24

    def totals_amout(self):
        return self.base * self.carat24()

    def deletes_data(self):
        self.delete_instance()

    def restore(self):
        pass
