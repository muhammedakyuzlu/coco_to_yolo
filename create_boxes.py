from xmlrpc.client import NOT_WELLFORMED_ERROR
import cv2 as cv
import numpy as np
import random
import glob



def RGBA(img_path,box_path,name,p):
    img = cv.imread(img_path,cv.IMREAD_UNCHANGED)
    img = cv.cvtColor(img, cv.COLOR_RGB2RGBA)
    # Then assign the mask to the last channel of the image
    img[:, :, 3] = 0
    box = cv.imread(box_path,cv.IMREAD_UNCHANGED)

    # get the dimensions
    img_h, img_w, _ = img.shape
    box_h, box_w, _ = box.shape

    # percent of original size   0-1
    scale_percent = (img_w / p) / box_w
    

    width  = int(box_w * scale_percent)
    height = int(box_h * scale_percent)
    dim = (width, height)
    resized_box = cv.resize(box, dim, interpolation = cv.INTER_AREA)
    x = random.randint(0,img_w-width)
    y = random.randint(0,img_h-height)
    where_to_overwrite = img[y:y+height,x:x+width,3] < resized_box[:,:,3]
    img[y:y+height,x:x+width,:][where_to_overwrite] = resized_box[where_to_overwrite]


    cv.imwrite(img_path, img)

    # return the coordinates
    return [x,y,width,height, img_h, img_w ]
     

def yoloV5_annotation(bbox,image_name,txt_path,c):
    # class_id center_x center_y width height
    # top left x,y
    x,y,width,height, img_h, img_w  = bbox

    cx = x + width / 2
    cy = y + height / 2

    n_cx = cx / img_w
    n_cy = cy / img_h

    n_w = width / img_w
    n_h = height / img_h

    file = open(txt_path+image_name+".txt","a")
    s = "\n{} {} {} {} {}".format(c,n_cx,n_cy,n_w,n_h )
    file.write(s)
    file.close()


    
    

if __name__ == "__main__":
    # /home/muhammed/Documents/work/datasets/box
    images_path = "/home/muhammed/Documents/work/datasets/box/dataset/images/train/*.jpg"
    boxes_path  = "/home/muhammed/Documents/work/datasets/box/boxes/*.png"
    txt_path = "/home/muhammed/Documents/work/datasets/box/dataset/labels/train/"

    images = glob.glob(images_path)
    boxes =  glob.glob(boxes_path)
    
    l = [2,4,8,16]
    idx_b = 0
    idx_l=0
    e = 0
    for img_path in images:
        # take the next box
        idx_b = (idx_b + 1) % len(boxes)
        box_path = boxes[idx_b]

        # take the scale
        idx_l = (idx_l + 1) % len(l)
        p = l[idx_l]
        # write the bbox to the text file with the same name as the image
        image_name  = img_path.split("/")[-1].split(".")[0]
        # add the box to the image and return the bbox
        # bbox = add(img,box,image_name)
        try:    
            bbox = RGBA(img_path,box_path,image_name,p)
            yoloV5_annotation(bbox,image_name,txt_path,93)
        except:
            e +=1
            print(e)
