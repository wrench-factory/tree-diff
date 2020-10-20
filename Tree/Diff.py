import abc
import logging

"""
sadasas daskd askldj
"""

from anytree import Node

########################################################################

logger = logging.getLogger(__name__)

########################################################################


class SideBySide:
    """
    This class will take two iterators as input and will return them in pairs but sorted.

    :param a: first iterator
    :type a: iterator
    :param b: second iterator
    :type b: iterator

    Imagine the following iterators:

    1. Iterator A: `[1,2,4,5,7]`
    2. Iterator B: `[1,4,5,6]`

    The `pairs()` will return the following pairs as tuples.

    .. code-block:: python3
       :linenos:

       (1,1)    <- the same elements from A and B will returned together
       (2,None) <- If there is no match in the other iterator None will be returned.
       (4,4)
       (5,5)
       (None,6)
       (7, None)

    Parameters
    ----------
    a : iterator
      First iterator
    b : iterator
      Second iterator
    key : function to extract the name from the elements

    """
    def __init__(self, a, b, key):
        self.a = a
        self.b = b
        self.key = key

    def pairs(self):
        """
        You can iterate through `pairs()`.

        :return: tuple elements
        """
        iter_a = iter(self.a)
        iter_b = iter(self.b)

        element_a = None
        element_b = None

        while True:

            if element_a is None and iter_a is not None:
                try:
                    element_a = next(iter_a)
                except StopIteration:
                    iter_a = None
                    element_a = None

            if element_b is None and iter_b is not None:
                try:
                    element_b = next(iter_b)
                except StopIteration:
                    iter_b = None
                    element_b = None

            name_a = 'None'
            if element_a is not None:
                name_a = self.key(element_a)

            name_b = 'None'
            if element_b is not None:
                name_b = self.key(element_b)

            logger.debug('{} <-> {}'.format(name_a, name_b))

            if element_a is None and element_b is None:
                return

            if element_a is not None and element_b is None:
                yield element_a, None
                element_a = None
            elif element_a is None and element_b is not None:
                yield None, element_b
                element_b = None
            elif self.key(element_a) < self.key(element_b):
                yield element_a, None
                element_a = None
            elif self.key(element_a) > self.key(element_b):
                yield None, element_b
                element_b = None
            else:
                yield element_a, element_b
                element_a = None
                element_b = None


########################################################################

class Tree(metaclass=abc.ABCMeta):
    """
    This is our private Tree class with just 2 methods.

    The first method :py:meth:`Tree.root()` will return the root node.

    """
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def root(self):
        """
        This will return the root node of the tree.

        :return: the root node.
        """
        pass

    @abc.abstractmethod
    def children(self, node):
        """
        This will return the children of the given node of the tree.

        Parameters
        ----------
        node : object
          This method will return the children of the given `node`.

        Returns
        -------
        list
          The list of children
        """
        pass


########################################################################


class TreeFromList(Tree):
    def __init__(self, nodes=None):
        super().__init__()
        self.root_node = Tree._prepare_nodes(nodes)

    @staticmethod
    def _prepare_nodes(self, nodes):

        node_for_name = {}

        root_node = None

        for data in nodes:
            node = Node(data['identifier'])

            if root_node is None:
                root_node = node

            node_for_name[node.name] = node

        for data in nodes:
            for child_name in data['children']:
                node_for_name[child_name].parent = node_for_name[data['identifier']]

        return root_node

    def root(self):
        return self.root_node

    def children(self, node):
        list_of_children = node.children

        def get_children_key(n):
            return n.name

        return sorted(list_of_children, key=get_children_key)

    def name(self, node):
        return node.name

########################################################################


class TreeActions(metaclass=abc.ABCMeta):
    """
    These are the 3 methods that we are supporting
    for transforming one tree into a second one.

    First action: :py:meth:`TreeActions.copy_node()`:

    .. code-block::

         A          A
        / \\   ->     \\
       B   C          C

    Copy the node `A/B` to the right side (to the same place).

    Second action: :py:meth:`TreeActions.remove_node()`:

    .. code-block::

         A          A
          \\   ->   / \\
           C      B   C

    Delete the node `B` on the right side

    :py:meth:`TreeActions.remove_node()`,
    :py:meth:`TreeActions.sync_node()`,

    """
    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def copy_node(self, reference_node, working_parent_node):
        """
        This will return the root node of the tree.

        Parameters
        ----------
        reference_node : object
          This method will return the children of the given `node`.
        working_parent_node : object
          This method will return the children of the given `node`.

        Returns
        -------
        list
          The list of children
        """
        pass

    @abc.abstractmethod
    def remove_node(self, node):
        pass

    @abc.abstractmethod
    def sync_node(self, reference_node, working_node):
        pass


