import pymongo

myclient = pymongo.MongoClient("mongodb+srv://svengauggel:XclhGMUvl1NNzRA2@stackrstore.icriak4.mongodb.net/test")
mydb = myclient["mongodbVSCodePlaygroundDB"]
mycol = mydb["sales"]

myquery = { "item": "abc" }
mydoc = mycol.find(myquery)
for x in mydoc:
  print(x)
