import inspect
from abc import ABCMeta as _ABCMeta
from abc import abstractmethod
from typing import Any


class AbstractAttribute:
    def __init__(self, doc: str) -> None:
        self.__doc__ = doc
        self.__is_abstract_attribute__ = True


def abstract_class_attribute(doc: str = "") -> Any:
    return AbstractAttribute(doc)


class Meta(_ABCMeta):
    def __new__(cls, name: str, bases: tuple, namespace: dict) -> Any:
        cls = _ABCMeta.__new__(cls, name, bases, namespace)
        if not bases:
            return cls
        abstract_attributes = set()
        abstract_class_method = set()
        for name in dir(cls):
            attr = getattr(cls, name)
            if getattr(attr, "__is_abstract_attribute__", False):
                abstract_attributes.add(name)
            elif getattr(attr, "__isabstractmethod__", False) and inspect.ismethod(
                attr
            ):
                abstract_class_method.add(name)

        if abstract_attributes:
            raise NotImplementedError(
                "Can't create class {} with abstract class attributes: {}".format(
                    cls.__name__, ", ".join(abstract_attributes)
                )
            )
        if abstract_class_method:
            raise NotImplementedError(
                "Can't create class {} with abstract classmethod: {}".format(
                    cls.__name__, ", ".join(abstract_class_method)
                )
            )
        return cls


__all__ = ["abstract_class_attribute", "abstractmethod", "Meta"]
