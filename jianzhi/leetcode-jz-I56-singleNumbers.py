
'''
面试题56 - I. 数组中数字出现的次数
一个整型数组 nums 里除两个数字之外，其他数字都出现了两次。请写程序找出这两个只出现一次的数字。要求时间复杂度是O(n)，空间复杂度是O(1)。



示例 1：

输入：nums = [4,1,4,6]
输出：[1,6] 或 [6,1]
示例 2：

输入：nums = [1,2,10,4,1,4,3,3]
输出：[2,10] 或 [10,2]


限制：

2 <= nums <= 10000
'''

class Solution0(object):
    def singleNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        #     //输入: [1,2,1,3,2,5]
    # //输出: [3,5]
    # vector<int> singleNumbers(vector<int>& nums) {
    #     int s = 0;
    #     for (int num : nums) {
    #         s ^= num;
    #     }
    #     //s是只出现一次的2个数字的^ 记做数字a,b
    #     //既然a,b 不一样，那么s肯定不是0，那么s的二进制肯定至少有1位（第n位）是1，只有0^1才等于1
    #     //所以a,b 在第n位，要么a是0，b是1 ，要么b是0，a是1    ---->A
    #     //s = 3 ^ 5; 0011 ^ 0101 = 0110 = 6
    #     //假设int是8位
    #     //-6  原码1000 0110
    #     //    反码1111 1001
    #     //    补码1111 1010
    #     //s & (-s)
    #     //  0000 0110
    #     //& 1111 1010
    #     //  0000 0010
    #     //所以k = s & (-s) 就是保留s的最后一个1，并且将其他位变为0  也就是s最后一个1是倒数第二位   --->B
    #     //由于s & (-s)很方便找到一个1 所以用他了，其实找到任何一个1都可以
    #     //根据A和B  我们可以确定 3 和 5 必定可以分到 不同的组里
    #     //同理 1和1 由于二进制完全相同，所有必定分到相同的组里
    #     //同理 2和2 由于二进制完全相同，所有必定分到相同的组里
    #     int k = s & (-s);
    #     //1  0001  第一组
    #     //2  0010  第二组
    #     //1  0001  第一组
    #     //3  0011  第二组
    #     //2  0010  第二组
    #     //5  0101  第一组
    #     //第一组 1 1 5  第二组 2 3 2 这样我们就将2个只有一个的数 分到了2个数组里了
    #     vector<int> rs(2,0);
    #     for(int num : nums){
    #         if(num & k){
    #             //第二组
    #             rs[0] ^= num;
    #         }else{
    #             //第一组
    #             rs[1] ^= num;
    #         }
    #     }
    #     return rs;

        xors = 0
        for i in range(len(nums)):
            xors ^= nums[i]
        # print(xors, bin(xors), bin(-xors))
        # xors = xors & (-xors)
        # print(xors, bin(xors))
        div = 1
        while div & xors == 0:
            div <<= 1
        a, b = 0, 0
        for i in range(len(nums)):
            # print(nums[i] & div, bin(nums[i]), bin(div))
            if nums[i] & div:
                a ^= nums[i]
            else:
                b ^= nums[i]
        return [a, b]


class Solution(object):
    def singleNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        from collections import defaultdict
        d = defaultdict(int)
        for num in nums:
            d[num] += 1
        res = []
        for k, v in d.items():
            if v == 1:
                res.append(k)
        return res


