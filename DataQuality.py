import os
import json
import pandas as pd
import TestRunning as tr
import testSchema as ts
import schemaParser as sp
from statsmodels.sandbox.cox import Observation


    
def main():
    #Load Data
    print('import testing library')
    p_path = os.path.join('QualityGap_Data', 'Observation.json')
    with open(p_path, 'r') as f:
        Observation = json.load(f)
    print(tr.TestRunning(Observation, 'Observation'))
    
                
if __name__ == "__main__":
    main()
    
     

    

            

