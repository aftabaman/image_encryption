
import os
from werkzeug.utils import  secure_filename
from flask import render_template,request, redirect,Flask,flash,url_for,send_from_directory,abort
app = Flask(__name__)

app.secret_key ="aftab"
# configureing our path to save the uploaded image

app.config["IMAGE_UPLOADS"] ="D:/PycharmProjects/image_encryption/uploaded_images"

app.config["CLIENT_IMAGES"] = "D:/PycharmProjects/image_encryption/uploaded_images"
app.config["ALLOWED_IMAGE_EXTENSIONS"]=["PNG","JPG","JPEG"]


###
key = 25

def encrypt(key,imgname):
    fi = open('uploaded_images/'+imgname,'rb')
    print(fi)

    img = fi.read()
    fi.close()
    img = bytearray(img)


    for index,values in enumerate(img):



        if index==0:
            hold = values ^ key
            img[index] = hold
        else:
            temp = values^hold
            img[index] = values^hold
            hold = temp



    fi2 = open('uploaded_images/'+imgname,'wb')
    fi2.write(img)
    fi2.close()
###

###

def decrypt(key,imgname):
    fi = open('uploaded_images/'+imgname, 'rb')
    print(fi)

    img = fi.read()
    fi.close()
    img = bytearray(img)

    print(len(img))

    for index, values in enumerate(img):
        #print(index, values)

        if index ==0:
            hold = values
            img[index]= values^key
        else:
            temp = values
            img[index]= values^hold
            hold = temp


    fi2 = open('uploaded_images/'+imgname, 'wb')
    fi2.write(img)
    fi2.close()
###
def allowed_image(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".",1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

# home page
@app.route("/")
def home():
    return render_template("encrypt.html")

@app.route("/alt")
def home_alt():
    return render_template("decrypt.html")

@app.route("/", methods=["POST"])
def home_after_download():
    dir = 'uploaded_images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    return render_template("encrypt.html")


# when the image is uploaded this will called
@app.route("/encrypt-image", methods=["GET","POST"])

def upload_image1():
    if request.method=="POST":
        if request.files:
            image = request.files["image"] # geting the image that has been passed

            if image.filename =="":
                return redirect(request.url)

            if not allowed_image(image.filename):
                return redirect(request.url)

            else:

                filename = secure_filename(image.filename)
                print(filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"],filename))
                # saving the image
                #image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
                flash('image saved!!')
                encrypt(key,filename)
            return render_template("index.html", filename = filename)

    return render_template("encrypt.html")

##
@app.route("/decrypt-image", methods=["GET", "POST"])
def upload_image2():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]  # geting the image that has been passed

            if image.filename == "":
                return redirect(request.url)

            if not allowed_image(image.filename):
                return redirect(request.url)

            else:

                filename = secure_filename(image.filename)
                print(filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                # saving the image
                # image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
                flash('image saved!!')
                decrypt(key, filename)
            return render_template("index.html", filename=filename)

    return render_template("decrypt.html")
##
@app.route('/download-image/<filename>')
def download_image(filename):
    print(filename)
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"] ,filename = filename, as_attachment=False)
    except FileNotFoundError:
        abort(404)
@app.route('/display/<filename>')
def send_image(filename):

    return send_from_directory(app.config["CLIENT_IMAGES"],filename)
if __name__ == "__main__":
    app.run(debug=True)