# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class PointAdmin( admin.ModelAdmin ):
    list_display = ('id', 'integer_field', 'char_field' )

admin.site.register(Point, PointAdmin)
