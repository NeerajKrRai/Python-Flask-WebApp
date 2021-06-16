import requests
from flask import Flask, request, render_template, jsonify, json
from requests.auth import HTTPBasicAuth
import logging

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submitForm', methods=['GET','POST'])
def my_form_post():
    name = request.form['name']
    address = request.form['address']
    email = request.form['email']

    #Server side validations
    error = None
    if not name or not name.strip():
        error = 'name is missing'
    if not email or not email.strip() or '@' not in email:
        error = 'email is missing'
    if not address or not address.strip():
        error = 'message is missing'

    if error:
        return {"err":"Please fill out all the fields"}
    #Creating data for the API
    data = {
   "activity_id":"b40ae957-2ac4-4b1c-a2e2-1ecb5935804f",
   "address":{
      "line_1":address,
      "line_2":"The Core, Bath Lane",
      "town":"Newcastle Upon Type",
      "district":"Tyne & Wear",
      "territory":"GBR",
      "postcode":"NE4 5TF"
   },
   "full_name":name,
   "email":email,
   "provider":"my-integration",
   "identity":"98700f04-e705-4547-a3ee-d38a8cc9293d",
   "telephone":"+441914980123",
   "line_items":[
      {
         "stock_partition_id":"bf77168f-d4d4-42fd-984f-9dc5bcf5c4d8"
      }
   ],
   "consents":[
   ],
   "locale":"en_GB"
}
    #request SoPost API with basic authentication.
    response = requests.post('https://api.staging.sopost.dev/v1/orders', auth=HTTPBasicAuth('54a13f32-2106-45a7-b1cf-0f90afd357a2', 'd815e01e-1261-4d48-81d8-3c880df798a3'),data = json.dumps(data))
    responses = response.json()
    print(data)
    html = "<p> <b> Thank you for placing an order with SoPost<br>.<br>Your Order details are : <b><p>"
    for i in responses:
        html += "<p>" + i + ":" + responses[i] + "<p>"
        html += "<br>";
    return html
    #return {'id': 'a5cfc138-c649-4426-bc7b-e0959be65432', 'created': '2021-06-15T11:19:24+00:00'}
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)