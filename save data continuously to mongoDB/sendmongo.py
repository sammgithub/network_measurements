import pymongo, time 
import datetime as dt

myclient = pymongo.MongoClient("mongodb://153.90.118.238:27017/")
mydb = myclient["db1"]
mycol = mydb["test1"]

for i in range(10):

	mylist = [
	  # {"name": "Rifat"},
	  # {"address": "GCD"},
	  {"name": "Rifat", "time": (int(round(time.time() * 1000)))},
	  # {"time": (dt.datetime.now())}
	  # {"time": (time.time()*1000.0)}
	]
	x = mycol.insert_many(mylist)
	# time.sleep(1)
	print (i)