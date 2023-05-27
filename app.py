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
    wget.download("https://download1072.mediafire.com/l34joaqpdrgg9Vcsdb1FDpj35I_asMUBBkh3fb-DLjGZbKQjelCMe2R4aIuG-0G0L6IRiP00G600cy7pmrln-ahuPiYWnj3YIlCoyS6UdOTDLnfl8-34PVgWOCE8cPWrWgWN-2hukVGwyPtBdFrl2hbcqzzB1v60yvUSp_pkVA/0aemngb1qh3t9cn/image_data_features.pkl")
    wget.download("https://download1492.mediafire.com/qcvf2phl645gH-gDgEChHIv5K76AE3qxtQsbf0_97f7EKf9eKTIQ1YAiFWqvaItDvL9W9sV6t5Q7NOl9LfCUyOKLrWLxzNFSKTBeoTDpLB_gWorEnmch83tbR8hKXandoic_hUtd0XnaCxsY4xAovI2v0VRl7Y_B7Q4traHW2Q/xtt5tjlp5fxx1lq/image_features_vectors.idx")
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
def new():
    return jsonify({"Testing": "Hello"})


@app.route('/api', methods=['POST', "GET"])
def index():
    
    print("We are here")
    if request.method == 'POST':
        print("Post here")
        image = request.files['fileup']
        newimage = Image.open(image)
        print("Image Loaded")
        newimage.save("Ahmed.jpg")
        print("Image Saved")
        x = st.get_image_metadata_file()
        print("metadata loaded")
        similar_images = st.get_similar_images(image_path="Ahmed.jpg", number_of_images=10)
        print("similar images")
        #os.remove(newimage.filename) 
        images  = []
        for index in similar_images:
            images.append(similar_images[index])
        print("Images are done")
        return jsonify({"Testing": images})
        
    else:
        print("we are in else")
        return jsonify({"Error": "No Images"})
            

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
