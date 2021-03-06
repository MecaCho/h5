'''

120. Triangle
Given a triangle, find the minimum path sum from top to bottom. Each step you may move to adjacent numbers on the row below.

For example, given the following triangle

[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
The minimum path sum from top to bottom is 11 (i.e., 2 + 3 + 5 + 1 = 11).

Note:

Bonus point if you are able to do this using only O(n) extra space, where n is the total number of rows in the triangle.

120. 三角形最小路径和
给定一个三角形，找出自顶向下的最小路径和。每一步只能移动到下一行中相邻的结点上。

相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。



例如，给定三角形：

[
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]
自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。



说明：

如果你可以只使用 O(n) 的额外空间（n 为三角形的总行数）来解决这个问题，那么你的算法会很加分。
'''


# 动态规划

class Solution(object):
    def minimumTotal(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        for i in range(1, len(triangle)):
            for j in range(len(triangle[i])):
                min1 = triangle[i-1][j] if len(triangle[i-1]) > j else float("inf")
                min2 = triangle[i-1][j-1] if j > 0 else float("inf")
                triangle[i][j] = min(min1, min2) + triangle[i][j]
        return min(triangle[-1])




# 回溯，超时
import functools
class Solution0(object):
    def minimumTotal(self, triangle):
        """
        :type triangle: List[List[int]]
        :rtype: int
        """
        self.res = float("inf")
        self.sum_dict = {}
        def bk(nums, tmp_sum, pre):
            # print(nums, pre)
            if nums == len(triangle):
                if tmp_sum < self.res:
                    self.res = tmp_sum
                return
            bk(nums+1, tmp_sum+triangle[nums][pre], pre)
            if len(triangle[nums]) > pre+1:
                bk(nums+1, tmp_sum+triangle[nums][pre+1], pre+1)
        bk(0, 0, 0)
        return self.res
