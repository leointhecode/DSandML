import os
from flask import Flask, request, render_template
from skimage.metrics import structural_similarity
import cv2
from PIL import Image

#Flask Config

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"


# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'
app.config['EXISTNG_FILE'] = 'app/static/original'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
	
    if request.method == "GET":
        return render_template("index.html" ,mainText="Upload your documents!")
	
    if request.method == "POST":

        check_file_upload = request.files["checkFile"]

        # Resize and save the uploaded image
        uploaded_image = Image.open(check_file_upload).resize((2550,3300))
        uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))


        # Resize and save the original image to ensure both uploaded and original matches in size
        original_file_upload = request.files["originalFile"]

        original_image = Image.open(original_file_upload).resize((2550,3300))
        original_image.save(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))


        # Read uploaded and original image as array
        original_image = cv2.imread(os.path.join(app.config['EXISTNG_FILE'], 'image.jpg'))
        uploaded_image = cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg'))


        # Convert image into grayscale
        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)


        # Calculate structural similarity
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")

        print(round(score*100,2))

        return render_template('index.html',mainText=str(round(score*100,2)) + '%' + ' correct')
    

if __name__ == '__main__':
   app.run(debug=True)
