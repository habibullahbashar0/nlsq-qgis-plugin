# -*- coding: utf-8 -*-
"""
/***************************************************************************
 NLSQ Plugin
 ***************************************************************************/
"""

def classFactory(iface):
    """Load NLSQPlugin class from file nlsq_plugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .nlsq_plugin import NLSQPlugin
    return NLSQPlugin(iface)
