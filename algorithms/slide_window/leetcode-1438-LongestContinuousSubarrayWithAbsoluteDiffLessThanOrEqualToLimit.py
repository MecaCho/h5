# encoding=utf8


'''
1438. 绝对差不超过限制的最长连续子数组
给你一个整数数组 nums ，和一个表示限制的整数 limit，请你返回最长连续子数组的长度，该子数组中的任意两个元素之间的绝对差必须小于或者等于 limit 。

如果不存在满足条件的子数组，则返回 0 。



示例 1：

输入：nums = [8,2,4,7], limit = 4
输出：2
解释：所有子数组如下：
[8] 最大绝对差 |8-8| = 0 <= 4.
[8,2] 最大绝对差 |8-2| = 6 > 4.
[8,2,4] 最大绝对差 |8-2| = 6 > 4.
[8,2,4,7] 最大绝对差 |8-2| = 6 > 4.
[2] 最大绝对差 |2-2| = 0 <= 4.
[2,4] 最大绝对差 |2-4| = 2 <= 4.
[2,4,7] 最大绝对差 |2-7| = 5 > 4.
[4] 最大绝对差 |4-4| = 0 <= 4.
[4,7] 最大绝对差 |4-7| = 3 <= 4.
[7] 最大绝对差 |7-7| = 0 <= 4.
因此，满足题意的最长子数组的长度为 2 。
示例 2：

输入：nums = [10,1,2,4,7,2], limit = 5
输出：4
解释：满足题意的最长子数组是 [2,4,7,2]，其最大绝对差 |2-7| = 5 <= 5 。
示例 3：

输入：nums = [4,2,2,2,4,4,2,2], limit = 0
输出：3


提示：

1 <= nums.length <= 10^5
1 <= nums[i] <= 10^9
0 <= limit <= 10^9


1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
Given an array of integers nums and an integer limit, return the size of the longest continuous subarray such that the absolute difference between any two elements is less than or equal to limit.

In case there is no subarray satisfying the given condition return 0.



Example 1:

Input: nums = [8,2,4,7], limit = 4
Output: 2
Explanation: All subarrays are:
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4.
Therefore, the size of the longest subarray is 2.
Example 2:

Input: nums = [10,1,2,4,7,2], limit = 5
Output: 4
Explanation: The subarray [2,4,7,2] is the longest since the maximum absolute diff is |2-7| = 5 <= 5.
Example 3:

Input: nums = [4,2,2,2,4,4,2,2], limit = 0
Output: 3


Constraints:

1 <= nums.length <= 10^5
1 <= nums[i] <= 10^9
0 <= limit <= 10^9
'''


class Solution(object):
    def longestSubarray(self, nums, limit):
        """
        :type nums: List[int]
        :type limit: int
        :rtype: int
        """
        # max_length = 1
        # cur = [nums[0]]
        # index_map = {nums[0]:0}
        # max_val = min_val = nums[0]
        # for i in range(1, len(nums)):

        #     if nums[i] > max_val:
        #         max_val = nums[i]
        #     if nums[i] < min_val:
        #         min_val = nums[i]

        #     if max_val - min_val <= limit:
        #         cur.append(nums[i])
        #         max_length = max(max_length, len(cur))
        #     else:
        #         # if max_val == nums[i]:
        #         #     cur = nums[index_map[min_val]+1:i+1]

        #         # elif min_val == nums[i]:
        #         #     cur = nums[index_map[max_val]+1:i+1]
        #         cur = cur[1:] + [nums[i]]
        #         max_val = max(cur)
        #         min_val = min(cur)
        #         # if max_val == nums[i]:
        #         #     j = i - 1
        #         #     while j >= 0:
        #         #         if max_val - nums[j] <= limit:
        #         #             min_val = nums[j]
        #         #             break
        #         #     cur = nums[j:i+1]
        #         # elif min_val == nums[i]:
        #         #     j = i - 1
        #         #     while j >= 0:
        #         #         if nums[j] - min_val <= limit:
        #         #             max_val = nums[j]
        #         #             break
        #         #     cur = nums[j:i+1]


        #     index_map[nums[i]] = i


        mins = []
        maxs = []
        cur = []
        max_length = 0

        for i in range(len(nums)):
            num = nums[i]
            cur.append(num)

            if not mins or num <= mins[-1]:
                mins.append(num)
            if not maxs or num >= maxs[-1]:
                maxs.append(num)

            min_val = mins[-1]
            max_val = maxs[-1]


            # print(min_val, mins, max_val, maxs, cur, len(cur))
            if max_val - min_val > limit:
                pop_val = cur.pop(0)
                if pop_val == mins[0]:
                    mins.pop(0)
                    if not mins:
                        mins.append(cur[0])
                        i = 1
                        while i < len(cur):
                            if cur[i] <= mins[-1]:
                                mins.append(cur[i])
                            i += 1
                if pop_val == maxs[0]:
                    maxs.pop(0)
                    if not maxs:
                        maxs.append(cur[0])
                        i = 1
                        while i < len(cur):
                            if cur[i] >= maxs[-1]:
                                maxs.append(cur[i])
                            i += 1
            else:
                max_length = max(max_length, len(cur))
                # print(max_length, len(cur), max(cur), min(cur), cur)
        # print(len(nums), max(nums), min(nums))
        return max_length


