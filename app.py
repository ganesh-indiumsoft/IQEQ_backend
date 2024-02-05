from flask import Flask,request,send_file
from flask_cors import CORS,cross_origin
import glob
import os
import numpy as np
import json
import shutil

# creating a Flask app
app = Flask(__name__,static_url_path='/static')
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/process', methods=['POST','GET'])
@cross_origin()
def generate():
    if request.method == 'POST':
        f = request.files['file']
        text = request.form.get('text')
        text = text.replace(" ","_")
        f.save(rf"{os.getcwd()}\upload\{text}\{f.filename}")
        shutil.copyfile(rf"{os.getcwd()}\upload\{text}\{f.filename}", rf"D:\IQEQ_UI\IQEQ\src\assets\{f.filename}")
        pdf_files_list = glob.glob(rf"D:\IQEQ_UI\IQEQ\src\assets\*.pdf") 
        asset_pdf_file = max(pdf_files_list, key=os.path.getctime)
        list_of_files = glob.glob(rf'{os.getcwd()}\upload\{text}\*.pdf') 
        latest_file = max(list_of_files, key=os.path.getctime)
        
        
        
        print(latest_file)
        # res = { "Bank Name": "SBM Bank (Mauritius) Ltd", "Authorised Representatives for Viewing Statements": ["Mr Neernaysingh Madhour", "Mrs Fatweena Bibi Ameen Uteene", "Mrs Savinilorna Payandi-Pillay Ramen"], "Authorised Representatives for Initiating Payments": ["Mr Anil Abbak", "Mr Nikola Pejovic"] }
        # res = { "Omnibus Account Provider Name": "CA Indosuez (Switzerland) SA", "Jurisdiction of Omnibus Account Provider": "Switzerland", "Undertaking Letter Obtained": "Yes", "Date Provided": "February 6, 2023" }
        # res = { "Company No.": "512978", "Date of incorporated": "Thursday, the 15th day of November, 2012" }
        res = { "Currency": "MUR", "IBAN": "MU81STCB1170000001084470000MUR", "Bank Branch Name": "SBM Bank (Mauritius) Limited 6th Floor SBM Tower Port Louis", "Beneficiary Name": "FINVEO MA" }
        res_dict = {}
        for k,v in res.items():
            if type(v) is list:
                res_dict[k] = ", ".join(v)
            else:
                res_dict[k] = v
        keys = list(res_dict.keys())
        n = len(keys)
        array = np.empty((n, 2), dtype=object)
        for i in range(n):
            array[i, 0] = keys[i]
            array[i, 1] = res_dict[keys[i]]
        latest_file = latest_file.replace("\\","/")
        json_res = {'res':array.tolist(),
                    'file':f"/assets/{os.path.basename(asset_pdf_file)}"}
        # 'file':f"http://localhost:5000/static/pdfplumber_5.pdf"
        json_res = json.dumps(json_res)
        return json_res

# driver function
if __name__ == '__main__':
    app.run(host ="localhost")
    # app.run(host='0.0.0.0',port=2001)