from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "arvr_secret"

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="Lax"
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED = {"png","jpg","jpeg","glb","gltf","obj","fbx","pdf"}

def allowed_file(name):
    return "." in name and name.rsplit(".",1)[1].lower() in ALLOWED


# LOGIN
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form["user"]=="admin" and request.form["pwd"]=="1234":
            session["user"]="admin"
            return redirect("/")
        return render_template("login.html", error="Invalid Login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# HOME
@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


# UPLOAD
@app.route("/upload", methods=["POST"])
def upload():
    file=request.files["file"]

    if file and allowed_file(file.filename):
        path=os.path.join(UPLOAD_FOLDER,file.filename)
        file.save(path)
        return redirect(url_for("viewer", name=file.filename))

    return "Invalid file"


# VIEWER
@app.route("/viewer/<name>")
def viewer(name):
    return render_template("viewer.html", file=name)


@app.route("/uploads/<name>")
def files(name):
    return send_from_directory(UPLOAD_FOLDER,name)


if __name__=="__main__":
    port=int(os.environ.get("PORT",10000))
    app.run(host="0.0.0.0",port=port)