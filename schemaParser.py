'''
Created on Jul 9, 2018

@author: Jason Zhang
'''

import dataquality_check
import numpy as np 
import errorlog
dqc = dataquality_check.dataqualityTest()


def cardinality_test(sourceType,resource,required_keys, resourceId):
    # Following are property with cardinality must greater than one
    # According to http://hl7.org/fhir/+sourceType
    Errors = []
    #Parsing self defined data schema
    for keys in required_keys:
        #if attribute is a list, which means cardinality > 1
        if type(keys) == list:
            # X data type in HL7
            if len(keys) > 1:
                if not any(k in list(resource.keys()) for k in keys):
                    source = sourceType +': '+ resourceId
                    raw = np.nan
                    etype = 'cardinality'
                    description = "Should including "+ keys[0]
                    error = errorlog.Error(source,raw,etype,description)
                    Errors.append(error)
            else:
                # required key parent is a list, which means cardinality > 1
                if type(keys[0]) == dict:
                    cardinality_test(sourceType,resource,[keys[0]],resourceId)
                # required key is a list
                else:
                    if keys[0] in list(resource.keys()):
                        for r in resource[keys[0]]:
                            if set(keys) > set(r.keys()):
                                source = sourceType +' :'+ resourceId
                                raw = np.nan
                                etype = 'cardinality'
                                description = "Should including "+ keys[0]
                                error = errorlog.Error(source,raw,etype,description)
                                Errors.append(error) 
        #the required attributes has a parent, which is not a list
        elif type(keys) == dict:
            for a in keys.keys():
                if a in list(resource.keys()):
                    attributes = resource[a]
                    #required attribute parent is a list, which means the cardinality of this attribute > 1
                    if type(attributes) == list: 
                        for attribute in attributes:
                            cardinality_test(sourceType,attribute, [keys[a]],resourceId)      
                    #required attribute parent is a value, which means the cardinality of this attribute = 1
                    else:
                        # check whether contains the required attribute
                        cardinality_test(sourceType,attributes, [keys[a]],resourceId)
        else:
            #required attribute is a single value
            if keys not in list(resource.keys()):
                    source = sourceType +': '+ resourceId
                    raw = np.nan
                    etype = 'cardinality'
                    description = "Should including "+ keys[0]
                    error = errorlog.Error(source,raw,etype,description)
                    Errors.append(error)
    return Errors



def reference_test(sourceType,resource,reference_keys, resourceId):
    Errors = []
    for keys in reference_keys:
        if type(keys) == list:
            #Reference attribute's parent is a list
            if type(keys[0]) == dict:
                reference_test(sourceType, resource,[keys[0]],resourceId)
            else:
            #Reference attribute is a list
                if keys[0] in list(resource.keys()):
                    for r in resource[keys[0]]:
                        if dqc.reference_check(r,sourceType,resourceId) != None:
                            Errors.append(dqc.reference_check(r,sourceType,resourceId))
        elif type(keys) == dict:
            #Reference attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    attributes = resource[key]
                    if type(attributes) == list:
                        for r in attributes:
                            reference_test(sourceType, r, [keys[key]],resourceId)
                    else:
                        reference_test(sourceType, attributes, [keys[key]],resourceId)
        else:
            #Reference attribute is a single value
            if keys in list(resource.keys()):
                if dqc.reference_check(resource[keys],sourceType,resourceId) != None:
                    Errors.append(dqc.reference_check(resource[keys],sourceType,resourceId))
    return Errors



