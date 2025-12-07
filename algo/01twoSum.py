#题目：两数之和 (Two Sum)

#给定一个整数列表 nums 和一个目标值 target，请找出和为目标值的两个整数，并返回它们的下标。

#例子： 输入：nums = [2, 7, 11, 15], target = 9 输出：[0, 1] (因为 2 + 7 = 9)
def two_sum(nums, target):
    memo = {}
    for i,num in enumerate(nums):
        need = target - num
        if need in memo:
            return [memo[need], i]
        memo[num] = i
    return []  # Return an empty list if no solution is found

    # --- 测试代码 ---
print("测试开始...")
result = two_sum([2, 7, 11, 15], 18)
print(f"结果是: {result}") # 应该输出 [0, 2]