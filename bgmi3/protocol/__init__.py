"""Protocol

all bgmi3 source and output plugin should implement abc from this package
"""
from bgmi3.protocol import backend, output, source

__all__ = ["backend", "output", "source"]
