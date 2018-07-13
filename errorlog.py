'''
Created on Jul 13, 2018

@author: Jason Zhang
'''
class Error:
    #Error class defines the error
    def __init__(self,source,raw,etype,description):
        self.source = source
        self.raw = raw
        self.etype = etype
        self.description = description
    
    def to_dict(self):
        # convert to dict, which make it easy to use pandas dataframe
        return{
                'source': self.source,
                'raw': self.raw,
                'type':self.etype,
                'description': self.description
            }
        