class Solution1(object):
    def longestSubarray(self, nums, limit):
        """
        :type nums: List[int]
        :type limit: int
        :rtype: int
        """
        # if not nums:
        #     return 0
        # curr_max = nums[0] # 当子数组下最大值 这里初始化为第一个数
        # curr_min = nums[0] # 当子数组下最大值 这里初始化为第一个数
        # sub_nums = [] # 以数组作为窗口滑动
        # for num in nums:
        #     if abs(num - curr_max) <=  limit and abs(num - curr_min) <=  limit and abs(curr_max - curr_min) <= limit:
        #         curr_max = max(num,curr_max)
        #         curr_min = min(num,curr_min)
        #         sub_nums.append(num)
        #     else:
        #         sub_nums.append(num)
        #         sub_nums.pop(0)
        #         curr_max = max(sub_nums) # 当子数组最大值
        #         curr_min = min(sub_nums) # 当前子数组最小值
        # return  len(sub_nums)

        max_length = 1
        cur = [nums[0]]
        max_val = min_val = nums[0]
        for i in range(1, len(nums)):
            if nums[i] > max_val:
                max_val = nums[i]
            if nums[i] < min_val:
                min_val = nums[i]

            if max_val - min_val <= limit:
                cur.append(nums[i])
                max_length = max(max_length, len(cur))
            else:
                # if max_val == nums[i]:
                #     cur = nums[index_map[min_val]+1:i+1]

                # elif min_val == nums[i]:
                #     cur = nums[index_map[max_val]+1:i+1]
                # cur = cur[1:] + [nums[i]]
                cur.append(nums[i])
                cur.pop(0)
                max_val = max(cur)
                min_val = min(cur)
                # if max_val == nums[i]:
                #     j = i - 1
                #     while j >= 0:
                #         if max_val - nums[j] <= limit:
                #             min_val = nums[j]
                #             break
                #     cur = nums[j:i+1]
                # elif min_val == nums[i]:
                #     j = i - 1
                #     while j >= 0:
                #         if nums[j] - min_val <= limit:
                #             max_val = nums[j]
                #             break
                #     cur = nums[j:i+1]

        #     index_map[nums[i]] = i

        # mins = []
        # maxs = []
        # cur = []
        # max_length = 0

        # for i in range(len(nums)):
        #     num = nums[i]
        #     cur.append(num)

        #     if not mins or num <= mins[-1]:
        #         mins.append(num)
        #     if not maxs or num >= maxs[-1]:
        #         maxs.append(num)

        #     min_val = mins[-1]
        #     max_val = maxs[-1]

        #     # print(min_val, mins, max_val, maxs, cur, len(cur))
        #     if max_val - min_val > limit:
        #         pop_val = cur.pop(0)
        #         if pop_val == mins[0]:
        #             mins.pop(0)
        #             if not mins:
        #                 mins.append(cur[0])
        #                 i = 1
        #                 while i < len(cur):
        #                     if cur[i] <= mins[-1]:
        #                         mins.append(cur[i])
        #                     i += 1
        #         if pop_val == maxs[0]:
        #             maxs.pop(0)
        #             if not maxs:
        #                 maxs.append(cur[0])
        #                 i = 1
        #                 while i < len(cur):
        #                     if cur[i] >= maxs[-1]:
        #                         maxs.append(cur[i])
        #                     i += 1
        #     else:
        #         max_length = max(max_length, len(cur))
        #         # print(max_length, len(cur), max(cur), min(cur), cur)
        # # print(len(nums), max(nums), min(nums))
        return max_length



class Solution20210221(object):
    def longestSubarray(self, nums, limit):
        """
        :type nums: List[int]
        :type limit: int
        :rtype: int
        """
        l, r = 0, 0
        max_len = 1
        max_, min_ = nums[0], nums[0]
        length = len(nums)
        res = 1
        while r < length:
            if nums[r] > max_:
                max_ = nums[r]

            if nums[r] < min_:
                min_ = nums[r]

            while l < r and max_ - min_ > limit:
                l += 1
                max_ = max(nums[l:r + 1])
                min_ = min(nums[l:r + 1])

            r += 1
            res = max(res, r - l)

        return res


# solutions

