"""

This package lets you compare two tree(-like) objects. The tree object can be anything,
but must meet the following conditions:

- the tree must have one root
- every node on the tree must have a name/identifier

Here's the big picture:

- We have three classes you must support/implement.
- The first class is the tree representation called. We call it `Tree` in this document.
- The second class is the tree comparison class (`Comparator` at this place.)
- The third class is is the tree changer (`Actions`).
- Stay calm.

The `TreeComparator` takes 2 `Tree` objects and compares them. Differences will
be announced (read: callback) via the `TreeActions` object.

"""

