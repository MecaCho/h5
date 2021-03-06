'''
110. 平衡二叉树
给定一个二叉树，判断它是否是高度平衡的二叉树。

本题中，一棵高度平衡二叉树定义为：

一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过1。

示例 1:

给定二叉树 [3,9,20,null,null,15,7]

    3
   / \
  9  20
    /  \
   15   7
返回 true 。

示例 2:

给定二叉树 [1,2,2,3,3,null,null,4,4]

       1
      / \
     2   2
    / \
   3   3
  / \
 4   4
返回 false 。

110. Balanced Binary Tree
Given a binary tree, determine if it is height-balanced.

For this problem, a height-balanced binary tree is defined as:

a binary tree in which the left and right subtrees of every node differ in height by no more than 1.



Example 1:

Given the following tree [3,9,20,null,null,15,7]:

    3
   / \
  9  20
    /  \
   15   7
Return true.

Example 2:

Given the following tree [1,2,2,3,3,null,null,4,4]:

       1
      / \
     2   2
    / \
   3   3
  / \
 4   4
Return false.
'''


# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution(object):

    def deepth(self, root):
        return max(self.deepth(root.left), self.deepth(root.right)) + 1 if root else 0

    def isBalanced(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        if not root:
            return True

        return self.isBalanced(root.left) and self.isBalanced(root.right) and abs(
            self.deepth(root.left) - self.deepth(root.right)) <= 1

# solutions

'''
方法一：自顶向下的递归
算法

定义方法 \texttt{height}height，用于计算任意一个节点 p\in Tp∈T 的高度：

\texttt{height}(p) = \begin{cases} -1 & p \text{ is an empty subtree i.e. } \texttt{null}\\ 1 + \max(\texttt{height}(p.left), \texttt{height}(p.right)) & \text{ otherwise} \end{cases}
height(p)={ 
−1
1+max(height(p.left),height(p.right))
​	
  
p is an empty subtree i.e. null
 otherwise
​	
 

接下来就是比较每个节点左右子树的高度。在一棵以 rr 为根节点的树
TT 中，只有每个节点左右子树高度差不大于 1 时，该树才是平衡的。因此可以比较每个节点左右两棵子树的高度差，然后向上递归。

PythonJavaCppPython

class Solution:
    # Compute the tree's height via recursion
    def height(self, root: TreeNode) -> int:
        # An empty tree has height -1
        if not root:
            return -1
        return 1 + max(self.height(root.left), self.height(root.right))
    
    def isBalanced(self, root: TreeNode) -> bool:
        # An empty tree satisfies the definition of a balanced tree
        if not root:
            return True

        # Check if subtrees have height within 1. If they do, check if the
        # subtrees are balanced
        return abs(self.height(root.left) - self.height(root.right)) < 2 \
            and self.isBalanced(root.left) \
            and self.isBalanced(root.right)
        

1 / 31

复杂度分析

时间复杂度：\mathcal{O}(n\log n)O(nlogn)。

对于每个深度为 dd 的节点 pp，\texttt{height}(p)height(p) 被调用 pp 次。

首先，需要知道一棵平衡二叉树可以拥有的节点数量。令 f(h)f(h) 表示一棵高度为 hh 的平衡二叉树需要的最少节点数量。

f(h) = f(h - 1) + f(h - 2) + 1
f(h)=f(h−1)+f(h−2)+1

这与斐波那契数列的递归关系几乎相同。实际上，它的复杂度分析方法也和斐波那契数列一样。f(h)f(h) 的下界是 f(h) = \Omega\left(\left(\frac{3}{2}\right)^h\right)f(h)=Ω(( 
2
3
​	
 ) 
h
 )。

\begin{align} f(h+1) &= f(h) + f(h-1) + 1 \\ &> f(h) + f(h-1) & \qquad\qquad \text{This is the fibonacci sequence}\\ &\geq \left(\frac{3}{2}\right)^{h} + \left(\frac{3}{2}\right)^{h-1} & \text{via our claim} \\ &= \frac{5}{2} \left(\frac{3}{2}\right)^{h-1}\\ &> \frac{9}{4} \left(\frac{3}{2}\right)^{h-1} & \frac{9}{4} < \frac{5}{2}\\ &> \left(\frac{3}{2}\right)^{h+1} \end{align}

因此，平衡二叉树的高度 hh 不大于 \mathcal{O}(\log_{1.5}(n))O(log 
1.5
​	
 (n))。有了这个限制，可以保证方法 \texttt{height}height 在每个节点上调用不超过 \mathcal{O}(\log n)O(logn) 次。

如果树是倾斜的，高度达到 \mathcal{O}(n)$，算法没有尽早结束，最终会达到 \mathcal{O}(n^2)O(n 
2
 ) 的复杂度。
但是请注意：只要有子节点的两棵子树高度差大于 1，就会停止递归。实际上，如果树是完全倾斜的，仅需要检查最开始的两棵子树。
空间复杂度：\mathcal{O}(n)O(n)。如果树完全倾斜，递归栈可能包含所有节点。

一个有趣的事实：f(n) = f(n-1) + f(n-2) + 1f(n)=f(n−1)+f(n−2)+1 被称为斐波那契数列。

方法二：自底向上的递归
思路

方法一计算 \texttt{height}height 存在大量冗余。每次调用 \texttt{height}height 时，要同时计算其子树高度。但是自底向上计算，每个子树的高度只会计算一次。可以递归先计算当前节点的子节点高度，然后再通过子节点高度判断当前节点是否平衡，从而消除冗余。

算法

使用与方法一中定义的 \texttt{height}height 方法。自底向上与自顶向下的逻辑相反，首先判断子树是否平衡，然后比较子树高度判断父节点是否平衡。算法如下：

检查子树是否平衡。如果平衡，则使用它们的高度判断父节点是否平衡，并计算父节点的高度。

JavaCppPython

class Solution:
    # Return whether or not the tree at root is balanced while also returning
    # the tree's height
    def isBalancedHelper(self, root: TreeNode) -> (bool, int):
        # An empty tree is balanced and has height -1
        if not root:
            return True, -1
        
        # Check subtrees to see if they are balanced. 
        leftIsBalanced, leftHeight = self.isBalancedHelper(root.left)
        if not leftIsBalanced:
            return False, 0
        rightIsBalanced, rightHeight = self.isBalancedHelper(root.right)
        if not rightIsBalanced:
            return False, 0
        
        # If the subtrees are balanced, check if the current tree is balanced
        # using their height
        return (abs(leftHeight - rightHeight) < 2), 1 + max(leftHeight, rightHeight)
        
    def isBalanced(self, root: TreeNode) -> bool:
        return self.isBalancedHelper(root)[0]


1 / 32

复杂度分析

时间复杂度：\mathcal{O}(n)O(n)，计算每棵子树的高度和判断平衡操作都在恒定时间内完成。

空间复杂度：\mathcal{O}(n)O(n)，如果树不平衡，递归栈可能达到 \mathcal{O}(n)O(n)。

作者：LeetCode
链接：https://leetcode-cn.com/problems/balanced-binary-tree/solution/ping-heng-er-cha-shu-by-leetcode/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''