'''
方法一：滑动窗口 + 有序集合
思路和解法

我们可以枚举每一个位置作为右端点，找到其对应的最靠左的左端点，满足区间中最大值与最小值的差不超过 \textit{limit}limit。

注意到随着右端点向右移动，左端点也将向右移动，于是我们可以使用滑动窗口解决本题。

为了方便统计当前窗口内的最大值与最小值，我们可以使用平衡树：

语言自带的红黑树，例如 \texttt{C++}C++ 中的 \texttt{std::multiset}std::multiset，\texttt{Java}Java 中的 \texttt{TreeMap}TreeMap；

第三方的平衡树库，例如 \texttt{Python}Python 中的 \texttt{sortedcontainers}sortedcontainers（事实上，这个库的底层实现并不是平衡树，但各种操作的时间复杂度仍然很优秀）；

手写 \texttt{Treap}Treap 一类的平衡树，例如下面的 \texttt{Golang}Golang 代码。

来维护窗口内元素构成的有序集合。

代码

对于 \texttt{Python}Python 语言，力扣平台支持 \texttt{sortedcontainers}sortedcontainers，但其没有默认被导入（import）。读者可以参考 Python Sorted Containers 了解该第三方库的使用方法。

C++JavaPython3Golang

class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        s = SortedList()
        n = len(nums)
        left = right = ret = 0

        while right < n:
            s.add(nums[right])
            while s[-1] - s[0] > limit:
                s.remove(nums[left])
                left += 1
            ret = max(ret, right - left + 1)
            right += 1
        
        return ret
复杂度分析

时间复杂度：O(n \log n)O(nlogn)，其中 nn 是数组长度。向有序集合中添加或删除元素都是 O(\log n)O(logn) 的时间复杂度。每个元素最多被添加与删除一次。

空间复杂度：O(n)O(n)，其中 nn 是数组长度。最坏情况下有序集合将和原数组等大。

方法二：滑动窗口 + 单调队列
思路和解法

在方法一中，我们仅需要统计当前窗口内的最大值与最小值，因此我们也可以分别使用两个单调队列解决本题。

在实际代码中，我们使用一个单调递增的队列 \textit{queMin}queMin 维护最小值，一个单调递减的队列 \textit{queMax}queMax 维护最大值。这样我们只需要计算两个队列的队首的差值，即可知道当前窗口是否满足条件。

代码

C++JavaJavaScriptPython3GolangC

class Solution:
    def longestSubarray(self, nums: List[int], limit: int) -> int:
        n = len(nums)
        queMax, queMin = deque(), deque()
        left = right = ret = 0

        while right < n:
            while queMax and queMax[-1] < nums[right]:
                queMax.pop()
            while queMin and queMin[-1] > nums[right]:
                queMin.pop()
            
            queMax.append(nums[right])
            queMin.append(nums[right])

            while queMax and queMin and queMax[0] - queMin[0] > limit:
                if nums[left] == queMin[0]:
                    queMin.popleft()
                if nums[left] == queMax[0]:
                    queMax.popleft()
                left += 1
            
            ret = max(ret, right - left + 1)
            right += 1
        
        return ret
复杂度分析

时间复杂度：O(n)O(n)，其中 nn 是数组长度。我们最多遍历该数组两次，两个单调队列入队出队次数也均为 O(n)O(n)。

空间复杂度：O(n)O(n)，其中 nn 是数组长度。最坏情况下单调队列将和原数组等大。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/solution/jue-dui-chai-bu-chao-guo-xian-zhi-de-zui-5bki/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''


'''
方法一 滑动窗口
解题思路
维护一直最大值和最小值
维护一个最长数组
sub\_nums增加的条件=\begin{cases} abs(num - curr\_max) <= limit & 判断当前元素是否复合条件，当前元素和数组中最大元素比较\\ abs(num - curr\_min) <= limit & 判断当前元素是否复合条件，当前元素和数组中最小元素比较 \\ abs(curr\_max - curr\_min) <= limit & 判断数组中元素是否符合条件，数组中最大元素和最小元素比较 \end{cases}
sub_nums增加的条件= 
⎩
⎪
⎨
⎪
⎧
​	
  
abs(num−curr_max)<=limit
abs(num−curr_min)<=limit
abs(curr_max−curr_min)<=limit
​	
  
判断当前元素是否复合条件，当前元素和数组中最大元素比较
判断当前元素是否复合条件，当前元素和数组中最小元素比较
判断数组中元素是否符合条件，数组中最大元素和最小元素比较
​	
 

当不复合数组增加条件，则以当前长度向后移动
在向后移动的同时，数组中元素也在在发生变化，所以需要更新数组中的最大最小值
时间复杂度复杂度 0(n)0(n) 空间复杂度 0(n)0(n)
执行过程 举例 nums = [10,1,2,4,7,2] limit = 5


代码
pythonjava
class Solution(object):
    def longestSubarray(self, nums, limit):
        if not nums:
            return 0
        curr_max = nums[0] # 当子数组下最大值 这里初始化为第一个数
        curr_min = nums[0] # 当子数组下最大值 这里初始化为第一个数
        sub_nums = [] # 以数组作为窗口滑动
        for num in nums:
            if abs(num - curr_max) <=  limit and abs(num - curr_min) <=  limit and abs(curr_max - curr_min) <= limit:
                curr_max = max(num,curr_max)
                curr_min = min(num,curr_min)
                sub_nums.append(num)
            else:    
                sub_nums.append(num)
                sub_nums.pop(0)
                curr_max = max(sub_nums) # 当子数组最大值
                curr_min = min(sub_nums) # 当前子数组最小值
        return  len(sub_nums)
'''
