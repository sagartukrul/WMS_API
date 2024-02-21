from flask import Flask, request,render_template,jsonify, redirect, json

app = Flask(__name__)




@app.route("/", methods=['POST','GET'])
def Main():

    if request.method == 'POST':

        content = request.json
        if content['Process'] == "Putaway":
            Matrial_Code = content["Data"]
            Putaway_Location = content['Location']
            print(Matrial_Code, Putaway_Location)

            context = {
                "Response" : "Putaway Complete"
            }
            return json.dumps(context)

    elif request.method == 'GET':
        return "<h1> WMS Server is running </h1>"






app.run(host='0.0.0.0',debug=False)