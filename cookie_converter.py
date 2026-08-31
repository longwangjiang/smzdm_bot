#!/usr/bin/env python3
"""
Cookie转换工具
将抓包获取的 key: value 格式转换为脚本需要的 cookie 字符串
"""

print("=" * 50)
print("什么值得买 Cookie 转换工具")
print("=" * 50)
print()
print("请粘贴抓包获取的cookie (key: value格式)")
print("粘贴完成后按两次回车:")
print()

lines = []
while True:
    line = input()
    if line == "":
        if len(lines) > 0 and lines[-1] == "":
            break
        lines.append(line)
    else:
        lines.append(line)

# 解析并转换
cookies = []
for line in lines:
    line = line.strip()
    if not line or ":" not in line:
        continue
    key, value = line.split(":", 1)
    cookies.append(f"{key.strip()}={value.strip()}")

result = ";".join(cookies)

print()
print("=" * 50)
print("转换结果 (复制下面的内容):")
print("=" * 50)
print()
print(result)
print()
print("=" * 50)
print(f"Cookie长度: {len(result)}")
print("=" * 50)
