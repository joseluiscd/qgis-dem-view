# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DemViewerDockWidget
                                 A QGIS plugin
 DEM viewer for QGIS
                             -------------------
        begin                : 2016-12-09
        git sha              : $Format:%H$
        copyright            : (C) 2016 by José Luis C.D.
        email                : jlcd0003@red.ujaen.es
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
from qgis.core import *
import dem_render, dem_drawable

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dem_viewer_dockwidget_base.ui'))


class DemViewerDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()



    def __init__(self, parent=None):
        """Constructor."""
        super(DemViewerDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.updateLayers()
        self.viewButton.pressed.connect(self.viewModel)


    def updateLayers(self):
        reg = QgsMapLayerRegistry.instance()
        for i in range(self.heightLayerBox.count()):
            self.heightLayerBox.removeItem(i)

        for i in range(self.colorLayerBox.count()):
            self.colorLayerBox.removeItem(i)

        for name, layer in reg.mapLayers().items():
            if isinstance(layer, QgsRasterLayer):
                self.heightLayerBox.addItem(name, layer)
                self.colorLayerBox.addItem(name, layer)



    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    def viewModel(self, *args, **kwargs):
        print(args)
        print(kwargs)

        heightRaster = self.heightLayerBox.itemData(self.heightLayerBox.currentIndex()).dataProvider()
        colorRaster = self.colorLayerBox.itemData(self.colorLayerBox.currentIndex()).dataProvider()

        dem = dem_drawable.DemDrawable(heightRaster, colorRaster, self.precisionBox.value())

        a = dem_render.DemViewerWindow(dem)

        self.currentWindow = a


        a.showMaximized()
