import os, uuid
import pymongo
import json

from pathlib import Path
from argparse import ArgumentParser

class StackrMetaData:
    def __init__(self, module: str, submodule: str, stackrId: str, version: str) -> None:
        self.module = module
        self.submodule = submodule
        self.stackrId = stackrId
        self.version = version
    
    #def toJSON(self):
    #    return json.dumps(self, default=lambda o: o.__dict__, 
    #        sort_keys=True, indent=4)

class StackrTestData:
    def __init__(self, metadata, testdata) -> None:
        self.metadata = metadata
        self.testdata = testdata

class StackrDecisionData:
    def __init__(self, metadata, decisiondata) -> None:
        self.metadata = metadata
        self.decisiondata = decisiondata

class StackrPlanData:
    def __init__(self, metadata, plandata) -> None:
        self.metadata = metadata
        self.plandata = plandata

class StackrEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

#
# Argument parsing
#
parser = ArgumentParser()
parser.add_argument("-m", "--modulename", type=str, required=True,
                    help="the module name to associate this record with, example: stackrModule")
parser.add_argument("-s", "--submodulename", type=str, required=True,
                    help="the submodule name to associate this record with, example: resourceGroup")
parser.add_argument("-o", "--mongodb", type=str, required=True,
                    help="the mongodb instance to connect to, example: stackrstore.icriak4.mongodb.net")
parser.add_argument("-p", "--password", type=str, required=True,
                    help="the password for the MongoDB connection")
parser.add_argument("-b", "--basepath", type=str, required=True,
                    help="the base path of the different data files to upload, example: /home/runner/work/stackrModule/stackrModule/")
parser.add_argument("-c", "--cucumberlocation", type=str, required=True,
                    help="the location of the cucumber.json file to upload, example: stackrModule/test/resourceGroup/results")
parser.add_argument("-d", "--decisionloglocation", type=str, required=True,
                    help="the location of the opa decision logs to upload, example: <no example yet>")
parser.add_argument("-t", "--tfplanlocation", type=str, required=True,
                    help="the location of the hcl plans in json to upload, example: stackrModule/plan.json")

args = parser.parse_args()

#
# Print out the different cmd line parameters
#
print(f"Module Name: {args.modulename}")
print(f"Submodule Name: {args.submodulename}")
print(f"MongoDB Instance: {args.mongodb}")
print(f"Password: <not revealed>")
print(f"Basepath: {args.basepath}")
print(f"Cucumber Location: {args.cucumberlocation}")
print(f"Decision Log Location: {args.decisionloglocation}")
print(f"TF Plan Location: {args.tfplanlocation}")

#
# Connect to MongoDB and set the correct database
#
dbclient = pymongo.MongoClient(f"mongodb+srv://svengauggel:{args.password}@{args.mongodb}/?retryWrites=true&w=majority")
db = dbclient["stackrStore"]

metadataCollection = db["metaData"]

filter = {'moduleName' : f'{args.modulename}',
          'subModuleName' : f'{args.submodulename}'}
metadataRecordStr = metadataCollection.find_one(filter, sort=[("version", pymongo.DESCENDING)])
metadataRecordJson = None
if metadataRecordStr:
    print("We have found a record so it seems we're adding a new one now")
    metadataRecordJson = json.loads(metadataRecordStr)
else:
    print("Seems like this is the first record for this module/submodule")

# generate the new metadata for this record
idStr = str(uuid.uuid4())
if metadataRecordJson == None:
    oldVersion = 0
else:
    oldVersion = int(metadataRecordJson['version'])
newVersion = oldVersion + 1
newMetadataRecord = StackrMetaData(args.modulename, args.submodulename, idStr, newVersion)

#
# Upload the metadata for stackrModule
#
metadataResultCollection = db["metaData"]
metaNo = metadataResultCollection.insert_one(newMetadataRecord.__dict__)

#
# Upload the cucumber.json file for stackrModule
#
jsonFileTest = open(f"{args.basepath}/{args.cucumberlocation}")
jsonStringTest = jsonFileTest.read()
jsonDataTest = json.loads(jsonStringTest)[0]
jsonDataTest.update({"uuid": idStr, "version": newVersion})
testResultCollection = db["testResults"]
testNo = testResultCollection.insert_one(jsonDataTest)

#
# Upload the module HCL plan in json format for stackrModule
#
jsonFilePlan = open(f"{args.basepath}/{args.tfplanlocation}")
jsonStringPlan = jsonFilePlan.read()
jsonDataPlan = json.loads(jsonStringPlan)
jsonDataPlan.update({"uuid": idStr, "version": newVersion})
planCollection = db["modulePlans"]
planNo = planCollection.insert_one(jsonDataPlan)

#
# Upload the decision logs for stackrModule
#
#jsonFileDecision = open(f"{args.basepath}{args.decisionloglocation}")
#jsonStringDecision = jsonFileDecision.read()
#jsonDataDecision = json.loads(jsonStringDecision)[0]
#jsonDataDecision.update({"uuid": idStr, "version": newVersion})
#decisionLogCollection = db["decisionLogs"]
#decisionNo = decisionLogCollection.insert_one(jsonDataDecision)
