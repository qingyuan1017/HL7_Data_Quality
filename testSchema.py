'''
Created on Jul 11, 2018

@author: Jason Zhang
'''

class TestSchema:
    #Schema for different resource in FHIR Release (STU)
    required_keys = []
    reference_keys = []
    codeConcept_keys = []
    code_keys = []
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
        self.required_keys = [{'animal':'species'},[{'communication':'language'}]]
        self.reference_keys = [[{'contact':'organization'}],['generalPractitioner'],'managingOrganization',[{'link':'other'}]]
        self.codeConcept_keys = ['maritalStatus',[{'contact':['relationship']}],{'animal':'species'},{'animal':'breed'},
                            {'animal':'genderStatus'}]
        self.code_keys = [{'gender':['male','female','other','unknown']}, [{'contact':{'gender':['male','female','other','unknown']}}],
                    [{'link':{'type':['replaced-by','replaces','refer','seealso']}}]]
        self.name_keys = [['name'],[{'contact':'name'}]]
        self.contact_keys = [['telecom'],[{'contact':['telecom']}]]
        self.address_keys = [['address'],[{'contact':'address'}]]

    def allergyintoleranceSchema(self):
        self.required_keys = ['verificationStatus','patient',[{'reaction':['manifestation']}]]
        self.reference_keys = ['patient','recorder','asserter']
        self.codeConcept_keys = ['code',[{'reaction':['manifestation']}],[{'reaction':'substance'}]]
        self.code_keys = [{'clinicalStatus':['active','inactive','resolved']},{'verificationStatus':['unconfirmed','confirmed','refuted','entered-in-error']},
                    {'type':['allergy','intolerance']},[{'category':['food','medication','environment','biologic']}],{'criticality':['low','high','unable-to-assess']},
                    [{'reaction':{'severity':['mild','moderate','severe']}}]]


    def conditionSchema(self):
        self.required_keys = ['subject']
        self.reference_keys = ['subject','context','asserter',{"stage":['assessment']},
                         {"evidence":['detail']}]
        self.codeConcept_keys = [['category'],'severity','code',['bodySite'],{'stage':'summary'},
                           [{'evidence':['code']}]]
        self.code_keys = [{"clinicalStatus":['active','recurrence','inactive','remission','resolved']},
                    {"verificationStatus":['provisional','differential','confirmed','refuted','entered-in-error','unknown']}]


    def observationSchema(self):
        self.required_keys = ['status','code',[{"related":"target"}],[{"component":"code"}]]
        self.reference_keys = [['basedOn'],'subject','context',['performer'],"specimen","device",
                   [{'related':'target'}]]
        self.codeConcept_keys = [['category'],'valueCodeableConcept','code','dataAbsentReason',
                    'interpretation','bodySite','method',{'referenceRange':'type'},{'referenceRange':'appliesTo'},
                    [{"component":"valueCodeableConcept"}],[{"component":"dataAbsentReason"}],
                    [{"component":"interpretation"}],[{"code"}]]
        self.code_keys = [{"status":['registered','preliminary','final','amended','resolved']},
                    [{"related":{'type':['has-member','derived-from','sequel-to','replaces','qualified-by','interfered-by']}}]]


    def familyhistorySchema(self):
        self.required_keys = ['status','patient','relationship',[{"condition":"code"}]]
        self.reference_keys = ['patient','reasonReference']
        self.codeConcept_keys = ['notDoneReason','relationship',['reasonCode'],
                    [{"condition":'code'}],[{'condition':'outcome'}]]
        self.code_keys = [{"status":['partial','completed','enter-in-error','health-unknown']},
            {"gender":['male','female','other','unknown']}]

    def reportSchema(self):
        self.required_keys = ['status','code',[{"image":"link"}],[{"performer":"actor"}]]
        self.reference_keys = ['subject','context',['specimen'],['result'],['imagingStudy']]
        self.codeConcept_keys = ['category','code',[{'performer':'role'}],['codedDiagonosis']]
        self.code_keys = [{"status":['partial','registered','preliminary','final']}]


    def immunizationSchema(self):
        self.required_keys = ['status','notGiven','vaccineCode','patient',[{'practitioner':'actor'}],{'vaccinationProtocol':['targetDisease']},
                        [{'vaccinationProtocol':'doseStatus'}]]
        self.reference_keys = ['patient','encounter','location','manufacturer',[{'practitioner':'actor'}],
                         [{'reaction':'detail'}],[{'vaccinationProtocol':'authority'}]]
        self.codeConcept_keys = ['vaccineCode','reportOrigin','site','route',[{'practitioner':'role'}],
                    {'explanation': ['reason']},{'explanation': ['reasonNotGiven']},
                    [{'vaccinationProtocol':['targetDisease']}],[{'vaccinationProtocol':'doesStatus'}],[{'vaccinationProtocol':'doseStatusReason'}]]
        self.code_keys = [{"status":['completed','entered-in-error']}]

    def careplanSchema(self):
        self.required_keys = ['status','intent','subject',[{'activity':{'detail':'status'}}]]
        self.reference_keys = [['definition'],['basedOn'],['replaces'],['partOf'],'subject','context',['author'],
                        ['careTeam'],['addresses'],['supportingInfo'],['goal'],
                        [{'activity':['outcomeReference']}],[{'activity':'reference'}],
                        [{'activity':{"detail":'definition'}}],[{'activity':{"detail":['reasonReference']}}],
                        [{'activity':{"detail":['goal']}}],[{'activity':{"detail":'location'}}],
                        [{'activity':{"detail":['performer']}}],[{'activity':{"detail":['productReference']}}]]
        self.codeConcept_keys = [['category'],[{'activity':['outcomeCodeableConcept']}],
                            [{'activity':{'detail':'category'}}],[{'activity':{'detail':'code'}}],
                            [{'activity':{'detail':['reasonCode']}}]]
        self.code_keys = [{"status":['draft','active','suspended','completed','entered-in-error','cancelled','unknown']},
                     {"intent":['proposal','plan','order','option']}]

    def procedureSchema(self):
        self.required_keys = ['status','subject',[{'performer':'actor'}],[{'focalDevice':'manipulated'}]]
        self.reference_keys = [['definition'],['basedOn'],['partOf'],'subject','context',[{'performer':'actor'}],
                         [{'performer':'onBehalfOf'}],'location',['reasonReference'],['report'],['complicationDetail'],
                         [{'focalDevice':'manipulated'}],['usedReference']]
        self.codeConcept_keys = ['notDoneReason','category','code',[{'performer':'role'}],
                           ['reasonCode'],['bodySite'],'outcome',['complication'],['followUp'],
                           [{'focalDevice':'action'}],['usedCode']]
        self.code_keys = [{"status":['preparation','in-progress','suspended','aborted','completed',
                                'entered-in-error','unknown']}]

    def deviceSchema(self):
        self.required_keys = []
        self.reference_keys = ['patient','owner','location']
        self.codeConcept_keys = ['type',['safety']]
        self.code_keys = [{'udi':{'entryType':['barcode','rfid','manual']}},
                    {'status':['active','inactive','entered-in-error','unknown']}]
        self.contact_keys = [['contact']]                          

    def documentSchema(self):
        self.required_keys = ['status','type','indexed',[{'relatesTo':'code'}],['content'],[{'content':'attachment'}]]
        self.reference_keys = ['subject',['author'],'authenticator','custodian',[{'relatesTo':'target'}],
                        {'context':'encounter'},{'context':'sourcePatientInfo'},[{'related':'ref'}]]
        self.codeConcept_keys = ['type','class','securityLabel',{'context':'facilityType'},
                            {'context':'practiceSetting'}]
        self.code_keys = [[{'relatesTo':{'code':['replaces','transforms','signs','appends']}}],
                    {'status':['current','superseded','entered-in-error']},
                    {'docStatus':['preliminary','final','appended','amended','entered-in-error']}]           