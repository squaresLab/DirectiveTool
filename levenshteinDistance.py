#!/usr/local/bin/python3

import sys
import os

#function taken from https://stackoverflow.com/questions/2460177/edit-distance-in-python
def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

#this function finds the new apk name in a repo when the build process changes the apk
#name slightly
def findAPKInRepo(repo, apkName):
    apkList = []
    for root, dirs, files in os.walk(repo):
        for f in files:
            if f.endswith('.apk'):
                apkList.append(os.path.join(root, f))
    if len(apkList) < 1:
        print('error: unable to find any apks in repo: {0}'.format(repo))
        sys.exit(1)
    elif len(apkList) == 1:
        return apkList[0]
    else:
        currentClosest = apkList[0]
        currentMin = levenshteinDistance(apkName, apkList[0])
        for testApk in apkList[1:]:
            testMin = levenshteinDistance(apkName, testApk)
            if testMin < currentMin:
                currentMin = testMin
                currentClosest = testApk
        return currentClosest



if __name__=="__main__":
    orig1 = 'org.flyve.mdm.agent_2020-01-22_210349-fcm-debug.apk'
    test1 = 'org.flyve.mdm.agent_2020-01-22_211120-fcm-debug.apk'
    test2 = 'org.flyve.mdm.agent_2020-01-22_211120-mqtt-debug.apk'
    print(levenshteinDistance(orig1, test1))
    print(levenshteinDistance(orig1, test2))