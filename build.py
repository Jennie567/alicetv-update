import os
import json
import time

CHANNEL_DIR = "channels"
OUTPUT_DIR = "templates"

version = f"v{int(time.time())}"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(CHANNEL_DIR):

    if not filename.endswith(".txt"):
        continue

    region_name = filename.replace(".txt", "")

    txt_path = os.path.join(CHANNEL_DIR, filename)

    json_path = os.path.join(OUTPUT_DIR, f"{region_name}.json")

    channels = []

    current_group = "其他频道"

    with open(txt_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:

                name, value = line.split(",", 1)

                name = name.strip()
                value = value.strip()

                # 分组行
                if value == "#genre#":

                    current_group = name
                    continue

                # 普通频道
                channel = {
                    "id": name,
                    "name": name,
                    "group": current_group,
                    "logo": f"{name}.png",
                    "src": value
                }

                channels.append(channel)

            except Exception as e:

                print(f"格式错误: {line}")
                print(e)

    result = {
        "version": version,
        "channels": channels
    }

    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"生成: {json_path}")

# 更新 version.json
with open("version.json", "w", encoding="utf-8") as f:

    json.dump({
        "version": version
    }, f, ensure_ascii=False, indent=2)

print("全部构建完成")
