import glob
import random
import shutil


def readLines(file):
    f = open(file,"r")
    lines = f.read().splitlines()
    f.close()    
    for line in lines:
        try :

            n = int(line.split(' ')[0])
            if n == 93:
                # print(file)
                global c
                c += 1
        except:
            print(file,line)


def deleteClass(file,class_number):
    with open(file, "r") as f:
        lines = f.readlines()

    with open(file, "w") as f:
        for line in lines:
            if int(line.split(' ')[0]) != class_number :
                f.write(line)
   
def copyImages(file):
    # copy images
    src_img = file.replace("labels","images").replace("txt","jpg")
    dst_img = src_img.replace("val","to_val")
    shutil.copyfile(src_img, dst_img)
    
    # copy txt
    dst_txt = file.replace("val","to_val")
    shutil.copyfile(file, dst_txt)



if __name__ == "__main__" :
    random.seed(1001)
    c = 0
    # /home/muhammed/Documents/work/datasets/coco_2017/coco_2017
    txt_files = glob.glob("/home/muhammed/Documents/work/datasets/box/dataset/labels/train/*.txt")
    random.shuffle(txt_files)

    for file in txt_files:
        readLines(file)
        # deleteClass(file,93)   
        # copyImages(file)
    print(c)
