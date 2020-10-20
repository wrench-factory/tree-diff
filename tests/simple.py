
from anytree import Node, RenderTree

import Tree.Diff

def test_empty():
    sbs = Tree.Diff.SideBySide(
        iter([]),
        iter([]),
        key=lambda x: str(x)
    )

    assert list(sbs.pairs()) == []


def test_simple():
    sbs = Tree.Diff.SideBySide(
        iter([1, 2, 4, 5, 7]),
        iter([1, 4, 5, 6]),
        key=lambda x: str(x)
    )

    assert list(sbs.pairs()) == [
        (1, 1),
        (2, None),
        (4, 4),
        (5, 5),
        (None, 6),
        (7, None),
        ]


class MyTree(Tree.Diff.Tree):
    def __init__(self, root_node):
        super().__init__()
        self.root_node = root_node

    def root(self):
        return self.root_node

    def children(self, node):
        return node.children


class MyTreeActions(Tree.Diff.TreeActions):
    def __init__(self, log_lines=None):
        super().__init__()
        if log_lines is None:
            log_lines = []
        self.log_lines = log_lines

    @staticmethod
    def name_from_node(node):
        return ''.join(map(lambda x: "/" + x.name, node.path))

    def copy_node(self, reference_node, working_parent_node):
        self.log_lines.append("cp {} under {}".format(
            MyTreeActions.name_from_node(reference_node),
            MyTreeActions.name_from_node(working_parent_node)
        ))
        Node(reference_node.name, parent=working_parent_node)

    def remove_node(self, node):
        self.log_lines.append("remove {}".format(MyTreeActions.name_from_node(node)))
        node.parent = None

    def sync_node(self, reference_node, working_node):
        self.log_lines.append("sync {} to {}".format(
            MyTreeActions.name_from_node(reference_node),
            MyTreeActions.name_from_node(working_node),
        ))
        pass



def build_test_trees():
    #
    root1 = Node("root-reference-tree")
    l1_1 = Node("bar", parent=root1)
    l1_2 = Node("foo", parent=root1)

    l1_1_1 = Node("bar1", parent=l1_1)
    l1_1_2 = Node("bar2", parent=l1_1)
    l1_1_3 = Node("bar3", parent=l1_1)

    root2 = Node("root-working-tree")
    l1_1 = Node("bar", parent=root2)
    l1_2 = Node("foo", parent=root2)

    l1_1_1 = Node("foo1", parent=l1_1)
    l1_1_2 = Node("foo2", parent=l1_1)
    l1_1_3 = Node("foo3", parent=l1_1)

    return MyTree(root1), MyTree(root2)


def test_comparator():

    reference_tree, working_tree = build_test_trees()

    tree_actions = MyTreeActions()

    tree_comparator = Tree.Diff.TreeComparator(
        reference_tree=reference_tree,
        working_tree=working_tree,
        actions=tree_actions,
    )
    tree_comparator.compare()

    print(tree_actions.log_lines)

    assert tree_actions.log_lines == [
        'sync /root-reference-tree to /root-working-tree',
        'sync /root-reference-tree/bar to /root-working-tree/bar',
        'sync /root-reference-tree/foo to /root-working-tree/foo',
        'cp /root-reference-tree/bar/bar1 under /root-working-tree/bar',
        'cp /root-reference-tree/bar/bar2 under /root-working-tree/bar',
        'cp /root-reference-tree/bar/bar3 under /root-working-tree/bar', 'remove /root-working-tree/bar/foo1',
        'remove /root-working-tree/bar/foo2', 'remove /root-working-tree/bar/foo3'
    ]
