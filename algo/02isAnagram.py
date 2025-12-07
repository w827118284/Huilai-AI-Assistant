#有效的字母异位词 (Valid Anagram)
# 例子：

# 输入：s = "anagram", t = "nagaram"

# 输出：True (因为都有 3个a，1个n，1个g，1个r，1个m，只是位置不同)

# 输入：s = "rat", t = "car"

# 输出：False (字母不一样)
def isAnagram(s,t):
    if len(s) != len(t):
        return False
    count = {}
    for char in s:
        count[char] = count.get(char, 0) + 1
    for char in t:
        if char not in count :
            return False
        count[char]  = count[char] - 1
        if count[char] < 0:
            return False
    return True

    # --- 测试代码 ---
print("测试 1 (应该 True):", isAnagram("anagram", "nagaram"))
print("测试 2 (应该 False):", isAnagram("rat", "car"))