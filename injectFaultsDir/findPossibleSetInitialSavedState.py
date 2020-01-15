#!/usr/local/bin/python3
import os
import re

#I'm not sure my initial approach makes the most sense because the Fragment instance
#may be different when you move it around

startingDir = '/Users/zack/git/reposFromFDroid/'
newInstanceDeclarationPattern = re.compile('public static .* newInstance(){')
for root, dirs, files in os.walk(startingDir, topdown=False):
  for f in files:
    if f.endswith('.java'):
      fullFilename = os.path.join(root,f)
      with open(fullFilename,'r') as fin:
        linesOfInterest = []
        lineStartsWithAFragment = False
        isActivity = False
        isFragment = False
        isNewInstance = False
        for lineCount, line in enumerate(fin):
          line = line.strip()
          if isNewInstance and '}' in line:
            isNewInstance = False
          elif not isFragment and not isActivity and line.startswith('public class'):
            if 'Fragment' in line:
              isFragment = True
            elif 'Activity' in line:
              isActivity = True
          elif newInstanceDeclarationPattern.match(line):
            print('found new instance!!!')
            print(line)
            inNewInstance = True
          else:
            lineItems = line.split(' ')
            if lineItems[0].endswith('Fragment') and '=' in line:
              if isActivity:
                print('is activity')
              if isFragment:
                print('is fragment')
              print(line)
              linesOfInterest.append(lineCount)
              lineStartsWithAFragment = True
        if lineStartsWithAFragment:
          #print('file: {0} contains FragmentManager in line: {1}'.format(fullFilename, lineCount))
          print('file of interest: {0}, lines of interest: {1}'.format(fullFilename, linesOfInterest))
          input('stopping here to check file. Press enter when finished to move to next one')