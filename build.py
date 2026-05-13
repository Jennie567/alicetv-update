import os
import json
from datetime import datetime

CHANNEL_DIR = "channels"
OUTPUT_DIR = "templates"

# 时间版本号
version = datetime.now().strftime("%Y.%m.%d.%H%M")

# 更新时间
updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 总频道数
total_channels = 0

# 遍历所有 txt
for filename in os.listdir(CHANNEL_DIR):

    if not filename.endswith(".txt"):
        continue

    region_name = filename.replace(".txt", "")

    txt_path = os.path.join(CHANNEL_DIR, filename)

    json_path = os.path.join(
        OUTPUT_DIR,
        f"{region_name}.json"
    )

    channels = []

    current_group = "其他频道"

    # 读取 txt
    with open(txt_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:

                name, value = line.split(",", 1)

                name = name.strip()
                value = value.strip()

                # 分组
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

    # 统计频道数
    total_channels += len(channels)

    # 生成地区 json
    result = {
        "version": version,
        "updated_at": updated_at,
        "region": region_name,
        "channel_count": len(channels),
        "channels": channels
    }

    with open(json_path, "w", encoding="utf-8") as f:

        json.dump(
            result,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"生成: {json_path}")

# 生成全局 version.json
with open("version.json", "w", encoding="utf-8") as f:

    json.dump({
        "version": version,
        "updated_at": updated_at,
        "total_channels": total_channels
    }, f, ensure_ascii=False, indent=2)

print("全部构建完成")
print(f"版本号: {version}")
print(f"总频道数: {total_channels}")
