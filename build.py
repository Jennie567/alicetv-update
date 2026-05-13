import os
import json
import time

CHANNEL_DIR = "channels"

result = {
    "version": f"v{int(time.time())}",
    "regions": {}
}

for filename in os.listdir(CHANNEL_DIR):

    if not filename.endswith(".txt"):
        continue

    region_name = filename.replace(".txt", "")

    region_channels = []

    filepath = os.path.join(CHANNEL_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            try:
                name, url = line.split(",", 1)

                channel = {
                    "name": name.strip(),
                    "url": url.strip()
                }

                region_channels.append(channel)

            except:
                pass

    result["regions"][region_name] = region_channels

with open("channels.json", "w", encoding="utf-8") as f:

    json.dump(result, f, ensure_ascii=False, indent=2)

with open("version.json", "w", encoding="utf-8") as f:

    json.dump({
        "version": result["version"]
    }, f, ensure_ascii=False, indent=2)

print("构建完成")
