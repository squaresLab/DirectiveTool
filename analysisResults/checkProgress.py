#!/usr/local/bin/python3

count = 0
#with open('serverRunResults.txt','r') as fin:
with open('fDroidErrorsSecondPass.txt','r') as fin:
  for line in fin:
    line = line.strip()
    if line.startswith("error;"):
      checker = line.split(" ")[4]
      apkName = line.split(" ")[-1]
      #print('{0}: {1} on {2}'.format(count, checker, apkName))
      if apkName == "it.eternitywall.eternitywall_33.apk":
        currentPosition = count
      count += 1
print('total count: {0}'.format(count))
print('current position: {0}'.format(currentPosition))

