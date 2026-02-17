from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "arvr_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED = {"png","jpg","jpeg","pdf","glb","gltf","obj","fbx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED


# -------- LOGIN (No DB simple auth) --------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]

        # simple demo login
        if user=="admin" and pwd=="1234":
            session["user"]=user
            return redirect("/")
        return "Invalid Login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# -------- MAIN PAGE --------
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# -------- FILE UPLOAD --------
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)
        return redirect(url_for("viewer", name=file.filename))
    return "Invalid file"


# -------- VIEWER --------
@app.route("/viewer/<name>")
def viewer(name):
    return render_template("viewer.html", file=name)


@app.route("/uploads/<name>")
def files(name):
    return send_from_directory(UPLOAD_FOLDER, name)


if __name__ == "__main__":
    app.run(debug=True)