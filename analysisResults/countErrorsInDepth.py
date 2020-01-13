#!/usr/local/bin/python3

#DetectInvalidSetContentViewFindViewByIDOrdering: 1591
#DetectIncorrectGetActivityMain: 1078
#DetectMissingSetHasOptionsMenu: 942
#DetectInvalidGetResources: 937
#DetectIncorrectSetInitialSavedState: 938
#DetectInvalidSetTheme: 953
#DetectSetSelectorSetPackageProblem: 980
#DetectInvalidInflateCallMain: 936
#DetectSetArgumentsMain: 936

import collections

errorCountDict = collections.defaultdict(int)
with open('fullResults.txt','r') as fin:
  for line in fin:
    line = line.strip()
    if line.startswith("error; couldn't run:"):
      errorCountDict[line.split(" ")[4]] += 1
for checker in errorCountDict:
  print('{0}: {1}'.format(checker,errorCountDict[checker]))
