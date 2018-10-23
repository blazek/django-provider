# -*- coding: utf-8 -*-
"""
QGIS vector provider for Django Web framework https://www.djangoproject.com/
"""
__author__ = 'Radim Blazek'
__date__ = '2018-10-10'
__copyright__ = 'Copyright 2018, Radim Blazek'

from qgis.PyQt.QtCore import QVariant, QUrl, QUrlQuery
from qgis.core import (
    QgsField,
    QgsFields,
    QgsFeatureRequest,
    QgsWkbTypes,
    QgsCoordinateReferenceSystem,
    QgsDataProvider,
    QgsVectorDataProvider,
    QgsRectangle,
    QgsFeatureIterator
)

from django.apps import apps
from django.contrib.gis.db import models

from .source import DjangoFeatureSource

wkb_types = {
    models.PointField: QgsWkbTypes.Point,
    models.MultiPointField: QgsWkbTypes.MultiPoint,
    models.LineStringField: QgsWkbTypes.LineString,
    models.MultiLineStringField: QgsWkbTypes.MultiLineString,
    models.PolygonField: QgsWkbTypes.Polygon,
    models.MultiPolygonField: QgsWkbTypes.MultiPolygon,
}


class DjangoProvider(QgsVectorDataProvider):

    @classmethod
    def providerKey(cls):
        return 'djangoprovider'

    @classmethod
    def description(cls):
        return 'Django vector provider'

    @classmethod
    def createProvider(cls, uri, providerOptions):
        return DjangoProvider(uri, providerOptions)

    def __init__(self, uri='', providerOptions=QgsDataProvider.ProviderOptions()):
        """
        :param uri: <app>.<model>[?geofield=<name>]
        :param providerOptions:
        """
        super().__init__(uri)
        self._is_valid = False
        self.setNativeTypes((
            # TODO
            QgsVectorDataProvider.NativeType('Integer', 'integer', QVariant.Int, -1, -1, 0, 0),
            QgsVectorDataProvider.NativeType('Text', 'text', QVariant.String, -1, -1, -1, -1),
        ))
        self._uri = uri
        url = QUrl(uri)
        url_query = QUrlQuery(url)
        self._full_model_name = url.path()
        self._app_label, self._model_name = self._full_model_name.split('.')
        self._model = apps.get_model(self._app_label, self._model_name)  # Django model
        self._meta = self._model._meta

        self._fields = QgsFields()
        self._dj_fields = []  # Django fields represented by provider in the same order as QgsFields
        for field in self._meta.get_fields():
            # TODO: more field types
            f = None
            if isinstance(field, models.IntegerField):
                f = QgsField(field.name, QVariant.Int, 'integer', 0, 0, field.verbose_name)
            elif isinstance(field, models.CharField):
                f = QgsField(field.name, QVariant.String, 'varchar', field.max_length, 0, field.verbose_name)

            if f:
                self._fields.append(f)
                self._dj_fields.append(field)

        self._geo_field_name = url_query.queryItemValue('geofield')
        self._geo_field = None  # Django geometry field
        if self._geo_field_name:
            self._meta.get_field(self._geo_field_name)
        else:
            # If geometry field was not specified in uri, use the first one if any.
            for field in self._meta.get_fields():
                if isinstance(field, models.GeometryField):
                    self._geo_field = field
                    self._geo_field_name = field.name
                    break

        self._wkbType = QgsWkbTypes.NoGeometry
        if self._geo_field:
            for geo_field_class in wkb_types.keys():
                if isinstance(self._geo_field, geo_field_class):
                    self._wkbType = wkb_types[geo_field_class]
                    break

        self._extent = QgsRectangle()
        self._crs = None
        if self._geo_field:
            self._crs = QgsCoordinateReferenceSystem.fromEpsgId(self._geo_field.srid)
        self._provider_options = providerOptions
        self._is_valid = True

    def featureSource(self):
        return DjangoFeatureSource(self._model, self._fields, self._dj_fields, self._geo_field, self._crs )

    def dataSourceUri(self, expandAuthConfig=True):
        return self._uri

    def storageType(self):
        return "Django"

    def getFeatures(self, request=QgsFeatureRequest()):
        return QgsFeatureIterator(self.featureSource().getFeatures(request))

    def uniqueValues(self, fieldIndex, limit=-1):
        if fieldIndex < 0 or fieldIndex >= self.fields().count():
            return set()

        dj_field = self._dj_fields[fieldIndex]
        values = self._model.objects.get_queryset().order_by(dj_field.name).values_list(dj_field.name, flat=True).distinct()
        if limit >= 0:
            values = values[:limit]
        return set(values)

    def wkbType(self):
        return self._wkbType

    def featureCount(self):
        return self._model.objects.get_queryset().count()

    def fields(self):
        return self._fields

    def addFeatures(self, features, flags=None):
        # TODO
        return False

    def deleteFeatures(self, ids):
        # TODO
        return False

    def addAttributes(self, attrs):
        return False

    def renameAttributes(self, renamedAttributes):
        return False

    def deleteAttributes(self, attributes):
        return False

    def changeAttributeValues(self, attr_map):
        # TODO
        for feature_id, attrs in attr_map.items():
            pass
        self.clearMinMaxCache()
        return True

    def changeGeometryValues(self, geometry_map):
        # TODO
        for feature_id, geometry in geometry_map.items():
            pass
        self.updateExtents()
        return True

    def allFeatureIds(self):
        return list(self._model.objects.get_queryset().values_list(self._meta.pk.name, flat=True))

    def subsetString(self):
        return None

    def setSubsetString(self, subsetString):
        return False

    def supportsSubsetString(self):
        return False

    def createSpatialIndex(self):
        return False

    def capabilities(self):
        # TODO: QgsVectorDataProvider.AddFeatures | QgsVectorDataProvider.DeleteFeatures | QgsVectorDataProvider.ChangeGeometries | QgsVectorDataProvider.ChangeAttributeValues
        # TODO: TransactionSupport
        return QgsVectorDataProvider.SelectAtId

    # ---------------------------- functions from QgsDataProvider ----------------------------

    def name(self):
        return self.providerKey()

    def extent(self):
        # TODO
        return QgsRectangle(-20037508.34, -20037508.34, 20037508.34, 20037508.34)
        if self._extent.isEmpty() and self._geo_field:
            box = list(self._model.objects.get_queryset().aggregate(models.Extent(self._geo_field_name)).values())[0]
            self._extent = QgsRectangle(box[0], box[0], box[0], box[0])

        return QgsRectangle(self._extent)

    def updateExtents(self):
        self._extent.setMinimal()

    def isValid(self):
        return self._is_valid

    def crs(self):
        return self._crs

    # -------------------------------- Private methods --------------------------------

    def _get_django_field(self, field_index):
        return self._dj_fields[field_index]