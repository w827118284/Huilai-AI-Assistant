class Solution(object):
    def lengthOfLongestSubstring(self, s):
        char_map = {}
        left = 0
        max_length = 0
        for i , char in enumerate(s):
            if char in char_map and char_map[char] >= left:
                left = char_map[char] + 1
            char_map[char] = i
            max_length = max(max_length, i - left + 1)
        return max_length
# --- 本地测试 ---
solver = Solution()
print(solver.lengthOfLongestSubstring("abcabcbb")) # 应该输出 3
print(solver.lengthOfLongestSubstring("pwwkew"))   # 应该输出 3 ("wke")