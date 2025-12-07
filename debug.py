import sys
import os

print("="*30)
print("🔍 正在侦查环境...")
print("="*30)

# 1. 打印 Python 在哪里运行
print(f"Python 解释器位置:\n{sys.executable}")

# 2. 打印 Python 搜索库的路径列表 (sys.path)
print(f"\nPython 搜索路径 (sys.path):")
for p in sys.path:
    print(f" - {p}")

# 3. 尝试导入 langchain 并揪出它的真身
try:
    import langchain
    print(f"\n✅ 成功导入 langchain！")
    print(f"📍 它藏在这个文件里: {langchain.__file__}")
    
    if "Desktop" in langchain.__file__:
        print("\n🚨🚨🚨 破案了！🚨🚨🚨")
        print("你在桌面上有一个叫 'langchain.py' 的文件，或者有个叫 'langchain' 的文件夹！")
        print("Python 把这个假货当成真的库加载了！")
        print("请立刻去桌面把那个文件/文件夹改名或删除！")
        
    elif "site-packages" in langchain.__file__:
        print("\n🤔 路径看起来是正确的 (在 site-packages 里)。")
        print("尝试导入 chains...")
        try:
            from langchain import chains
            print("✅ chains 模块存在！")
        except ImportError as e:
            print(f"❌ chains 模块缺失: {e}")
            print("这说明库文件损坏了。")

except ImportError as e:
    print(f"\n❌ 根本找不到 langchain: {e}")

print("="*30)