########################################################################


class ProtocolTreeActions(TreeActions):
    def __init__(self):
        super().__init__()
        self.protocol = []

    @staticmethod
    def resolve(node):
        return '/'.join([n.name for n in node.path])

    def copy_node(self, reference_node, working_parent_node):
        self.protocol.append('cp {} {}'.format(ProtocolTreeActions.resolve(reference_node),
                                               ProtocolTreeActions.resolve(working_parent_node)))
        Node(reference_node.name).parent = working_parent_node

    def remove_node(self, node):
        self.protocol.append('rm {}'.format(ProtocolTreeActions.resolve(node)))
        node.parent = None

    def sync_node(self, reference_node, working_node):
        self.protocol.append('sync {} {}'.format(ProtocolTreeActions.resolve(reference_node),
                                                 ProtocolTreeActions.resolve(working_node)))


########################################################################

class TreeComparator:
    """
    This class compares 2 trees (first and second) and gives you the actions you need to perform on the second tree,
    so the second tree will match the first one.

    For the clarity: the `reference_tree` will not changed at all. The `working_tree` will be changed to it's the same
    as the `reference_tree`.

    These are the 3 actions to transform `working_tree` into your `reference_tree`.

    * :py:meth:`TreeActions.copy_node`
    * :py:meth:`TreeActions.remove_node`
    * :py:meth:`TreeActions.sync_node`

    The constructor will take 2 arguments.

    :param reference_tree: The is the reference tree
    :type reference_tree: :py:meth:`Tree` like object
    :param working_tree: second iterator
    :type working_tree: :py:meth:`Tree` like object

    """
    def __init__(self,  reference_tree: Tree, working_tree: Tree, actions: TreeActions):
        self.reference_tree: Tree = reference_tree
        self.working_tree: Tree = working_tree
        self.tree_actions: TreeActions = actions

    #
    #    root             root
    #    / | \            / | \
    #   /  |  \          /  |  \
    #  1   2   3        0   2   4
    #     /|\
    #    / | \
    #   a  b  c

    def compare(self):
        """

        :return:
        """
        self.tree_actions.sync_node(self.reference_tree.root(), self.working_tree.root())

        self._compare_leaf(self.reference_tree.root(), self.working_tree.root())

    def _compare_leaf(self, reference_node, working_node):

        def name_from_node(node):
            return node.name

        logger.debug("Getting children for reference node '{!s}' and working node '{!s}'".
                     format(reference_node, working_node))
        children_a = self.reference_tree.children(reference_node)
        children_b = self.working_tree.children(working_node)

        for pair in SideBySide(children_a, children_b, key=name_from_node).pairs():

            if pair[0] is not None and pair[1] is None:
                logger.debug('Comparing node pair ({!s}↔{!s}): {}'.format(pair[0], pair[1], 'copy node'))
                self.tree_actions.copy_node(pair[0], working_node)
            elif pair[0] is None and pair[1] is not None:
                logger.debug('Comparing node pair ({!s}↔{!s}): {}'.format(pair[0], pair[1], 'remove node'))
                self.tree_actions.remove_node(pair[1])
            else:
                logger.debug('Comparing node pair ({!s}↔{!s}): {}'.format(pair[0], pair[1], 'sync node'))
                self.tree_actions.sync_node(pair[0], pair[1])

        #   Generate a new list of children because this was changed!
        children_a = list(self.reference_tree.children(reference_node))
        children_b = list(self.working_tree.children(working_node))

        logger.debug("reference tree node {!s} has {} children, working tree node {!s} has {} children".format(
                     reference_node, len(children_a),
                     working_node, len(children_b),
                     ))

        pairs = list(SideBySide(children_a, children_b, key=name_from_node).pairs())

        for pair in pairs:
            assert pair[0] is not None and pair[1] is not None, "Empty pair?"
            assert pair[0] is not None, 'Reference node has no match for working tree node {!s}'.format(pair[1])
            assert pair[1] is not None, 'Working tree node has no match for reference tree node {!s}'.format(pair[0])
            self._compare_leaf(pair[0], pair[1])

########################################################################

