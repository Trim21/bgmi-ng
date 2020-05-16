import pytest

from bgmi.helper import abstract


class BaseWIthClassMethod(metaclass=abstract.Meta):
    @classmethod
    @abstract.abstractmethod
    def abs_class(cls):  # pragma: no cover
        pass


class BaseWithMethod(metaclass=abstract.Meta):
    @abstract.abstractmethod
    def abs_class(self):  # pragma: no cover
        pass


class BaseWithAttr(metaclass=abstract.Meta):
    a = abstract.abstract_class_attribute()


def test_class_method():

    with pytest.raises(NotImplementedError):

        class B(BaseWIthClassMethod):
            pass


def test_method_should_not_raise_when_create():
    class B(BaseWithMethod):
        pass


def test_method_should_raise_when_inst():
    class B(BaseWithMethod):
        pass

    with pytest.raises(NotImplementedError):
        B()


def test_method_should_not_raise_when_inst():
    class B(BaseWithMethod):
        def abs_class(self):
            pass

    B()


def test_missing_class_attr():

    with pytest.raises(NotImplementedError):

        class B(BaseWithAttr):
            pass
