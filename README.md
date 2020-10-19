# Summary #

Compares (abstract) tree objects

# Description #

This can be useful for syncing filesystems or other hierarchical structures.

The library will take 2 tree objects and returns abstract working instructions
so the second tree will look like the first tree.

      root-reference-tree  root-working-tree
            /  \                 /  \
          bar  foo             bar  foo
         / | \                     / | \
        /  |  \                   /  |  \
    bar1  bar2 bar3           foo1  foo2 foo3

We need 9 steps to transform the working tree.

1. sync `/root-reference-tree` to `/root-working-tree`
2. sync `/root-reference-tree/bar` to `/root-working-tree/bar`
3. sync `/root-reference-tree/foo` to `/root-working-tree/foo`
4. copy `/root-reference-tree/bar/bar1` under `/root-working-tree/bar`
5. copy `/root-reference-tree/bar/bar2` under `/root-working-tree/bar`
6. copy `/root-reference-tree/bar/bar3` under `/root-working-tree/bar`
7. remove `/root-working-tree/bar/foo1`
8. remove `/root-working-tree/bar/foo2`
9. remove `/root-working-tree/bar/foo3`

# Used tutorials #

* [How to Publish an Open-Source Python Package to PyPI – Real Python](https://realpython.com/pypi-publish-python-package/)
* [Packaging Python Projects — Python Packaging User Guide](https://packaging.python.org/tutorials/packaging-projects/)
* [Sharing docs on ReadTheDocs | Creating and sharing a CircuitPython library | Adafruit Learning System](https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs)
* [A “How to” Guide for Sphinx + ReadTheDocs — Sphinx-RTD-Tutorial documentation](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/index.html)
