import json
import cv2
import os


def make_cropped_label(x, y, w, h, file_name, folder_path):
    im = cv2.imread('./input/image1.png')
    # y is starting y-axis and y+h is end of y-axis
    # x is staring x-axis and x+w is end of x-axis
    cropped = im[y:y + h, x:x + w]
    # if directory exist then do nothing if not then it will make
    os.makedirs(os.path.dirname(folder_path), exist_ok=True)
    cv2.imwrite(folder_path + str(y) + '$' + file_name, cropped)


def cropped_images():
    with open('input/json/test.json', 'r') as j:
        dicts = json.load(j)
    json_name = dicts[0]
    for box in json_name["regions"]:
        box_dict = box['bounding_box']
        make_cropped_label(box_dict['x'], box_dict['y'], box_dict['w'], box_dict['h'], json_name.get("image_name"),
                           './output/croped/')


cropped_images()
