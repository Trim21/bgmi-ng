from setuptools import setup

setup(
    name="my plugin name",
    entry_points={"bgmi3.extensions.source": ["my-plugin-id = my_source:MySource"]},
)
