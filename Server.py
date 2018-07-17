'''
Created on Jul 17, 2018

@author: User1
'''

import pandas as pd
import os 

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("enrollment.html")


@app.route("/codeConcept")
def get_codeConcept_data():
    return render_template("enrollment.html")

@app.route("/codeConcept/SNOMED/<code>")
def get_SNOMED_data(code):
    path = os.path.join('QualityGap_Data', 'Snomed_Dict.csv')
    Snomed = pd.read_csv(path)
    Snomed = Snomed[Snomed['conceptId'] == int(code)]
    return Snomed.reset_index().to_json(orient='records') 

@app.route("/codeConcept/LOINC/<code>")
def get_LOINC_data(code):
    path = os.path.join('QualityGap_Data', 'Loinc.csv')
    Loinc = pd.read_csv(path,low_memory=False)
    Loinc = Loinc[Loinc['LOINC_NUM'] == code]
    return Loinc.reset_index().to_json(orient='records')

@app.route("/codeConcept/RXNORM/<code>")
def get_RXNORM_data(code):
    path = os.path.join('QualityGap_Data', 'RXNORM_Dict.csv')
    RXNORM = pd.read_csv(path)
    RXNORM = RXNORM[RXNORM['RXCUI'] == int(code)]
    return RXNORM.reset_index().to_json(orient='records')
 
@app.route("/codeConcept/Firstname")    
def get_Firstname():
    path = os.path.join('QualityGap_Data','Firstname.csv')
    Firstname = pd.read_csv(path)
    return Firstname.reset_index().to_json(orient='records')

@app.route("/codeConcept/Lastname")
def get_Lastname():
    path = os.path.join('QualityGap_Data','Lastname.csv')
    Lastname = pd.read_csv(path)
    return Lastname.reset_index().to_json(orient='records')
if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    
    