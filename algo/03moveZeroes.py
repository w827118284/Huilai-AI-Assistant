class Solution(object):
    def moveZeroes(self, nums):
        j = 0

        for i  in range(len(nums)):
            if nums[i] != 0:
                nums[j] = nums[i]
                j += 1
    
        for i in range(j, len(nums)):
            nums[i] = 0

# --- 本地测试代码 (提交到 LeetCode 时不要复制下面这几行) ---
# 1. 创建一个“解决方案”的实例
solver = Solution()

# 2. 准备数据
my_list = [0, 1, 0, 3, 12]
print("处理前:", my_list)

# 3. 调用类里面的方法
solver.moveZeroes(my_list)

print("处理后:", my_list)