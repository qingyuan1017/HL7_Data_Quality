'''
Created on Jul 11, 2018

@author: Jason Zhang
'''
import json
import os
import re

class TestSchema:
    #Schema for different resource in FHIR Release (STU)
    required_keys = []
    reference_keys = []
    codeConcept_keys = []
    name_keys = []
    contact_keys = []
    address_keys = []

    def __init__(self,flag):
        if flag == 'Patient':
            self.patientSchema()
        elif flag == 'Allergyintolerance':
            self.patientSchema()
        elif flag == 'Condition':
            self.conditionSchema()
        elif flag == 'Observation':
            self.observationSchema()
        elif flag == 'Familyhistory':
            self.familyhistorySchema()
        elif flag == 'Report':
            self.reportSchema()
        elif flag == 'Immunization':
            self.immunizationSchema()
        elif flag == 'Careplan':
            self.careplanSchema()
        elif flag == 'Procedure':
            self.procedureSchema()
        elif flag == 'Device':
            self.deviceSchema()
        elif flag == 'Document':
            self.documentSchema()

    def patientSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'Patient.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)
        self.name_keys = [['name'],[{'contact':'name'}]]
        self.contact_keys = [['telecom'],[{'contact':['telecom']}]]
        self.address_keys = [['address'],[{'contact':'address'}]]

    def allergyintoleranceSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'AllergyIntolerance.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)
        


    def conditionSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'Condition.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)

    def observationSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'Observation.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)

    def familyhistorySchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'FamilyMemberHistory.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)
    
    def reportSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'DiagnosticReport.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)
    

    def immunizationSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'Immunization.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)

    def careplanSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'CarePlan.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)

    def procedureSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'Procedure.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)


    def deviceSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'Device.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)                          

    def documentSchema(self):
        path = os.path.join('QualityGap_Data/Schema', 'DocumentReference.schema.json')
        with open(path, 'r',encoding="utf8") as f:
            self.schema = json.load(f)
        keys = list(self.schema['definitions'].keys())
        keys = list(map(lambda x: '#/definitions/' + x ,keys))
        direct,nested = self.findReference(self.schema,keys,'',[],[],'Reference.schema.json#/definitions/Reference')
        nested.remove('')
        self.reference_keys = self.process_schema(direct,nested)
        direct,nested = self.findReference(self.schema,keys,'',[],[],'CodeableConcept.schema.json#/definitions/CodeableConcept')
        nested.remove('')
        self.codeConcept_keys = self.process_schema(direct,nested)
        
    def findReference(self,d,keys,path,direct,nested,argument):
        omit = ['definitions','allOf','properties']
        if isinstance(d, dict):
            for k, v in d.items():
                temp = path
                if (k not in omit) & (k!= keys[0].split('/')[-1]):
                    if k == 'items':
                        temp = [temp]
                    else:
                        if temp != '':
                            temp = {str(temp):k}
                        else:
                            temp += k
                if isinstance(v, dict):
                    self.findReference(v,keys,temp,direct,nested,argument)
                if isinstance(v, list):
                    self.findReference(v,keys,temp,direct,nested,argument)
                else:
                    if any(key in v for key in keys):
                        nested.append(path)
                    if argument in v:
                        direct.append(path)
        if isinstance(d, list):
            for x in d:
                self.findReference(x,keys,path,direct,nested,argument)
        return direct,nested
    
    def process_schema(self,direct,nested):
        result = self.removeDict(direct,[])
        for i in nested:
            if type(i) == list:
                key = i[0]
                if type(key) == dict:
                    for t in key.keys():
                        k = key[t]
                        new_t = self.selfReplacement(t,nested)
                        if type(new_t) == list:
                            v = self.findReplacement(k,direct)
                            for s in v:
                                result.append([{new_t[0]:[s]}])
                        else:
                            v = self.findReplacement(k,direct)
                            for s in v:
                                result.append({new_t:[s]})
                else:
                    v = self.findReplacement(key,direct)
                    for s in v:
                        result.append([s])
            elif type(i) == dict:
                for t in i.keys():
                        k = i[t]
                        new_t = self.selfReplacement(t,nested)
                        if type(new_t) == list:
                            v = self.findReplacement(k,direct)
                            for s in v:
                                result.append([{new_t[0]:s}])
                        else:
                            v = self.findReplacement(k,direct)
                            for s in v:
                                result.append({new_t:s})
            else:
                v = self.findReplacement(i,direct)
                for s in v:
                    result.append(s)
    
    
        return result
    
    def findReplacement(self,key,a):
        result = []
        for i in a:
            if type(i) == list:
                v= i[0]
                if type(v) == dict:
                    if re.search(key,list(v.keys())[0],re.IGNORECASE) != None:
                        result.append({key:[v[list(v.keys())[0]]]})
            if type(i) == dict:
                if re.search(key,list(i.keys())[0],re.IGNORECASE) != None:
                        result.append({key:i[list(i.keys())[0]]})
        return result
                    
                    
            
    def selfReplacement(self,key,nested):
        for i in nested:
            if type(i) == list:
                v= i[0]
                if type(v) == str:
                    if re.search(v,key,re.IGNORECASE) != None:
                        return i
            if type(i) == str:
                if re.search(i,key,re.IGNORECASE) != None:
                        return i 
                    
    def removeDict(self,direct,result):
        for i in direct:
            if type(i) == str:
                result.append(i)
            elif type(i) == list:
                if type(i[0]) == str:
                    result.append(i)
        return result               