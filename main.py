#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
import sys

sys.path.append(os.path.abspath('../'))

from PyQt4.QtGui import QApplication
from Common.ui.window import FWindow
from Common.cmain import cmain
from Common.ui.style_qss import theme
from ui.mainwindow import MainWindow

app = QApplication(sys.argv)

def main():
    """   """
    window = MainWindow()
    window.setStyleSheet(theme)
    setattr(FWindow, 'window', window)
    # window.show()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # main()
    if cmain():
        main()
