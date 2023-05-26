from flask import Flask, jsonify
from flask import request
import os
from PIL import Image
from DeepImageSearch import Load_Data, Search_Setup
import wget
import shutil


image_list = Load_Data().from_folder(folder_list = ["Data"])
st = Search_Setup(image_list, model_name="vgg19", pretrained=True)

file = open("first.txt", "r+")
x = file.readline()
if int(x) == 0:
    response = wget.download("https://b36e-197-56-156-118.eu.ngrok.io/static/image_data_features.pkl")
    response2 = wget.download("https://b36e-197-56-156-118.eu.ngrok.io/static/image_features_vectors.idx")
    shutil.move("image_features_vectors.idx", "metadata-files/vgg19/image_features_vectors.idx" )
    shutil.move("image_data_features.pkl", "metadata-files/vgg19/image_data_features.pkl" )
    #st.run_index()
    file.write("1")

file.close()

app = Flask(__name__)

def is_valid_image(file):
    try:
        image = Image.open(file)
        image.verify()
        return True
    except:
        return False




@app.route('/', methods=['POST', "GET"])
def index():
    
    if request.method == 'POST':
        image = request.files['fileup']
        newimage = Image.open(image)
        newimage.save("Ahmed.jpg")
        try:
            x = st.get_image_metadata_file()
            similar_images = st.get_similar_images(image_path="Ahmed.jpg", number_of_images=10)
            #os.remove(newimage.filename) 
            images  = []
            for index in similar_images:
                images.append(similar_images[index])

            return jsonify({"Testing": images})
        except:
            return jsonify({"Testing": "Error"})
    else:
        return jsonify({"Error": "No Images"})
            

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
