from __future__ import division
import os
import numpy as np
import json
from scipy import io as scio
import pickle

def get_citypersons(root_dir='data/cityperson', type='train'):
    all_img_path = os.path.join(root_dir, 'images')
    all_anno_path = os.path.join(root_dir, 'annotations')
    rows, cols = 1024, 2048

    anno_path = os.path.join(all_anno_path, 'anno_' + type + '.mat')
    image_data = []
    annos = scio.loadmat(anno_path)
    index = 'anno_' + type + '_aligned'
    valid_count = 0
    iggt_count = 0
    box_count = 0

    for l in range(len(annos[index][0])):
        anno = annos[index][0][l]
        cityname = anno[0][0][0][0]
        imgname = anno[0][0][1][0]
        gts = anno[0][0][2]
        img_path = os.path.join(all_img_path, type + '/' + cityname + '/' + imgname)
        boxes = []
        ig_boxes = []
        vis_boxes = []
        for i in range(len(gts)):
            label, x1, y1, w, h = gts[i, :5]
            x1, y1 = max(int(x1), 0), max(int(y1), 0)
            w, h = min(int(w), cols - x1 - 1), min(int(h), rows - y1 - 1)
            xv1, yv1, wv, hv = gts[i, 6:]
            xv1, yv1 = max(int(xv1), 0), max(int(yv1), 0)
            wv, hv = min(int(wv), cols - xv1 - 1), min(int(hv), rows - yv1 - 1)

            if label == 1 and h >= 50:
                box = np.array([int(x1), int(y1), int(x1) + int(w), int(y1) + int(h)])
                boxes.append(box)
                vis_box = np.array([int(xv1), int(yv1), int(xv1) + int(wv), int(yv1) + int(hv)])
                vis_boxes.append(vis_box)
            else:
                ig_box = np.array([int(x1), int(y1), int(x1) + int(w), int(y1) + int(h)])
                ig_boxes.append(ig_box)
        boxes = np.array(boxes)
        vis_boxes = np.array(vis_boxes)
        ig_boxes = np.array(ig_boxes)

        if len(boxes) > 0:
            valid_count += 1
        annotation = {}
        annotation['filepath'] = img_path
        box_count += len(boxes)
        iggt_count += len(ig_boxes)
        annotation['bboxes'] = boxes
        annotation['vis_bboxes'] = vis_boxes
        annotation['ignoreareas'] = ig_boxes
        image_data.append(annotation)

    return image_data

# /data/caltech/images -> /data/cache/caltech/**
def get_caltech(root_dir='data/caltech', type='train_gt'):

    cache_anno_path = os.path.join('/'.join(root_dir.split('/')[:-2]), 'cache', 'caltech')
    cache_file = os.path.join(cache_anno_path, f'{type}')

    with open(cache_file, 'rb') as fid:
        cache_data = pickle.load(fid, encoding='iso-8859-1')
    
    return cache_data

def get_tju(root_dir='data/tju', split='train'):
    all_img_path = os.path.join(root_dir, "images")
    all_anno_path = os.path.join(root_dir, "annotations")
    anno_path = os.path.join(all_anno_path, f"{split}.json")
    image_data = dict()
    valid_count = 0
    iggt_count = 0
    box_count = 0
    with open(anno_path) as f: anno_data = json.load(f)
    for im in anno_data["images"]: 
        image_data[im["id"]] = dict(image_id=im["id"], filepath=os.path.join(all_img_path, im["file_name"]), bboxes=list(), ignoreareas=list())
    for anno in anno_data["annotations"]:
        bbox = list(map(int, anno["bbox"]))
        bbox = np.array([bbox[0], bbox[1], bbox[0]+bbox[2], bbox[1]+bbox[3]])
        ignore = 1 if "ignore" in anno and anno["ignore"] == 1 else 0
        if ignore or anno["iscrowd"] == 1: image_data[anno["image_id"]]["ignoreareas"].append(bbox)
        else: image_data[anno["image_id"]]["bboxes"].append(bbox)
    for im_dict in image_data.values():
        im_dict["bboxes"] = np.array(im_dict["bboxes"])
        im_dict["ignoreareas"] = np.array(im_dict["ignoreareas"])
    return list(image_data.values())

