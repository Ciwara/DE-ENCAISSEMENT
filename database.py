#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from models import (ProviderOrClient, Collection, Disbursement)

from Common.cdatabase import AdminDatabase


class Setup(AdminDatabase):

    """docstring for FixtInit"""

    def __init__(self):
        super(AdminDatabase, self).__init__()

        self.LIST_CREAT.append(ProviderOrClient)
        self.LIST_CREAT.append(Collection)
        self.LIST_CREAT.append(Disbursement)
