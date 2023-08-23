import glob
import shutil
import os
import json

xception_result_dic = {}

with open('xception_result.json', 'r') as f:
    xception_result_dic = json.load(f)

for idx, result in xception_result_dic.items():
    dst_dir = f"./xception/{idx}"
    for k, v in result.items():
        if k == "result":
            for img_path in v:
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                shutil.copy(img_path[0], dst_dir)