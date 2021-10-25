# convert the coco annotation to yolo annotation
# the coco annotation can be fond in coco web site https://cocodataset.org/#download
# this file tested on the coco 2017 version
# no licence required :)



import json


def convert_coco_to_yolo(annotationFilePath,pathToSave):

    # load annotation file
    annotation_data = json.load(open(annotationFilePath))
    check_set = set()

    # get images height and width from the annotation file and but them in dictionary with key as image name
    images_data = {}
    for i in range(len(annotation_data['images'])):
        images_data[str(annotation_data['images'][i]['file_name']).split('.')[0]] = {
            "height": annotation_data['images'][i]['height'],
            "width":   annotation_data['images'][i]['width'],
            }

    # go throw the annotations
    for i in range(len(annotation_data['annotations'])):
        
        image_id    =  str(annotation_data['annotations'][i]['image_id'])   
        coco_bbox   =  annotation_data['annotations'][i]['bbox']        # list 4 elements top left point --> (x,y) , width and height
        category_id =  annotation_data['annotations'][i]['category_id'] # int


        # all the images id consists of 12 digits 
        number_of_zeros = 12 - len(image_id)
        image_id =   str('0'*number_of_zeros) +  image_id

        # get image height and width for the specific image
        height = images_data[image_id]['height']
        width  = images_data[image_id]['width']
        
        # convert the boundring box from coco format to yolo format
        yolo_bbox = convert_bbox(height,width,coco_bbox)
        content   = f"{category_id} {yolo_bbox[0]} {yolo_bbox[1]} {yolo_bbox[2]} {yolo_bbox[3]}"

        # Prepare for export
        filename = f'{pathToSave}{image_id}.txt'

        # Export 
        if image_id in check_set:
        # Append to existing file as there can be more than one label in each image
            file = open(filename, "a")
            file.write("\n")
            file.write(content)
            file.close()

        elif image_id not in check_set:
            check_set.add(image_id)
            # Write files
            file = open(filename, "w")
            file.write(content)
            file.close()


def convert_bbox(height,width,coco_bbox):
        x, y, w, h  = coco_bbox
        dw = 1. / width
        dh = 1. / height
        x =  x +  (w / 2.0)
        y =  y +  (h / 2.0)
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x,y,w,h)


if __name__ == '__main__':

    annotationFilePath = "./annotations_train_val_2017/instances_val2017.json"
    pathToSave = "./val2017/labels/"
    convert_coco_to_yolo(annotationFilePath,pathToSave)