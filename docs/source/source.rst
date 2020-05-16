添加数据源
==========

数据源应该是可以通过pip安装，由pypi分发的python package。尽量不内置在 ``BGmi`` 中。

需要继承 :py:class:`bgmi.protocol.source.Base`，并且实现所有的抽象方法，并且提供所有所需的类属性。

确保你的类可以实例化，对应的metaclass会是否实现了所有的抽象方法。

返回的 :py:class:`bgmi.protocol.source.Episode` 等数据类型用到了 ``pydantic``。
可以查阅 `pydantic的文档 <https://pydantic-docs.helpmanual.io/>`_ 了解更多用法。

.. literalinclude:: ../../examples/source.py

setup.py:

.. literalinclude:: ../../examples/setup.py

.. todo::

    应该有一个github template repo，不应该把 ``setup.py`` 的例子也放在这个仓库中
