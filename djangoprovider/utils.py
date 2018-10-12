# -*- coding: utf-8 -*-
from qgis.core import QgsProviderRegistry, QgsProviderMetadata

from djangoprovider.provider import DjangoProvider


def register_django_provider():
    registry = QgsProviderRegistry.instance()

    metadata = QgsProviderMetadata(DjangoProvider.providerKey(), DjangoProvider.description(),
                                   DjangoProvider.createProvider)

    if not registry.registerProvider(metadata) or registry.providerMetadata(DjangoProvider.providerKey()) != metadata:
         raise Exception('Cannot register Django provider')
