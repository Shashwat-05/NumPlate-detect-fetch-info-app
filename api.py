from flask import render_template,Flask,request
import json,requests,xmltodict
from werkzeug.utils import secure_filename
import plate_model ,os

app = Flask('vehicleInfo') #webapp name

UPLOAD_FOLDER = '<< PATH TO FOLDER >>' #where to save the uploaded file back in server

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def vehicle_info(plate_num): #fetches vehicle details via API
    rno = str(plate_num)
    username = '<< enter the username >>'
    r = requests.get(f"http://www.regcheck.org.uk/api/reg.asmx/CheckIndia?RegistrationNumber={rno}&username={username}")
    data = xmltodict.parse(r.content)
    in_json = json.dumps(data)
    info = json.loads(in_json)
    veh_info = json.loads(info['Vehicle']['vehicleJson'])
    return veh_info

@app.route('/search')
def api():
    return render_template('api.html')



@app.route('/output',methods=['POST'])
def output():
    
    file = request.files['imagefile']  #gets the files via POST
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #saved file
    
    full_pic , plate_pic = plate_model.inputImg(filename)
    pnum = plate_model.toText(plate_pic)  # pic characters converted to text

    
    register_info = vehicle_info(pnum)
    return render_template('out.html',data=register_info) #forwards output 

app.run(host="<< IP of SYSTEM >>", port=1234 ,debug=True)
