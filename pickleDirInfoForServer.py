#!/usr/local/bin/python3

import pickle
import os

appsDir = '/Users/zack/git/DirectiveTool/appsFromFDroid/'
basePath = '/Users/zack/git/DirectiveTool/' 

appsList = os.listdir(appsDir)
saveFile = os.path.join(basePath, 'appsName.pickle')
pickle.dump(appsList, open(saveFile,'wb'))
print('saved to {0}'.format(saveFile))

