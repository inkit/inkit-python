from __future__ import absolute_import

from inkit.metaclasses import ProductMetaclass


class AbstractProduct(metaclass=ProductMetaclass):

    _main_resource = None