def code_test(sourceType,resource, code_keys, resourceId):
    Errors = [] 
    for keys in code_keys:
        if type(keys) == list:
        #Code attribute's parent is a list
            if type(keys[0]) == dict:
                if set(keys[0].keys()) < set(resource.keys()):
                    for key in keys[0].keys():
                        attributes = resource[key]
                        if type(attributes) == list:
                            #Several code attribute share same parent
                            for r in attributes:
                                code_test(sourceType, r, [keys[0][key]],resourceId)
                        else:
                            #iterate to test code attribute
                            code_test(sourceType, attributes, [keys[0][key]],resourceId)
        if type(keys) == dict:
        #Code attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    #Check whether code in the code list
                    if type(keys[key]) == list:
                        if dqc.code_check(resource[key],keys[key], sourceType,resourceId)!= None:
                            Errors.append(dqc.code_check(resource[key],keys[key], sourceType,resourceId))
                    elif type(keys[key]) == dict:
                        code_test(sourceType,resource[key],[keys[key]],resourceId)
    return Errors

def codeConcept_test(sourceType,resource,codeConcept_keys, resourceId):
    Errors = []
    for keys in codeConcept_keys:
        if type(keys) == list:
            if type(keys[0]) == dict:
                #codeConcept attribute's parent is a list
                codeConcept_test(sourceType,resource,[keys[0]],resourceId)
            else:
                #codeConcept attribute is a list
                if keys[0] in list(resource.keys()):
                    for r in resource[keys[0]]:
                        if dqc.codeConcept_check(r, sourceType,resourceId) != None:
                            Errors.append(dqc.codeConcept_check(r, sourceType,resourceId))
        elif type(keys) == dict:
            #codeConcept attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    attributes = resource[key]
                    if type(attributes) == list:
                        for r in attributes:
                            codeConcept_test(sourceType,r, [keys[key]],resourceId)
                    else:
                        codeConcept_test(sourceType,attributes, [keys[key]],resourceId)
        else:
            #codeConcept is a single value
            if keys in list(resource.keys()):
                if dqc.codeConcept_check(resource[keys],sourceType,resourceId) != None:
                    Errors.append(dqc.codeConcept_check(resource[keys],sourceType,resourceId))
    return Errors

def value_test(sourceType, resource, flag, value_keys,resourceId):
    Errors = []
    for keys in value_keys:
        if type(keys) == list:
            #value attribute's parent is a list
            if type(keys[0]) == dict:
                value_test(sourceType, resource,flag,[keys[0]],resourceId)
            else:
                #test for different value type
                if keys[0] in list(resource.keys()):
                    for r in resource[keys[0]]:
                        if flag == 'humanname':
                            if dqc.name_test(r, sourceType,resourceId) != None:
                                Errors.append(dqc.name_test(r, sourceType,resourceId))
                        if flag == 'contactpoint':
                            if dqc.telecom_test(r,sourceType,resourceId) != None:
                                Errors.append(dqc.telecom_test(r, sourceType,resourceId))
                        if flag == 'address':
                            if dqc.address_test(r,sourceType,resourceId) != None:
                                Errors.append(dqc.address_test(r, sourceType,resourceId))
        elif type(keys) == dict:
            #value attribute's parent is a single value
            if set(keys.keys()) < set(resource.keys()):
                for key in keys.keys():
                    attributes = resource[key]
                    if type(attributes) == list:
                        for r in attributes:
                            value_test(sourceType, r, flag, [keys[key]],resourceId)
                    else:
                        value_test(sourceType, attributes, flag, [keys[key]],resourceId)
        else:
            #value attribute is a single value
            if keys in list(resource.keys()):
                if flag == 'humanname':
                    if dqc.name_test(resource[keys],sourceType,resourceId) != None:
                        Errors.append(dqc.name_test(resource[keys],sourceType,resourceId))
                if flag == 'contactpoint':
                    if dqc.telecom_test(resource[keys],sourceType,resourceId) != None:
                        Errors.append(dqc.telecom_test(resource[keys],sourceType,resourceId)) 
                if flag == 'address':
                    if dqc.address_test(resource[keys],sourceType,resourceId) != None:
                        Errors.append(dqc.address_test(resource[keys],sourceType,resourceId))
    return Errors                    
                            