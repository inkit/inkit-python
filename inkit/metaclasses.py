from __future__ import absolute_import


from inkit.exceptions import InkitException


class NotInstantiableMetaclass(type):

    def __new__(mcs, classname, superclasses, attr_dict):
        raise InkitException(f'Class {classname} is not instantiable')


class ProductMetaclass(NotInstantiableMetaclass):

    def __getattribute__(cls, item):
        return super().__getattribute__(item)
