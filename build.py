import os
import json
import time

CHANNEL_DIR = "channels"
OUTPUT_DIR = "templates"

# 自动更新时间版本号
version = f"v{int(time.time())}"

# 确保 templates 目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 遍历 channels 目录
for filename in os.listdir(CHANNEL_DIR):

    if not filename.endswith(".txt"):
        continue

    region_name = filename.replace(".txt", "")

    txt_path = os.path.join(CHANNEL_DIR, filename)

    json_path = os.path.join(OUTPUT_DIR, f"{region_name}.json")

    channels = []

    with open(txt_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                name, url = line.split(",", 1)

                channels.append({
                    "name": name.strip(),
                    "url": url.strip()
                })

            except:
                print(f"格式错误: {line}")

    # 写入对应 json
    with open(json_path, "w", encoding="utf-8") as f:

        json.dump({
            "version": version,
            "channels": channels
        }, f, ensure_ascii=False, indent=2)

    print(f"生成: {json_path}")

# 更新 version.json
with open("version.json", "w", encoding="utf-8") as f:

    json.dump({
        "version": version
    }, f, ensure_ascii=False, indent=2)

print("全部构建完成")
