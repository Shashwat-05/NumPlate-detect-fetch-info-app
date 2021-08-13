from flask import render_template,Flask,request
import json,requests,xmltodict
from werkzeug.utils import secure_filename
import plate_model ,os

app = Flask('vehicleInfo')
UPLOAD_FOLDER = 'D:\\SUMMER PROGRAM\\tasks\\task8\\'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def vehicle_info(plate_num):
    rno = str(plate_num)
    username = 'ElSid1'
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
    #file = request.files.get('img','')
    file = request.files['imagefile']
    #in_num = request.args.get('number')

    #if in_num == '':
        
    filename = secure_filename(file.filename)

    

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    full_pic , plate_pic = plate_model.inputImg(filename)
    pnum = plate_model.toText(plate_pic)

    #else:
    pnum = 'UP25BN3162'
    
    register_info = vehicle_info(pnum)
    return render_template('out.html',data=register_info)

app.run(host="192.168.29.78", port=4321 ,debug=True)
