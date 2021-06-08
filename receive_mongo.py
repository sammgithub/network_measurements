import pymongo, time
import datetime as dt

# while True:
myclient = pymongo.MongoClient("mongodb://153.90.118.238:27017/")
t1 = int(round(time.time() *1000.0))
mydb = myclient["db1"]
mycol = mydb["test1"]
t2 = mycol.find({},{'_id': False})

for x in t2:
	t1
	time.sleep(1)
	print (t1-x['time'])