'''
Created on Jul 9, 2018

@author: Jason Zhang
'''

import dataquality_check
import errorlog
import jsonschema
dqc = dataquality_check.dataqualityTest()


def schema_test(sourceType, resource, schema, Id):
    # Following are property with cardinality must greater than one
    # According to http://hl7.org/fhir/+sourceType
    Errors = []
    v = jsonschema.Draft4Validator(schema)
    for error in sorted (v.iter_errors(resource),key = str):
        path = error.absolute_path
        source = sourceType +':' + Id
        for p in list(path):
            source = source + '/' + str(p)
        raw = error.instance
        etype = 'schema'
        description = error.message
        #contained did not specify in schema, might have to find a another way.
        if not 'contained' in source:
            error = errorlog.Error(source, raw, etype,description)
            Errors.append(error)
    return Errors

def reference_test(sourceType,resource,reference_keys, path):
    Errors = []
    for keys in reference_keys:
        if type(keys) == list:
            #Reference attribute's parent is a list
            if type(keys[0]) == dict:
                reference_test(sourceType, resource,[keys[0]],path)
            else:
            #Reference attribute is a list
                if keys[0] in list(resource.keys()):
                    for r in resource[keys[0]]:
                        path = path + '/'+keys[0]
                        if dqc.reference_check(r,sourceType,path) != None:
                            Errors.append(dqc.reference_check(r,sourceType,path))
        elif type(keys) == dict:
            #Reference attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    attributes = resource[key]
                    path = path + '/'+key
                    if type(attributes) == list:
                        for r in attributes:
                            reference_test(sourceType, r, [keys[key]],path)
                    else:
                        reference_test(sourceType, attributes, [keys[key]],path)
        else:
            #Reference attribute is a single value
            if keys in list(resource.keys()):
                path = path + '/'+keys
                if dqc.reference_check(resource[keys],sourceType,path) != None:
                    Errors.append(dqc.reference_check(resource[keys],sourceType,path))
    return Errors
   

def codeConcept_test(sourceType,resource,codeConcept_keys, path):
    Errors = []
    for keys in codeConcept_keys:
        if type(keys) == list:
            if type(keys[0]) == dict:
                #codeConcept attribute's parent is a list
                codeConcept_test(sourceType,resource,[keys[0]],path)
            else:
                #codeConcept attribute is a list
                if keys[0] in list(resource.keys()):
                    for r in resource[keys[0]]:
                        path = path + '/'+keys[0]
                        if dqc.codeConcept_check(r, sourceType,path) != None:
                            Errors.append(dqc.codeConcept_check(r, sourceType,path))
        elif type(keys) == dict:
            #codeConcept attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    attributes = resource[key]
                    path = path + '/'+key
                    if type(attributes) == list:
                        for r in attributes:
                            codeConcept_test(sourceType,r, [keys[key]],path)
                    else:
                        codeConcept_test(sourceType,attributes, [keys[key]],path)
        else:
            #codeConcept is a single value
            if keys in list(resource.keys()):
                path = path + '/'+keys
                if dqc.codeConcept_check(resource[keys],sourceType,path) != None:
                    Errors.append(dqc.codeConcept_check(resource[keys],sourceType,path))
    return Errors

def value_test(sourceType, resource, flag, value_keys,path):
    Errors = []
    for keys in value_keys:
        if type(keys) == list:
            #value attribute's parent is a list
            if type(keys[0]) == dict:
                value_test(sourceType, resource,flag,[keys[0]],path)
            else:
                #test for different value type
                if keys[0] in list(resource.keys()):
                    for r in resource[keys[0]]:
                        path = path + '/'+keys[0]
                        if flag == 'humanname':
                            if dqc.name_test(r, sourceType,path) != None:
                                Errors.append(dqc.name_test(r, sourceType,path))
                        if flag == 'contactpoint':
                            if dqc.telecom_test(r,sourceType,path) != None:
                                Errors.append(dqc.telecom_test(r, sourceType,path))
                        if flag == 'address':
                            if dqc.address_test(r,sourceType,path) != None:
                                Errors.append(dqc.address_test(r, sourceType,path))
        elif type(keys) == dict:
            #value attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    attributes = resource[key]
                    path = path + '/'+key
                    if type(attributes) == list:
                        for r in attributes:
                            value_test(sourceType, r, flag, [keys[key]],path)
                    else:
                        value_test(sourceType, attributes, flag, [keys[key]],path)
        else:
            #value attribute is a single value
            if keys in list(resource.keys()):
                path = path + '/'+keys
                if flag == 'humanname':
                    if dqc.name_test(resource[keys],sourceType,path) != None:
                        Errors.append(dqc.name_test(resource[keys],sourceType,path))
                if flag == 'contactpoint':
                    if dqc.telecom_test(resource[keys],sourceType,path) != None:
                        Errors.append(dqc.telecom_test(resource[keys],sourceType,path)) 
                if flag == 'address':
                    if dqc.address_test(resource[keys],sourceType,path) != None:
                        Errors.append(dqc.address_test(resource[keys],sourceType,path))
    return Errors                    
                            