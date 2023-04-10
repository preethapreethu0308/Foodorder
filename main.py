import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

con=mysql.connector.connect(user="root", database="foodies")
app = Flask(__name__)
app.secret_key="viva"
@app.route("/")
def home():
    session["user"]="no"
    return render_template("home.html")


@app.route("/fooditems")
def fooditems():
    cur1=con.cursor()
    cur1.execute("select * from dishes where Category='Breakfast'")
    result1=cur1.fetchall()

    cur2 = con.cursor()
    cur2.execute("select * from dishes where Category='Lunch'")
    result2 = cur2.fetchall()

    cur3 = con.cursor()
    cur3.execute("select * from dishes where Category='Dinner'")
    result3 = cur3.fetchall()

    cur4 = con.cursor()
    cur4.execute("select * from dishes where Category='Starters'")
    result4 = cur4.fetchall()

    cur5 = con.cursor()
    cur5.execute("select * from dishes where Category='Ice Cream'")
    result5 = cur5.fetchall()
    return render_template("fooditems.html", data1=result1, data2=result2, data3=result3, data4=result4, data5=result5)

@app.route("/foodentry")
def foodentry():
    return render_template("foodentry.html")

@app.route("/dishessave",methods=["POST","GET"])
def dishessave():
    if request.method == "POST":
        a = request.form["Food_Id"]
        print(a)
        b = request.form["Food_Name"]
        print(b)
        c = request.form["Food_Image"]
        print(c)
        d = request.form["Price"]
        print(d)
        e = request.form["Category"]
        print(e)
        f = request.form["Hotel_Name"]
        print(f)
        cur=con.cursor()
        cur.execute("insert INTO dishes values('"+a+"','"+b+"','"+c+"','"+d+"','"+e+"','"+f+"')")
        con.commit()
        cur.close()
        return redirect(url_for("dishes"))


@app.route("/custmerdetail")
def custmerdetail():
    cur=con.cursor()
    cur.execute("select * from customer")
    result=cur.fetchall()
    return render_template("custmerdetail.html", data=result)

@app.route("/customeredit")
def custmer():
    id = request.args.get("id")
    cur = con.cursor()
    cur.execute("select * from customer where Customer_Id='"+id+"'")
    result = cur.fetchall()
    return render_template("custmer.html", data=result)



@app.route("/custmerupdate", methods=["POST","GET"])
def custmerupdate():
    if request.method == "POST":
        a = request.form["cusid"]
        print(a)
        b = request.form["cname"]
        print(b)
        c = request.form["email"]
        print(c)
        d = request.form["add"]
        print(d)
        e = request.form["phone"]
        print(e)
        f = request.form["custimage"]
        print(f)
        cur=con.cursor()
        cur.execute("update customer set Customer_Name='"+b+"', Email_Id='"+c+"', Address='"+d+"', PhoneNumber='"+e+"', Customer_Image='"+f+"' where Customer_Id='" +a+ "'")
        con.commit()
        cur.close()
        return redirect(url_for("customer"))

@app.route("/customerdelete", methods=["GET","POST"])
def customerdelete():
    id=request.args.get("id")
    cur=con.cursor()
    cur.execute("delete from customer where Customer_Id='"+id+"'")
    con.commit()
    cur.close()
    return redirect(url_for("customer"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logincheckup", methods=["GET","POST"])
def logincheckup():
    if request.method == "POST":
        a = request.form["username"]
        b = request.form["password"]
        cur = con.cursor()
        cur.execute("select * from customer where Customer_Name='"+a+"' and Customer_Id='"+b+"'")
        result=cur.fetchone()
        con.commit()
        cur.close()

    if result:
        session["user"]=a
        session["userid"]=b
        return render_template("home.html")
    else:
        return render_template("login.html")


@app.route("/orders")
def orders():
    cur = con.cursor()
    cur.execute("select * from ordersnow where Customer_Id ='"+session["userid"]+"'")
    result = cur.fetchall()
    cur.close()
    cur1 = con.cursor()
    cur1.execute("select sum(Amount) from ordersnow where Customer_Id ='"+session["userid"]+"'")
    result1 = cur1.fetchall()
    cur1.close()
    return render_template("bill.html", data=result, data1=result1)


@app.route("/ordersSave", methods=["POST", "GET"])
def ordersSave():
    userid = session["userid"]
    user = session["user"]
    fname = request.args.get("fname")
    prize = request.args.get("prize")
    qnty = request.form.get("qnty")

    cur = con.cursor()
    cur.execute("insert into ordersnow values('1','"+ userid +"','"+ user +"','13/03/2023','"+ fname +"','"+ prize +"','2')")
    con.commit()
    cur.close()
    print(qnty)
    return redirect(url_for("orders"))


@app.route("/orderedit")
def orderedit():
    id = request.args.get("fid")
    cur = con.cursor()
    cur.execute("select * from dishes where Food_Id ='"+id+"'")
    result = cur.fetchall()
    return render_template("orderedit.html", data=result)


@app.route("/orderupdate", methods=["POST","GET"])
def orderupdate():
    if request.method == "POST":
        a = request.form["ord"]
        print(a)
        b = request.form["usname"]
        print(b)
        c = request.form["pri"]
        print(c)
        d = request.form["qnty"]
        print(d)
        e = int(c)*int(d)
        print(e)
        cur=con.cursor()
        cur.execute("Insert into ordersnow Values('"+a+"','"+session["userid"]+"','"+session["user"]+"','"+str(datetime.datetime.now())+"','"+b+"','"+c+"','"+d+"','"+str(e)+"')")
        con.commit()
        cur.close()
        return redirect(url_for("orders"))

@app.route("/footer")
def footer():
    return render_template("footer.html")


if __name__ == "__main__":
    app.run()


