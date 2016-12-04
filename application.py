from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
import json
import urllib.request
from urllib.parse import quote
import requests
import pprint


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/vehicle/', methods=['GET', 'POST'])
def vehicle():
    if request.method == 'POST':
            vehicle_make = request.get_json(force=True)
            response = requests.get("https://api.edmunds.com/api/vehicle/v2/{}/models?fmt=json&api_key=2skrh7ku3dkgzen67zwxcszy".format(vehicle_make)).json()
            return jsonify(response)
            # for model in range(0, vehicle_model_options['modelsCount']):
            #    pprint.pprint(vehicle_model_options['models'][model]['id'])
    else:
        return render_template('vehicle.html')

@app.route('/ssa/', methods=['GET', 'POST'])
def ssa():
    if request.method == 'POST':
        vehicle_make = request.get_json(force=True)
        response = requests.get("https://api.edmunds.com/api/vehicle/v2/{}/models?fmt=json&api_key=2skrh7ku3dkgzen67zwxcszy".format(vehicle_make)).json()
        return jsonify(response)
            # for model in range(0, vehicle_model_options['modelsCount']):
            #    pprint.pprint(vehicle_model_options['models'][model]['id'])
    else:
        return render_template('ssa.html')
        
@app.route('/register/')
def register():
    return render_template('register.html')
    
@app.route('/logout/')
def logout():
    return render_template('logout.html')

@app.route('/pacer/', methods=['GET', 'POST'])
def pacer():
    if request.method == "POST":
        
        if request.form["court_type"] == "" or request.form["court_region"] == "" or request.form["party_name"] == "":
            #  failure!!
            return render_template("pacer.html") 
        
        apikey = ""
        # apikey = "hyxS7CQczefd7rWy9zsu"
        court_type, court_region = request.form["court_type"], request.form["court_region"]
        filed_start_date, filed_end_date = request.form["filed_start_date"], request.form["filed_end_date"]
        closed_start_date, closed_end_date = request.form["closed_start_date"], request.form["closed_end_date"] 
        case_num, party_name = request.form["case_num"], urllib.parse.quote(request.form["party_name"])
        ssn, ssn4 = request.form["ssn"], request.form["ssn4"]
        
        url = "https://www.enclout.com/api/v1/pacer/show.json?auth_token={}".format(apikey) + "&sel_court={}".format(court_type) + "&sel_region={}".format(court_region) + "&date_filed_start={}".format(filed_start_date) + "&date_filed_end={}".format(filed_end_date) + "&date_term_start={}".format(closed_start_date) + "&date_term_end={}".format(closed_end_date) + "&case_no={}".format(case_num) + "&party={}".format(party_name) + "&ssn={}".format(ssn) + "&ssn4={}".format(ssn4)
        data = urllib.request.urlopen(url).read().decode("utf-8")
        obj = json.loads(data)
        return render_template("pacer_results.html", cart=obj["cases"])
    return render_template('pacer.html')


if __name__ == '__main__':
    app.run(debug=True)