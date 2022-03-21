import glob
import cv2 as cv
from pascal_voc_writer import Writer
# pip install pascal-voc-writer


labels = ['-','person','bicycle','car','motorcycle','airplane','bus','train','truck','boat','traffic light','fire hydrant','-',
'stop sign','parking meter','bench','bird','cat','dog','horse','sheep','cow','elephant','bear','zebra','giraffe','-','backpack',
'umbrella','-','-','handbag','tie','suitcase','frisbee','skis','snowboard','sports ball','kite','baseball bat','baseball glove',
'skateboard','surfboard','tennis racket','bottle','-','wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich',
'orange','broccoli','carrot','hot dog','pizza','donut','cake','chair','couch','potted plant','bed','-','dining table','-','-',
'toilet','-','tv','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator','-','book',
'clock','vase','scissors','teddy bear','hair drier','toothbrush','-','face','box']





def yolo_to_voc(line, img_width, img_height):
    
    c,n_cx,n_cy,n_w,n_h = line.split(" ")
    name = labels[int(c)]
    x_rect_mid = float(n_cx)
    y_rect_mid = float(n_cy)
    width_rect = float(n_w)
    height_rect = float(n_h)
    x_min_rect = ((2 * x_rect_mid * img_width)  - (width_rect * img_width))   / 2
    x_max_rect = ((2 * x_rect_mid * img_width)  + (width_rect * img_width))   / 2
    y_min_rect = ((2 * y_rect_mid * img_height) - (height_rect * img_height)) / 2
    y_max_rect = ((2 * y_rect_mid * img_height) + (height_rect * img_height)) / 2


    return name, x_min_rect, y_min_rect, x_max_rect , y_max_rect

if __name__ == "__main__":

    i_path = "./boxes/images/train/*"
    l_path = "./boxes/labels/train/"
    s_path = "./boxes/xml_labels/train/"
    images = glob.glob(i_path)


    for file in images:
        print(file)
        img = cv.imread(file)
        img_h, img_w, _ = img.shape
        label_name = file.split("/")[-1].split(".")[0]+".txt"

        # Writer(path, width, height)
        writer = Writer(file, img_w, img_h)
        
        with open(l_path+label_name, "r") as f:
            lines = f.readlines()
            for line in lines:
                print(line)
                name, xmin, ymin, xmax, ymax = yolo_to_voc(line,img_w,img_h)
                # ::addObject(name, xmin, ymin, xmax, ymax)
                writer.addObject(name, int(xmin), int(ymin), int(xmax), int(ymax))
        
        # ::save(path)
        writer.save(s_path+label_name.split(".")[0]+".xml")
