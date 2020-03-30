from flask import Flask ,jsonify,request,render_template,send_file
from zipfile import ZipFile
import os
import pandas as pd
import shutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    files = request.files.getlist('files[]')
    name = request.form['name']
    dataset_path = os.path.join('static','datasets',name)
    shutil.rmtree(dataset_path, ignore_errors=True)
    os.mkdir(dataset_path)
    df = pd.DataFrame()
    for f in files:
        file_path = os.path.join('static','uploads',f.filename)
        f.save(file_path)
        with ZipFile(file_path) as test_zip:
            with test_zip.open('patches.csv') as patch_info:
                temp_df = pd.read_csv(patch_info)
                temp_df['filename'] = f.filename
                df.append(temp_df)
                for _ , row in temp_df.iterrows():
                    dataset_class_path = os.path.join('static','datasets',name,row['note'])
                    if not os.path.isdir(dataset_class_path):
                        os.mkdir(dataset_class_path)
                    with test_zip.open(row['location'][2:],'r') as temp_file:
                        with open(os.path.join(dataset_class_path,f'{f.filename}-{row["id"]}.jpg'),'wb') as t2:
                            t2.write(temp_file.read())
    shutil.make_archive(os.path.join('static','parsed',name),'zip',root_dir=dataset_path)       

    return send_file(os.path.join('static','parsed',name+'.zip'),as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)