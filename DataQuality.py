import os
import json
import pandas as pd
import schemaParser as sp
import TestRunning as tr
import testSchema as ts



    
def main():
    #Load Data
    p_path = os.path.join('QualityGap_Data', 'Report.json')
    with open(p_path, 'r') as f:
        Report = json.load(f)
    print(type(Report))
    print(tr.TestRunning(Report, 'Report'))
        
if __name__ == "__main__":
    main()
     
    
    

            

