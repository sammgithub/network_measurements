import subprocess, json, re
from random import random
from statistics import median
# import numpy
# "http://www.youtube.com","http://www.facebook.com","http://www.baidu.com","http://www.wikipedia.org","http://www.qq.com",

urls = ["http://www.taobao.com","http://www.tmall.com","http://www.amazon.com","http://www.sohu.com","http://www.weibo.com","http://www.reddit.com","http://www.csdn.net","http://www.twitch.tv","http://www.aliexpress.com","http://www.microsoft.com","http://www.tribunnews.com","http://www.ebay.com","http://www.wordpress.com","http://www.msn.com","http://www.apple.com","http://www.imgur.com","http://www.adobe.com","http://www.pinterest.com","http://www.fandom.com","http://www.paypal.com"]
		

def getMetrics(url,Nrun):
	speedIndexData=[]
	for i in range(Nrun):
		print("iteration no: " + str(i+1))
		res=subprocess.check_output("pwmetrics %s --json" % url, shell=True)
		res = res.decode("utf-8")
		# print(res)
		res = re.sub(r"[^\{]*","",res,1)
		res = json.loads(res)
		runs=res["runs"]

		speedIndex=None

		for run in runs:
				for timing in run["timings"]:
						if timing["id"]=="speedIndex":
							speedIndex = timing["timing"]
							break
		if speedIndex is None:
			speedIndex =0
		#return speedIndex
		speedIndexData.append(speedIndex)
	print(speedIndexData)
	print(median(speedIndexData))
	# print(sum(speedIndexData)/Nrun)
	return median(speedIndexData)

def write2File(speedIndex, bandwidth, latency, source):
	global file
	file.write( "%s,%s,%s,%s\n" % (speedIndex, bandwidth, latency, source))

def getMin(choice_l):
	#print(choice_l)
	choice_l=sorted(choice_l)
	#print(sorted(choice_l))
	print(choice_l)
	return choice_l[0]
bandwidth_l=[128,256,512,1024,2048,4096,8192,16384,24576,32768,40960,49152,57344,65536,73728,81920]
latency_l=[150,140,130,120,110,100,90,80,70,60,50,40,30,20,10,0]
Nrun=9
# bandwidth_l=[1024,2048]
# latency_l=[20,10]

with open("sidata.csv", "a") as file:
	file.write("speedIndex,bandwidth,latency,source\n")
	for url in urls:
		# source=re.sub(r"^[^\.]+\.|\.[^\.]+$","",url)
		source=re.sub(r"^[^\.]+\.","",url)
		source=re.sub(r"\..*$","",source)
		b_ix = 0
		l_ix = 0
		point_recorded = False
		# datetime.datetime.now()
		choice_l = []
		subprocess.check_output("sudo tc qdisc add dev eno1 root handle 1:0 netem delay %sms && sudo tc qdisc add dev eno1 parent 1:1 handle 10: tbf rate %skbit buffer 1600 limit 10000" % (latency_l[l_ix], bandwidth_l[b_ix]), shell=True)
		si_0=getMetrics(url,Nrun)

		print('First point (bw %d, lat %d)(bnd %d, ltn %d) SI index %d' %  (b_ix,l_ix,bandwidth_l[b_ix],latency_l[l_ix],si_0))
		choice_l.append([si_0, l_ix, b_ix])
		subprocess.check_output("sudo tc qdisc del dev eno1 root", shell=True)

		if not point_recorded:
			# write2File(si_0,bandwidth_l[b_ix],latency_l[l_ix], source)
			point_recorded = True
		while b_ix < len(bandwidth_l) and l_ix < len(latency_l):
			flag=0
			if(l_ix+1<len(bandwidth_l)):
				subprocess.check_output("sudo tc qdisc add dev eno1 root handle 1:0 netem delay %sms && sudo tc qdisc add dev eno1 parent 1:1 handle 10: tbf rate %skbit buffer 1600 limit 10000" % (latency_l[l_ix+1], bandwidth_l[b_ix]), shell=True)
				si_1=getMetrics(url,Nrun)
				print('Second point (b_point %d, l_point %d)(band %d, lat %d) SI index %d'% (b_ix,l_ix+1,bandwidth_l[b_ix],latency_l[l_ix+1],si_1))
				choice_l.append([si_1, l_ix+1, b_ix])
				subprocess.check_output("sudo tc qdisc del dev eno1 root", shell=True)
				flag+=1
				
			if(b_ix+1<len(bandwidth_l)):
				subprocess.check_output("sudo tc qdisc add dev eno1 root handle 1:0 netem delay %sms && sudo tc qdisc add dev eno1 parent 1:1 handle 10: tbf rate %skbit buffer 1600 limit 10000" % (latency_l[l_ix], bandwidth_l[b_ix+1]), shell=True)
				si_2=getMetrics(url,Nrun)
				print('Third point (b_point %d, l_point %d)(band %d, lat %d) SI index %d' % (b_ix+1,l_ix,bandwidth_l[b_ix+1],latency_l[l_ix],si_2))
				choice_l.append([si_2, l_ix, b_ix+1])
				subprocess.check_output("sudo tc qdisc del dev eno1 root", shell=True)
				flag+=1
			if(flag==0):
				break
			print(getMin(choice_l))
			si, l_ix, b_ix= getMin(choice_l)
			# print(si)
			# print(l_ix)
			# print(b_ix)
			# print(time_si)
			
			if(si==si_0):
				print("no change")
				#continue
			else:
				write2File(si,bandwidth_l[b_ix],latency_l[l_ix], source)
			
			si_0=si
			choice_l = []
			choice_l.append([si, l_ix, b_ix])