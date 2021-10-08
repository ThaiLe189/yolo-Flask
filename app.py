"""
Simple app to upload an image via a web form 
and view the inference results on the image in the browser.
"""
import argparse
import io
import os
from PIL import Image
import cv2
import numpy as np

import torch
from flask import Flask, render_template, request, redirect, jsonify, json, Response
from detect import load_model, detect_one, detect_one_api
from camera import Video

app = Flask(__name__)

model = load_model("./yolov5s-face.pt", 'cpu')

@app.route("/", methods=["GET", "POST"])
def predict():
    face = []
    if request.method == "POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if not file:
            return

        img_bytes = file.read()

        nparr = np.fromstring(img_bytes, np.uint8)
        mat = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        results = detect_one(model, mat, 'cpu')

        cv2.imwrite("static/image0.jpg", results)
        return redirect("static/image0.jpg")

    return render_template("index.html")

DETECTION_URL = "/v1/"
@app.route(DETECTION_URL, methods=["POST"])
def predict_api():
    if not request.method == "POST":
        return

    face = []
    if request.files.get("image"):
        image_file = request.files["image"]
        img_bytes = image_file.read()

        nparr = np.fromstring(img_bytes, np.uint8)
        mat = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # cv2.imwrite("api.jpg", mat)
        results = detect_one_api(model, mat, 'cpu')
        
        for i in results:
            faceDict = {
                'rect' : str(i[0]).replace('[]',''),
                'point': str(i[1]).replace('[]','')
            }
            face.append(faceDict)

    jsonFace = json.dumps(face)

    return jsonify(Face=jsonFace)
 # concat frame one by one and show result

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route("/video_feed", methods=["GET"])
def video_feed():
    try:
        return Response(gen(Video()), mimetype='multipart/x-mixed-replace; boundary=frame')
    catch (exception):
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    # model = torch.hub.load(
    #     "deepcam-cnyolov5-face", "custom", pretrained=True, force_reload=True
    # ).autoshape()  # force_reload = recache latest code

    # model = torch.hub.load(
    #     'D:\\DATA\\MAIN\\ML_2\\BC\\yolov5-face', 'D:\\DATA\\MAIN\\ML_2\BC\\yolov5-flask\\yolov5s-face', force_reload=True, source = 'local'
    # )
    
    i = cv2.imread('./init/init.jpg')
    init = detect_one(model, i, 'cpu')
    
    # model.eval()
    # app.run(host="0.0.0.0", port=int(os.environment.get('PORT', 8080)))  # debug=True causes Restarting with stat
    app.run(host="0.0.0.0", port=args.port)