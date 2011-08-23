#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import  template
import datetime

register = template.Library()

@register.filter(name='timestamp_convert')
def timestamp_convert(value):
    return datetime.datetime.fromtimestamp(float(value))