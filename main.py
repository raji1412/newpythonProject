from flask import Flask, render_template, redirect, url_for, flash, abort,request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import json

app=Flask(__name__)

#connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///details.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#tabel creation
class Detail(UserMixin, db.Model):
    __tablename__ = "detail"
    id=db.Column(db.Integer,primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    mobile=db.Column(db.Integer,unique=True)
    address = db.Column(db.String(1000))


# db.create_all()

@app.route("/")
def main_page():
    return render_template("index.html")
@app.route("/customers",methods=["GET", "POST","PUT","DELETE"])
def get_page():
    posts = Detail.query.all()
    return render_template("get.html",inf=posts)
@app.route("/customers/post",methods=["GET", "POST","PUT","DELETE"])
def post_page():
    if request.method=="POST":
        new_detail=Detail(
            id=request.form["id"],
            firstName=request.form["firstName"],
            lastName=request.form["lastName"],
            email=request.form["email"],
            mobile=request.form["mobile"],
            address=request.form["address"]
        )
        db.session.add(new_detail)
        db.session.commit()
        return redirect(url_for("get_page"))
    return render_template("post.html")

@app.route("/customers/put",methods=["GET", "POST","PUT","DELETE"])
def put_page():
    if request.method=="POST":
        id=request.form["id"]
        tobe_updated=Detail.query.get(id)
        tobe_updated.firstName=request.form["firstName"]
        tobe_updated.lastName = request.form["lastName"]
        tobe_updated.email = request.form["email"]
        tobe_updated.mobile = request.form["mobile"]
        tobe_updated.address = request.form["address"]
        db.session.commit()
        return redirect(url_for("get_page"))
    return render_template("put.html")

@app.route("/customers/<int:id>",methods=["GET", "POST","PUT","DELETE"])
def get_page_details(id):
    inf=Detail.query.get(id)
    arr=[]
    arr.append({
            "id":inf.id,
            "firstName":inf.firstName,
            "lastName":inf.lastName,
            "email":inf.email,
            "mobile":inf.mobile,
            "address":inf.address
        })
    return json.dumps({"Detail":arr}),200,{"Content- Type":"Application/json"}

@app.route("/customers/getall",methods=["GET", "POST","PUT","DELETE"])
def get_all_page_details():
    info=Detail.query.all()
    arr=[]
    for inf in info:
        arr.append({
                "id":inf.id,
                "firstName":inf.firstName,
                "lastName":inf.lastName,
                "email":inf.email,
                "mobile":inf.mobile,
                "address":inf.address
            })
    return json.dumps({"Detail":arr}),200,{"Content- Type":"Application/json"}


@app.route("/customers/delete",methods=["GET", "POST","PUT","DELETE"])
def delete_page():

    if request.method=="POST":
        id=request.form["id"]
        id_to_delete=Detail.query.get(id)
        db.session.delete(id_to_delete)
        db.session.commit()
        return redirect(url_for("get_page"))

    return render_template("delete.html")


if __name__ == "__main__":
    app.run(port=8080,debug=True)

