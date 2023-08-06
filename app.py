from flask import Flask, jsonify
from flask import request
import os
from PIL import Image
from DeepImageSearch import Load_Data, Search_Setup
import wget
import shutil

print("Loading Data")
image_list = Load_Data().from_folder(folder_list = ["Data"])
print("Data Loaded")
print("Loading Model")
st = Search_Setup(image_list, model_name="vgg19", pretrained=True)
print("Model Loaded")
file = open("first.txt", "r+")
x = file.readline()
if int(x) == 0:
    print("Download Weights")
    
    wget.download("https://download1326.mediafire.com/v007a2zsj4vgtpBu34LQo7l1ZC3UHZsaoJNDm7DQUyepa12N2I5M2VcQZkFFIPKhluv2_cn3bY_cklv2qXlCdLnvr2TFpNR769nYqtdDWOHSINRpXIGR2VHoMOHnrFl-EPSYgvuyxj-maA_E6dmy7tTacYOQdYy05Q7RIhjPR10/ekg10hcq141v5hi/image_features_vectors.idx")
    wget.download("https://download1584.mediafire.com/re2w5ite1zlgrq66_uYN6K6VDzsfy5rnWpgTboqqy2Nfpc3UEcb4LNry0uSQcYF3jPuf6psQSF-SrSjUnutnNoqpyG1i1OpF-lVjpmUM961LDBZ0YqT7e3JD5y5nbaMSEN6-nOU7q3IevSQorOSHsoVw-nhEfnI9fCwbvswzpZo/0aemngb1qh3t9cn/image_data_features.pkl")
    print("Weights Downloaded")
    print("Done")
    shutil.move("image_features_vectors.idx", "metadata-files/vgg19/image_features_vectors.idx" )
    shutil.move("image_data_features.pkl", "metadata-files/vgg19/image_data_features.pkl" )
    #st.run_index()
    file.write("1")

file.close()
#meta = st.get_image_metadata_file()
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
        print("we are here")
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
