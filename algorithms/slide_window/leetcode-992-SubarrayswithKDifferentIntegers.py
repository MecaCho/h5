# encoding=utf8

'''
992. Subarrays with K Different Integers
Given an array A of positive integers, call a (contiguous, not necessarily distinct) subarray of A good if the number of different integers in that subarray is exactly K.

(For example, [1,2,3,1,2] has 3 different integers: 1, 2, and 3.)

Return the number of good subarrays of A.



Example 1:

Input: A = [1,2,1,2,3], K = 2
Output: 7
Explanation: Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2].
Example 2:

Input: A = [1,2,1,3,4], K = 3
Output: 3
Explanation: Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].


Note:

1 <= A.length <= 20000
1 <= A[i] <= A.length
1 <= K <= A.length


992. K 个不同整数的子数组
给定一个正整数数组 A，如果 A 的某个子数组中不同整数的个数恰好为 K，则称 A 的这个连续、不一定独立的子数组为好子数组。

（例如，[1,2,3,1,2] 中有 3 个不同的整数：1，2，以及 3。）

返回 A 中好子数组的数目。



示例 1：

输入：A = [1,2,1,2,3], K = 2
输出：7
解释：恰好由 2 个不同整数组成的子数组：[1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2].
示例 2：

输入：A = [1,2,1,3,4], K = 3
输出：3
解释：恰好由 3 个不同整数组成的子数组：[1,2,1,3], [2,1,3], [1,3,4].


提示：

1 <= A.length <= 20000
1 <= A[i] <= A.length
1 <= K <= A.length
'''


