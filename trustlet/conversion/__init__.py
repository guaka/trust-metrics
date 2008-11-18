"""
conversion module,
you can convert a c2 in a pajek, or a dot, or some other
standard format, listed here:
pajek
dot

"""

__all__ = ['wikixml2graph','dot','pajek']

from wikixml2graph import wikixml2graph
import dot
import pajek
