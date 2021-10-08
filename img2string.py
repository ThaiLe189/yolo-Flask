import base64

with open("D:\\DATA\\MAIN\\ML_2\\BC\\yolov5_face\\data\\images\\zidane.jpg", "rb") as img_file:
    b64_string = base64.b64encode(img_file.read())
    f = open("zidanbase64.txt", 'w')
    f.write(str(b64_string))
