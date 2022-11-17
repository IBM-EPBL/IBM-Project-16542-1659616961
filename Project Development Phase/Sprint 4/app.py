from flask import Flask , request , redirect,url_for
import os
import pickle
import requests

from flask import render_template
model = pickle.load(open('wqi_prediction_model.pkl','rb'))

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return render_template("Page-2.html",display="none",result="")

@app.route("/predict",methods=['POST'])
def predict():
    temp = request.form["TEMP"]
    dissolved_oxygen = request.form["DO"]
    ph = request.form["PH"]
    conductivity = request.form["CO"]
    biochemical_oxygen = request.form["BO"]
    nitrate = request.form["NT"]
    feral_coliform = request.form["FC"]
    total_coliform = request.form["TC"]
    input = [[temp,dissolved_oxygen,ph,conductivity,biochemical_oxygen,nitrate,feral_coliform,total_coliform]]
    print(temp,dissolved_oxygen,ph,conductivity,biochemical_oxygen,nitrate,feral_coliform,total_coliform)
    transform = pickle.load(open('object.pkl','rb'))
    preprocessed_input = transform.transform(input)
    input = preprocessed_input.tolist()
    output = wqi_predict(input)

    print(output)
    if output == 0:
        result = "This kind of water need to be refined or recycled for any further use."
    elif output == 1:
        result = "Can be used for farming. Water after washing vegetables or fruits comes under this category. Using them for watering plants helps increases growth"
    elif output == 2:
        result = "Used for bathing, washing purposes. It is good for aquatic lives too."
    else:
        result = "Excellent and good	Water classified under this can be used for drinking purposes."
    print(result)
    return render_template("Page-2.html",display="",result=result)

def wqi_predict(input):
    

    # NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
    API_KEY = "pOBlNpQZRHjnXu4PKHll5AuycxtWWPhS-WY3aRUeR0WU"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5','f6','f7']], "values":input}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/b7435f7c-15a7-460e-adbf-cd2df5330e58/predictions?version=2022-11-16', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring.json())
    output = response_scoring.json()["predictions"][0]["values"][0][0]
    return output
if __name__ == "__main__":
    app.run(debug=True)