class Solution1(object):
    def singleNumbers(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        from collections import defaultdict
        d = defaultdict(int)
        for num in nums:
            d[num] += 1
        res = []
        for k, v in d.items():
            if v == 1:
                res.append(k)
        return res
        # from collections import Counter
        # hash_map = Counter(nums)
        # res = []
        # for k, v in hash_map.items():
        #     if v == 1:
        #         res.append(k)
        # return res

'''
前菜
本题和主站260 是一样的. 除了这个，主站还有136和137。 总共加起来本系列一共三道题。 三道题全部都是位运算的套路，如果你想练习位运算的话，不要错过哦～～

异或的性质
两个数字异或的结果a^b是将 a 和 b 的二进制每一位进行运算，得出的数字。 运算的逻辑是
如果同一位的数字相同则为 0，不同则为 1

异或的规律

任何数和本身异或则为0

任何数和 0 异或是本身

OK，我们来看下这三道题吧。

136. 只出现一次的数字1
题目大意是除了一个数字出现一次，其他都出现了两次，让我们找到出现一次的数。我们执行一次全员异或即可。

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        single_number = 0
        for num in nums:
            single_number ^= num
        return single_number
复杂度分析

时间复杂度：O(N)O(N)，其中N为数组长度。
空间复杂度：O(1)O(1)
137. 只出现一次的数字2
题目大意是除了一个数字出现一次，其他都出现了三次，让我们找到出现一次的数。 灵活运用位运算是本题的关键。

Python3:

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for i in range(32):
            cnt = 0  # 记录当前 bit 有多少个1
            bit = 1 << i  # 记录当前要操作的 bit
            for num in nums:
                if num & bit != 0:
                    cnt += 1
            if cnt % 3 != 0:
                # 不等于0说明唯一出现的数字在这个 bit 上是1
                res |= bit

        return res - 2 ** 32 if res > 2 ** 31 - 1 else res
为什么Python最后需要对返回值进行判断？
如果不这么做的话测试用例是[-2,-2,1,1,-3,1,-3,-3,-4,-2] 的时候，就会输出 4294967292。 
其原因在于Python是动态类型语言，在这种情况下其会将符号位置的1看成了值，而不是当作符号“负数”。 这是不对的。 正确答案应该是 - 4，
-4的二进制码是 1111...100，就变成 2^32-4=4294967292，解决办法就是 减去 2 ** 32 。

之所以这样不会有问题的原因还在于题目限定的数组范围不会超过 2 ** 32

JavaScript:

var singleNumber = function(nums) {
  let res = 0;
  for (let i = 0; i < 32; i++) {
    let cnt = 0;
    let bit = 1 << i;
    for (let j = 0; j < nums.length; j++) {
      if (nums[j] & bit) cnt++;
    }
    if (cnt % 3 != 0) res = res | bit;
  }
  return res;
};
复杂度分析

时间复杂度：O(N)O(N)，其中N为数组长度。
空间复杂度：O(1)O(1)
645. 错误的集合
和上面的137. 只出现一次的数字2思路一样。

这题没有限制空间复杂度，因此直接hashmap 存储一下没问题。 不多说了，我们来看一种空间复杂度O(1)O(1)的解法。

我们和137. 只出现一次的数字2思路基本一样，我直接复用了代码。

这里我们的思路是，将nums的所有索引提取出一个数组idx，那么由idx和nums组成的数组构成singleNumbers的输入，其输出是唯二不同的两个数。

但是我们不知道哪个是缺失的，哪个是重复的，因此我们需要重新进行一次遍历，判断出哪个是缺失的，哪个是重复的。

class Solution:
    def singleNumbers(self, nums: List[int]) -> List[int]:
        ret = 0  # 所有数字异或的结果
        a = 0
        b = 0
        for n in nums:
            ret ^= n
        # 找到第一位不是0的
        h = 1
        while(ret & h == 0):
            h <<= 1
        for n in nums:
            # 根据该位是否为0将其分为两组
            if (h & n == 0):
                a ^= n
            else:
                b ^= n

        return [a, b]

    def findErrorNums(self, nums: List[int]) -> List[int]:
        nums = [0] + nums
        idx = []
        for i in range(len(nums)):
            idx.append(i)
        a, b = self.singleNumbers(nums + idx)
        for num in nums:
            if a == num:
                return [a, b]
        return [b, a]

复杂度分析

时间复杂度：O(N)O(N)
空间复杂度：O(1)O(1)
260. 只出现一次的数字3(就是本题)
题目大意是除了两个数字出现一次，其他都出现了两次，让我们找到这个两个数。

我们进行一次全员异或操作，得到的结果就是那两个只出现一次的不同的数字的异或结果。

我们刚才讲了异或的规律中有一个任何数和本身异或则为0， 因此我们的思路是能不能将这两个不同的数字分成两组 A 和 B。
分组需要满足两个条件.

两个独特的的数字分成不同组

相同的数字分成相同组

这样每一组的数据进行异或即可得到那两个数字。

问题的关键点是我们怎么进行分组呢？

由于异或的性质是，同一位相同则为 0，不同则为 1. 我们将所有数字异或的结果一定不是 0，也就是说至少有一位是 1.

我们随便取一个， 分组的依据就来了， 就是你取的那一位是 0 分成 1 组，那一位是 1 的分成一组。
这样肯定能保证2. 相同的数字分成相同组, 不同的数字会被分成不同组么。 很明显当然可以， 因此我们选择是 1，也就是
说两个独特的的数字在那一位一定是不同的，因此两个独特元素一定会被分成不同组。

class Solution:
    def singleNumbers(self, nums: List[int]) -> List[int]:
        ret = 0  # 所有数字异或的结果
        a = 0
        b = 0
        for n in nums:
            ret ^= n
        # 找到第一位不是0的
        h = 1
        while(ret & h == 0):
            h <<= 1
        for n in nums:
            # 根据该位是否为0将其分为两组
            if (h & n == 0):
                a ^= n
            else:
                b ^= n

        return [a, b]
复杂度分析

时间复杂度：O(N)O(N)，其中N为数组长度。
空间复杂度：O(1)O(1)
更多题解可以访问我的LeetCode题解仓库：https://github.com/azl397985856/leetcode 。 目前已经接近30K star啦。

大家也可以关注我的公众号《脑洞前端》获取更多更新鲜的LeetCode题解

作者：fe-lucifer
链接：https://leetcode-cn.com/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/solution/zhi-chu-xian-yi-ci-de-shu-xi-lie-wei-yun-suan-by-a/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
'''
