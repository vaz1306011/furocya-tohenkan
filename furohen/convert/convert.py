import logging

from pycparser.c_ast import Node as ASTNode

from furohen.exceptions import UnsupportedASTTypeException
from furohen.models.entries.node import Node

from .format_to_str import format_dict

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def to_node(node: ASTNode) -> Node:
    text = to_str(node)
    return Node(text)


def to_str(node: ASTNode) -> str:
    node_type = type(node)
    if not node_type in format_dict:
        raise UnsupportedASTTypeException(node_type)
    return format_dict[node_type](node)
