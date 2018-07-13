'''
Created on Jul 13, 2018

@author: User1
'''
import pandas as pd
import schemaParser as sp
import testSchema as ts

#Running function that parse the schema and test the raw data
def TestRunning(data,flag):
    schema = ts.TestSchema(flag)
    ErrorList = []
    #Loop over each resource instance
    for resource in data:
        #Show progress
        print('Analyzing '+ flag + ": "+ resource['id'])
        #Combining Error
        ErrorList = ErrorList + sp.codeConcept_test(flag,resource,schema.codeConcept_keys,resource['id']) \
        + sp.cardinality_test(flag,resource,schema.required_keys,resource['id']) \
        +sp.reference_test(flag,resource,schema.reference_keys,resource['id']) \
        +sp.code_test(flag,resource,schema.code_keys,resource['id']) 
        #Special case test
        if flag == 'Patient':
            ErrorList = ErrorList + sp.value_test(flag,resource,'humanname',schema.name_keys,resource['id']) \
            +sp.value_test(flag,resource,'contactpoint',schema.contact_keys,resource['id']) \
            +sp.value_test(flag,resource,'address',schema.address_keys,resource['id']) 
    return (pd.DataFrame.from_records(e.to_dict() for e in ErrorList))
