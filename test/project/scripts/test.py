# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys

from PyQt5.QtCore import QSize

from qgis.core import (
    QgsVectorLayer,
    QgsApplication,
    QgsProject, QgsMapSettings, QgsMapRendererCustomPainterJob)

from PyQt5.QtGui import *

import django

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))

# Standalone test which is not run through manage.py
if __name__ == '__main__':
    # QGIS_PREFIX_PATH should be set if not run from install dir
    qgs = QgsApplication([], False)
    qgs.initQgis()

    django.setup(set_prefix=False)

    from djangoprovider import DjangoProvider, register_django_provider
    register_django_provider()

    from basic.models import *  # after django setup

    model = Point
    uri = '%s.%s' % (model._meta.app_label, model._meta.model_name)
    layer = QgsVectorLayer(uri, 'test', 'djangoprovider')
    print('layer valid: %s' % layer.isValid())
    print('feature count: %s' % layer.featureCount())
    print('crs authid: %s' % layer.crs().authid())
    print('extent: %s' % layer.sourceExtent().toString())
    QgsProject.instance().addMapLayer(layer)
    
    image = QImage(QSize(600, 400), QImage.Format_ARGB32_Premultiplied)

    image.fill(QColor(255, 255, 128).rgb())

    painter = QPainter(image)
    
    settings = QgsMapSettings()
    settings.setOutputDpi(image.logicalDpiX())
    settings.setOutputImageFormat(QImage.Format_ARGB32)
    settings.setDestinationCrs(layer.crs())
    settings.setOutputSize(image.size())
    settings.setFlag(QgsMapSettings.Antialiasing, True)
    settings.setFlag(QgsMapSettings.RenderMapTile, True)
    settings.setFlag(QgsMapSettings.UseAdvancedEffects, True)
    settings.setBackgroundColor(QColor(255, 255, 255, 0))

    settings.setLayers([layer])
    settings.setExtent(layer.extent())

    job = QgsMapRendererCustomPainterJob(settings, painter)
    job.renderSynchronously()
    painter.end()

    output_path = os.environ.get('QGIS_DJANGO_PROVIDER_TEST_OUTPUT', '/tmp/qgis-django-provider-test.png')
    image.save(output_path,'png')
