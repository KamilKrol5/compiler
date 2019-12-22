from typing import List


class TreeNode:
    def __init__(self, children: List['TreeNode'], parent: 'TreeNode', child_id=0):
        self.children: List['TreeNode'] = children
        self.parent: TreeNode = parent
        self.child_id: int = child_id


class Tree:
    def __init__(self, root: TreeNode, name='tree'):
        self.name = name
        self.root = root

    def __str__(self):
        return str(self.root)


class BinaryOperation(TreeNode):
    def __init__(self, children: List['TreeNode'], parent: 'TreeNode', operator: str, child_id=0):
        super().__init__(children, parent, child_id)
        self.operator = operator


class WhileNode(TreeNode):
    def __init__(self, children: List['TreeNode'], parent: 'TreeNode'):
        super().__init__(children, parent)