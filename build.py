import os
import json
from datetime import datetime

CHANNEL_DIR = "channels"
OUTPUT_DIR = "templates"
M3U_DIR = "m3u"

LOGO_BASE_URL = "https://alicetv-update.pages.dev/logos"

# 时间版本号
version = datetime.now().strftime("%Y.%m.%d.%H%M")

# 更新时间
updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(M3U_DIR, exist_ok=True)

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

    m3u_path = os.path.join(
        M3U_DIR,
        f"{region_name}.m3u"
    )

    channels = []

    m3u_lines = ["#EXTM3U"]

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
                # 兼容：
                # 央视-卫视,#genre#
                # 央视-卫视,udp://#genre#
                # 央视-卫视,rtp://#genre#
                lower_value = value.lower()

                if lower_value in ("#genre#", "udp://#genre#", "rtp://#genre#"):
                    current_group = name
                    continue

                # M3U 使用原始播放地址
                m3u_src = value

                # 兼容旧版 AliceTV：
                # GitHub txt 可以写 rtp:// 或 udp://
                # 但生成 templates/*.json 时自动去掉协议头
                if lower_value.startswith("rtp://"):
                    value = value[6:].strip()

                elif lower_value.startswith("udp://"):
                    value = value[6:].strip()

                # 普通频道
                channel = {
                    "id": name,
                    "name": name,
                    "group": current_group,
                    "logo": f"{name}.png",
                    "src": value
                }

                channels.append(channel)

                # 生成 M3U 条目
                logo_url = f"{LOGO_BASE_URL}/{name}.png"

                m3u_lines.append(
                    f'#EXTINF:-1 tvg-id="{name}" tvg-name="{name}" tvg-logo="{logo_url}" group-title="{current_group}",{name}'
                )
                m3u_lines.append(m3u_src)

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

    # 生成地区 m3u
    with open(m3u_path, "w", encoding="utf-8") as f:

        f.write("\n".join(m3u_lines))
        f.write("\n")

    print(f"生成: {m3u_path}")

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
