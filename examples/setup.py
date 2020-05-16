from setuptools import setup

setup(
    name="my plugin name",
    entry_points={"bgmi.extensions.source": ["my-plugin-id = my_source:MySource"]},
)
