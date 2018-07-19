'''
Created on Jul 17, 2018

@author: User1
'''

import pandas as pd
import os
import json 

from flask import Flask
from flask import render_template

app = Flask(__name__)
base = 'QualityGap_Data\codeConcept'

@app.route("/")
def index():
    return render_template("enrollment.html")


@app.route("/codeConcept")
def get_codeConcept_data():
    return render_template("enrollment.html")

@app.route("/codeConcept/SNOMED/<code>")
def get_SNOMED_data(code):
    path = os.path.join(base, 'Snomed_Dict.csv')
    Snomed = pd.read_csv(path)
    Snomed = Snomed[Snomed['conceptId'] == int(code)]
    return Snomed.reset_index().to_json(orient='records') 

@app.route("/codeConcept/LOINC/<code>")
def get_LOINC_data(code):
    path = os.path.join(base, 'LOINC_Dict.csv')
    Loinc = pd.read_csv(path,low_memory=False)
    Loinc = Loinc[Loinc['LOINC_NUM'] == code]
    return Loinc.reset_index().to_json(orient='records')

@app.route("/codeConcept/RXNORM/<code>")
def get_RXNORM_data(code):
    path = os.path.join(base, 'RXNORM_Dict.csv')
    RXNORM = pd.read_csv(path)
    RXNORM = RXNORM[RXNORM['RXCUI'] == int(code)]
    return RXNORM.reset_index().to_json(orient='records')

@app.route("/codeConcept/UCUM/<code>")
def get_UCUM_data(code):
    path = os.path.join(base, 'UCUM_Dict.csv')
    UCUM = pd.read_csv(path)
    UCUM = UCUM[UCUM['Code'] == code]
    return UCUM.reset_index().to_json(orient='records')

@app.route("/codeConcept/Metathesaurus/<code>")
def get_Metathesaurus_data(code):
    path = os.path.join(base, 'Metathesaurus_Dict.csv')
    Metathesaurus = pd.read_csv(path)
    Metathesaurus = Metathesaurus[Metathesaurus['code'] == code]
    return Metathesaurus.reset_index().to_json(orient='records')

@app.route("/codeConcept/NDRT/<code>")
def get_NDRT_data(code):
    path = os.path.join(base, 'NDRT_Dict.csv')
    NDRT = pd.read_csv(path)
    NDRT = NDRT[NDRT['SCUI'] == code]
    return NDRT.reset_index().to_json(orient='records')

@app.route("/codeConcept/UNII/<code>")
def get_UNII_data(code):
    path = os.path.join(base, 'UNII_Dict.csv')
    UNII = pd.read_csv(path)
    UNII = UNII[UNII['UNII'] == code]
    return UNII.reset_index().to_json(orient='records')

@app.route("/codeConcept/NDC/<code>")
def get_NDC_data(code):
    path = os.path.join(base, 'NDC_Dict.csv')
    NDC = pd.read_csv(path)
    NDC = NDC[NDC['NDCPACKAGECODE'] == code]
    return NDC.reset_index().to_json(orient='records')

@app.route("/codeConcept/CVX/<code>")
def get_CVX_data(code):
    path = os.path.join(base, 'CVX_Dict.csv')
    CVX = pd.read_csv(path)
    CVX = CVX[CVX['CVX Code'] == code]
    return CVX.reset_index().to_json(orient='records')

@app.route("/codeConcept/internal/<system>")
def get_internal(system):
    path = os.path.join(base + '/internal', system + '.json')
    with open(path, 'r') as f:
        internal = json.load(f)
    return json.dumps(internal)

@app.route("/codeConcept/v2/<system>")
def get_v2(system):
    path = os.path.join(base + '/v2', system + '.json')
    with open(path, 'r') as f:
        v2 = json.load(f)
    return json.dumps(v2)

@app.route("/codeConcept/v3/<system>")
def get_v3(system):
    path = os.path.join(base + '/v3', system + '.json')
    with open(path, 'r') as f:
        v3 = json.load(f)
    return json.dumps(v3)


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
    
    
    
    
    