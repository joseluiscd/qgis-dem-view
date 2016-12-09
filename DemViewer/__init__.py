# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DemViewer
                                 A QGIS plugin
 DEM viewer for QGIS
                             -------------------
        begin                : 2016-12-09
        copyright            : (C) 2016 by José Luis C.D.
        email                : jlcd0003@red.ujaen.es
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load DemViewer class from file DemViewer.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .dem_viewer import DemViewer
    return DemViewer(iface)
