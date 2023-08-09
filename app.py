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
    
    wget.download("https://download1326.mediafire.com/1ga0rvjg6qkgha8oOPFVHY2V_WLYwde6gCWBXT1FQlhATeqS-GNBaZrzcuNuwZSCLs76qScw1vWYEhFSLNiKLjkMJX3Gog3gCSUz2VzV2IRE5ZfZOySSbF5HHww8AU9_dYJNZIriOyGNI4hTosvysfJZvpOY93jRC2z77H9N_66D/ekg10hcq141v5hi/image_features_vectors.idx")
    wget.download("https://download1584.mediafire.com/29g7k41bwpqg5eCW0sOQnrNX853Xxi74F66GoMquaXqTH4jeAPyMKr4H8N2vrtBfjscyLDHOJxyMusdAfZEMRq7ZbKzG3hKPPbjf_YIDPcgAf3Keca8UzD6kAPro24YbwhV_63uLYfYWAG9ka8c-L_rCFZ09alLyplZ3OTS_uKfC/0aemngb1qh3t9cn/image_data_features.pkl")
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