class Solution(object):
    def subarraysWithKDistinct(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """

        def max_sub_arr(nums, K):
            l, r = 0, 0
            res = 0
            length = len(nums)
            freq = [0] * (length + 1)
            count = 0
            while r < length:
                if freq[nums[r]] == 0:
                    count += 1

                freq[nums[r]] += 1
                r += 1

                while count > K:
                    freq[nums[l]] -= 1
                    if freq[nums[l]] == 0:
                        count -= 1
                    l += 1

                res += r - l

            return res

        return max_sub_arr(A, K) - max_sub_arr(A, K - 1)




# solutions

'''
最初直觉使用双指针算法遇到的问题
对于一个固定的左边界来说，满足「恰好存在 K 个不同整数的子区间」的右边界 不唯一，且形成区间。

示例 1：左边界固定的时候，恰好存在 22 个不同整数的子区间为 [1,2],[1,2,1],[1,2,1,2][1,2],[1,2,1],[1,2,1,2] ，总数为 33。其值为下标 3 - 1 + 13−1+1，即区间 [1..3][1..3] 的长度。



须要找到左边界固定的情况下，满足「恰好存在 K 个不同整数的子区间」最小右边界和最大右边界。对比以前我们做过的，使用双指针解决的问题的问法基本都会出现「最小」、「最大」这样的字眼。

76. 最小覆盖子串；
209. 长度最小的子数组；
159. 至多包含两个不同字符的最长子串；
424. 替换后的最长重复字符。
把原问题转换成为容易求解的问题
把「恰好」改成「最多」就可以使用双指针一前一后交替向右的方法完成，这是因为 对于每一个确定的左边界，最多包含 KK 种不同整数的右边界是唯一确定的，并且在左边界向右移动的过程中，右边界或者在原来的地方，或者在原来地方的右边。

而「最多存在 KK 个不同整数的子区间的个数」与「恰好存在 K 个不同整数的子区间的个数」的差恰好等于「最多存在 K - 1K−1 个不同整数的子区间的个数」。



因为原问题就转换成为求解「最多存在 KK 个不同整数的子区间的个数」与 「最多存在 K - 1K−1 个不同整数的子区间的个数」，它们其实是一个问题。

方法：双指针（滑动窗口）
实现函数 atMostWithKDistinct(A, K) ，表示「最多存在 KK 个不同整数的子区间的个数」。于是 atMostWithKDistinct(A, K) - atMostWithKDistinct(A, K - 1) 即为所求。

参考代码：

Java

public class Solution {

    public int subarraysWithKDistinct(int[] A, int K) {
        return atMostKDistinct(A, K) - atMostKDistinct(A, K - 1);
    }

    /**
     * @param A
     * @param K
     * @return 最多包含 K 个不同整数的子区间的个数
     */
    private int atMostKDistinct(int[] A, int K) {
        int len = A.length;
        int[] freq = new int[len + 1];

        int left = 0;
        int right = 0;
        // [left, right) 里不同整数的个数
        int count = 0;
        int res = 0;
        // [left, right) 包含不同整数的个数小于等于 K
        while (right < len) {
            if (freq[A[right]] == 0) {
                count++;
            }
            freq[A[right]]++;
            right++;

            while (count > K) {
                freq[A[left]]--;
                if (freq[A[left]] == 0) {
                    count--;
                }
                left++;
            }
            // [left, right) 区间的长度就是对结果的贡献
            res += right - left;
        }
        return res;
    }
}
复杂度分析：

时间复杂度：O(N)O(N)，这里 NN 是输入数组的长度；
空间复杂度：O(N)O(N)，使用了常数个变量、频数数组的长度为 N + 1N+1。
总结
使用双指针（滑动窗口、两个变量一前一后交替向后移动）解决的问题通常都和这个问题要问的结果有关。以我们在题解中给出的 4 道经典问题为例：

76. 最小覆盖子串：求一个字符串的子串覆盖另一个字符串的长度一定是问「最小」，而不会问「最大」，因为最大一定是整个字符串；
209. 长度最小的子数组：所有元素都是正整数，且子区间里所有元素的和大于等于定值 s 的子区间一定是问长度「最小」，而不会问「最多」，因为最多也一定是整个数组的长度；
159. 至多包含两个不同字符的最长子串：最多包含两个不同字符一定是问「最长」才有意义，因为长度更长的子串可能会包含更多的字符；
424. 替换后的最长重复字符：替换的次数 k 是定值，替换以后字符全部相等的子串也一定只会问「最长」。
练习
提示：在做这些问题的时候，一定要思考清楚为什么可以采用双指针（滑动窗口）的方式解决如上的问题，为什么左右指针向右移动的时候可以不回头。

713. 乘积小于 K 的子数组；
904. 水果成篮 ；
795. 区间子数组个数；
1358. 包含所有三种字符的子字符串数目；
467. 环绕字符串中唯一的子字符串；
340. 至多包含 K 个不同字符的最长子串。

作者：LeetCode
链接：https://leetcode-cn.com/problems/subarrays-with-k-different-integers/solution/k-ge-bu-tong-zheng-shu-de-zi-shu-zu-by-l-ud34/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''


# sokutions1

'''
方法一：滑动窗口
思路及算法

我们容易发现，对于任意一个右端点，可能存在一系列左端点与其对应，满足两端点所指区间对应的子数组内恰有 KK 个不同整数。因此可能有 O(n^2)O(n 
2
 ) 个子数组满足条件。因此无法暴力解决该题。

分析这些左端点，我们可以证明：对于任意一个右端点，能够与其对应的左端点们必然相邻。

证明非常直观，假设区间 [l_1,r][l 
1
​	
 ,r] 和 [l_2,r][l 
2
​	
 ,r] 为满足条件的数组（不失一般性，设 l_1\leq l_2l 
1
​	
 ≤l 
2
​	
 ）。现在我们设存在一个 ll 满足 l_1 \leq l \leq l_2l 
1
​	
 ≤l≤l 
2
​	
 ，那么区间 [l,r][l,r] 作为 [l_1,r][l 
1
​	
 ,r] 的子数组，其中的不同整数数量必然不超过 KK。同理，区间 [l,r][l,r] 作为 [l_2,r][l 
2
​	
 ,r] 的父数组，其中的不同整数数量必然不少于 KK。那么可知区间 [l,r][l,r] 中的不同整数数量即为 KK。

这样我们就可以用一个区间 [l_1,l_2][l 
1
​	
 ,l 
2
​	
 ] 来代表能够与右端点 rr 对应的左端点们。

同时，我们可以发现：当右端点向右移动时，左端点区间也同样向右移动。因为当我们在原有区间的右侧添加元素时，区间中的不同整数数量不会减少而只会不变或增加，因此我们需要在区间左侧删除一定元素，以保证区间内整数数量仍然为 KK。

于是我们可以用滑动窗口解决本题，和普通的滑动窗口解法的不同之处在于，我们需要记录两个左指针 \textit{left}_1left 
1
​	
  与 \textit{left}_2left 
2
​	
  来表示左端点区间 [\textit{left}_1,\textit{left}_2)[left 
1
​	
 ,left 
2
​	
 )。第一个左指针表示极大的包含 KK 个不同整数的区间的左端点，第二个左指针则表示极大的包含 K-1K−1 个不同整数的区间的左端点。

代码

C++JavaJavaScriptPython3GolangC

class Solution:
    def subarraysWithKDistinct(self, A: List[int], K: int) -> int:
        n = len(A)
        num1, num2 = collections.Counter(), collections.Counter()
        tot1 = tot2 = 0
        left1 = left2 = right = 0
        ret = 0

        for right, num in enumerate(A):
            if num1[num] == 0:
                tot1 += 1
            num1[num] += 1
            if num2[num] == 0:
                tot2 += 1
            num2[num] += 1
            
            while tot1 > K:
                num1[A[left1]] -= 1
                if num1[A[left1]] == 0:
                    tot1 -= 1
                left1 += 1
            while tot2 > K - 1:
                num2[A[left2]] -= 1
                if num2[A[left2]] == 0:
                    tot2 -= 1
                left2 += 1
            
            ret += left2 - left1
        
        return ret
复杂度分析

时间复杂度：O(n)O(n)，其中 nn 是数组长度。我们至多只需要遍历该数组三次（右指针和两个左指针各一次）。

空间复杂度：O(n)O(n)，其中 nn 是数组长度。我们需要记录每一个数的出现次数，本题中数的大小不超过数组长度。

作者：LeetCode-Solution
链接：https://leetcode-cn.com/problems/subarrays-with-k-different-integers/solution/k-ge-bu-tong-zheng-shu-de-zi-shu-zu-by-l-9ylo/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''
