#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)
import os
# from static import Constants
from Common.cstatic import CConstants

ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))


class Config(CConstants):

    """ docstring for Config
                            """

    DATEFORMAT = u'%d/%m/%Y'

    def __init__(self):
        CConstants.__init__(self)

    # ------------------------- Organisation --------------------------#

    from Common.models import Settings, Version, Organization

    try:
        DB_VERS = Version().get(Version.id == 1)
    except Exception as e:
        print(e)
        DB_VERS = 1
    try:
        sttg = Organization().get(Settings.id == 1)
        # LOGIN = sttg.login
        NAME_ORGA = sttg.name_orga
        TEL_ORGA = sttg.phone
        ADRESS_ORGA = sttg.adress_org
        BP = sttg.bp
        EMAIL_ORGA = sttg.email_org
        DEVISE_M = sttg.devise
        # DEBUG = True
    except Exception as e:
        print(e)
    # DEBUG = True
    DEBUG = False

    # des_image_record = "static/img_prod"
    ARMOIRE = "img_prod"
    des_image_record = os.path.join(ROOT_DIR, ARMOIRE)
    PEEWEE_V = 224
    credit = 17
    tolerance = 50
    nb_warning = 5
    ORG_LOGO = None

    # -------- Application -----------#

    NAME_MAIN = "main.py"

    pdf_source = "pdf_source.pdf"
    APP_NAME = "DE-ENCAISEMENT"

    APP_VERSION = 1
    APP_DATE = u"02/2020"
    img_media = os.path.join(os.path.join(ROOT_DIR, "static"), "images/")
    APP_LOGO = os.path.join(img_media, "logo.png")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")
