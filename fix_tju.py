# VLPD codebase does not use the real id of the images but instead the position they come in the annotation file
import json, os
with open(os.path.join("TJU-DHD-Traffic", "val.json")) as f: test = json.load(f)
imid_map = dict()
for i, im in enumerate(test["images"]):
    imid_map[im["id"]] = i+1
    test["images"][i]["id"] = i+1
for i, ann in enumerate(test["annotations"]): test["annotations"][i]["image_id"] = imid_map[ann["image_id"]]
with open(os.path.join("TJU-DHD-Traffic", "new_val.json")) as f: json.dump(test, f)