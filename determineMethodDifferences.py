#!/usr/local/bin/python3

import javalang
import time
import sys
import traceback
import os

#important! remember that line numbers are 0 indexed in this file

errorFile = 'errorLog.txt'

class lineCheckInfo:
  def __init__(self, originalStatement, methodCallList, typeList, lineNumber):
    self.originalStatement = originalStatement
    self.methodCallList = methodCallList
    self.typeList = typeList
    self.lineNumber = lineNumber

def getFullNameOfArg(arg):
  #if arg.qualifier.startswith('R.'):
  #  print('{0} might be a static file'.format(arg))
  #  traceback.print_stack()
  #  sys.exit(1)
  if (isinstance(arg, javalang.tree.MemberReference)):
    if (arg.qualifier == "" or arg.qualifier == None):
      varName = arg.member
    else: 
      varName = arg.qualifier + "." + arg.member
    return varName
  elif (isinstance(arg, javalang.tree.Literal)):
      if arg.qualifier == None or arg.qualifier == "" or arg.qualifier == []:
        return arg.value
      else:
        return '{0}.{1}'.format(arg.qualifier,arg.value)
  else: 
    #There are abnormal parameters, like string being concatenated, that I don't 
    #currently handle
    #returning None for those case
    #another case is global variables that I don't have the type info for
    return None
    #traceback.print_stack()
    #print('invalid type: {0}'.format(type(arg)))
    #print(arg)
    #sys.exit(1)


def getTypeOfVar(dictToUse, varName):
  if varName.startswith("R."):
    return "StaticFile"
  if varName == 'true' or varName == 'false':
    #return "bool"
    #I think I want to meaningfully differentiate between true and false
    return varName
  else:
    #first example of this case was a global variable, which I'm currently
    #not handling; I'll have to look into if not handling those cases are a 
    #problem later
    if varName in dictToUse:
      return dictToUse[varName]
    else:
      return None
    #if not varName in dictToUse:
      #THis is probably the wrong way to handle this problem, 
      #but stopping the execution for now so I can look at individual 
      #cases instead of making assumptions about how to handle it
    #  print('error: {0} not in {1}'.format(varName, dictToUse))
    #  traceback.print_stack() 
    #  print('about to exit')
    #  sys.exit(1)
    #else:


#deciding to 0 index this list
def getStatementNumberXFromParseTree(parseTree, statementNumber):
  node = parseTree.types[0].body[0]
  statementList = []
  for s in node.body:
    if isinstance(s, javalang.tree.StatementExpression):
      statementList.append(s)
  return statementList[statementNumber]


#TODO: about to add this; actually, I'm not sure that it isn't a better idea
#to recreate the line from the parse tree information. I'm going to stop on this
#method and try the other approach and then come back to this if necessary
#commenting out for now
#def createNodeToLineNumberList(fileInput, fileTree):
  #lineIndex = 0
  #lineList = fileInput.splitlines()
  #currentLine = lineList[lineIndex]
  #methodStatementList = fileTree.types[0].body[0].body
  #methodStatementIndex = 0
  #methodStatementToLineListMapping = {}
  #nestingCount = 0
  #while(methodStatementIndex < len(methodStatementList) and lineIndex < len(lineList)):
    ##currently making the assumption that there aren't random ;'s in the file
    #may want to adjust this later if I notice the assumption is wrong
    #for c in currentLine:
      #if c == '{':
        #nestingCount = nestingCount + 1
      #elif c == '}':
        #nestingCount = nestingCount + 1

#note, this method often doesn't add the ';' at the end of the line at the moment    
def nodeToCodeLine(node):
  def isBlank(nodeAttribute):
    if nodeAttribute == None or nodeAttribute == "" or nodeAttribute == []:
      return True
    else:
      return False
  def testAttributesNotHandledAreBlank(node, nodeAttributeList):
    for n in nodeAttributeList:
      if not isBlank(getattr(node,n)):
        print('error: unsupported attribute {0} for node: {1}'.format(n, node))
        sys.exit(1)
  def prependQualifierIfProvided(currentString, possibleQualifier):
    if isBlank(possibleQualifier):
      return currentString
    else:
      return '{0}.{1}'.format(possibleQualifier, currentString)
  if isinstance(node, javalang.tree.StatementExpression):
    unsupportedAttributes = ["label"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return nodeToCodeLine(node.expression)
  elif isinstance(node, javalang.tree.MethodInvocation):
    unsupportedAttributes = ["postfix_operators", "prefix_operators"]
    #selectors are how the multiple function calls are chained together
    selectorString = ''
    if not isBlank(getattr(node, "selectors")):
      for s in node.selectors:
        selectorString = '{0}.{1}'.format(selectorString, nodeToCodeLine(s))
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    argumentItemStrings = [nodeToCodeLine(a) for a in node.arguments]
    argumentString = ','.join(argumentItemStrings)
    methodCallWithoutQualifier = '{0}({1}){2}'.format(node.member, argumentString, selectorString)
    return prependQualifierIfProvided(methodCallWithoutQualifier, node.qualifier)
  elif isinstance(node, javalang.tree.SuperMethodInvocation):
    unsupportedAttributes = ["postfix_operators", "prefix_operators", "selectors","type_arguments"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    argumentItemStrings = [nodeToCodeLine(a) for a in node.arguments]
    argumentString = ','.join(argumentItemStrings)
    methodCallWithoutQualifier = '{0}({1})'.format(node.member, argumentString)
    resultWithoutSuperCall = prependQualifierIfProvided(methodCallWithoutQualifier, node.qualifier)
    return 'super.{0}'.format(resultWithoutSuperCall)
  elif isinstance(node, javalang.tree.Literal):
    unsupportedAttributes = ["postfix_operators", "prefix_operators", "selectors"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return prependQualifierIfProvided(node.value, node.qualifier)
  elif isinstance(node, javalang.tree.MemberReference):
    unsupportedAttributes = ["postfix_operators", "prefix_operators", "selectors"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    if isinstance(node.member, str):
      memberString = node.member
    else:
      memberString = nodeToCodeLine(node.member)
    return prependQualifierIfProvided(memberString, node.qualifier)
  elif isinstance(node, javalang.tree.LocalVariableDeclaration):
    unsupportedAttributes = ["annotations"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    #for some reason the default modifiers here is the empty set string, so 
    #have to check for that explicitly
    if not len(getattr(node,"modifiers")) < 1:
      print('error: unsupported attribute {0} for node: {1}'.format("modifiers", node))
      print('found |{0}| instead of set()'.format(getattr(node,"modifiers")))
      print('comparison result: {0}'.format(getattr(node,"modifiers") == "set()"))
      print('type is {0}'.format(type(getattr(node,"modifiers"))))
      sys.exit(1)
    else:
      declaratorList = [ nodeToCodeLine(d) for d in node.declarators] 
      declaratorsString = ','.join(declaratorList)
      return '{0} {1};'.format(nodeToCodeLine(node.type), declaratorsString)
  elif isinstance(node, javalang.tree.VariableDeclarator):
    unsupportedAttributes = ["dimensions"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    if isBlank(getattr(node, "initializer")):
      return node.name
    else:
      return '{0} = {1}'.format(node.name, nodeToCodeLine(node.initializer))
  elif isinstance(node, javalang.tree.Assignment):
    #unsupportedAttributes = []
    #testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return '{0} = {1};'.format(nodeToCodeLine(node.expressionl), nodeToCodeLine(node.value))
  #block handling is controversal in my opinion, since I'm probably only intersted in the 
  #condition, when I run into an instance or this case; however, I'll also return the 
  #inner block contents at the moment and allow another method to extract the important
  #parts
  elif isinstance(node, javalang.tree.IfStatement):
    unsupportedAttributes = ["label"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    if isBlank(node.else_statement):
      return 'if({0}){{\n{1}}};'.format(nodeToCodeLine(node.condition), nodeToCodeLine(node.then_statement))
    else:
      return 'if({0}){{\n{1}\n}}\nelse{{\n{2}\n}};'.format(nodeToCodeLine(node.condition), nodeToCodeLine(node.then_statement), nodeToCodeLine(node.else_statement))
  elif isinstance(node, javalang.tree.BlockStatement):
    unsupportedAttributes = ["label"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return '\n'.join([nodeToCodeLine(b) for b in node.statements])
  elif isinstance(node, javalang.tree.ClassCreator):
    unsupportedAttributes = ["constructor_type_arguments", "postfix_operators", "prefix_operators","selectors"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    if isBlank(getattr(node,"arguments")) and isBlank(getattr(node,"body")):
      return 'new {0}()'.format(prependQualifierIfProvided(nodeToCodeLine(node.type), node.qualifier))
    elif isBlank(getattr(node,"body")):
      argList = ','.join([nodeToCodeLine(a) for a in node.arguments])
      return 'new {0}({1})'.format(prependQualifierIfProvided(nodeToCodeLine(node.type), node.qualifier), argList)
    elif isBlank(getattr(node, "arguments")):
      return 'new {0}(){{\n {1}\n}}'.format(prependQualifierIfProvided(nodeToCodeLine(node.type), node.qualifier), nodeToCodeLine(node.body))
    else: 
      argList = ','.join([nodeToCodeLine(a) for a in node.arguments])
      return 'new {0}({1}){{\n {2}\n}}'.format(prependQualifierIfProvided(nodeToCodeLine(node.type), node.qualifier), argList, nodeToCodeLine(node.body))
  elif isinstance(node, javalang.tree.Cast):
    return '({0}) {1}'.format(nodeToCodeLine(node.type), nodeToCodeLine(node.expression))
  elif isinstance(node, javalang.tree.ReferenceType):
    unsupportedAttributes = ["arguments", "dimensions"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    if isBlank(getattr(node, "sub_type")):
      return node.name
    else:
      return '{0}.{1}'.format(node.name, nodeToCodeLine(node.sub_type))
  elif isinstance(node, javalang.tree.This):
    unsupportedAttributes = ["postfix_operators", "prefix_operators"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    selectorString = ''
    if not isBlank(getattr(node, "selectors")):
      for s in node.selectors:
        '{0}.{1}'.format(selectorString, nodeToCodeLine(s))
    if isBlank(getattr(node, "qualifier")):
      return 'this{0}'.format(selectorString)
    else:
      return '{0}.this{1}'.format(node.qualifier, selectorString)
  elif isinstance(node, javalang.tree.BinaryOperation):
    return "{0}{1}{2}".format(nodeToCodeLine(node.operandl),node.operator, nodeToCodeLine(node.operandr))
  elif isinstance(node, list):
    resultString = ''
    for i in node:
      resultString = '{0}{1}\n'.format(resultString, nodeToCodeLine(i))
    return resultString
  elif isinstance(node, javalang.tree.MethodDeclaration):
    unsupportedAttributes = ["documentation", "throws", "type_parameters"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    resultString = ''
    if not isBlank(getattr(node, "annotations")):
      resultString = '{0}\n'.format(nodeToCodeLine(node.annotations))
    modifiersString = ''
    for modifierCount, m in enumerate(node.modifiers):
      if modifierCount == 0:
        modifiersString = m
      else:
        modifiersString = '{0} {1}'.format(modifiersString, m)
    paramerString = ''
    for parameterCount, p in enumerate(node.parameters):
      if parameterCount == 0:
        parameterString = nodeToCodeLine(p)
      else:
        parameterString = '{0}, {1}'.format(parameterString, p)
    if isBlank(getattr(node, "return_type")):
      resultString = '{0} {1} void {2}({3}){{\n'.format(resultString, modifiersString, node.name, parameterString)
    else:
      resultString = '{0} {1} {2} {3}({4}){{\n'.format(resultString, modifiersString, nodeToCodeLine(node.return_type), node.name, parameterString)
    resultString = '{0} {1}\n}}\n'.format(resultString, nodeToCodeLine(node.body))
    return resultString
  elif isinstance(node, javalang.tree.Annotation):
    unsupportedAttributes = ["element"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return node.name
  elif isinstance(node, javalang.tree.FormalParameter):
    unsupportedAttributes = ["annotations", "modifiers"]
    if node.varargs:
      print('error: unhandled varargs in FormalParmaters\nNeed to fix when I see an example')
      print('node: {0}'.format(node))
      traceback.print_stack() 
      sys.exit(1)
    else:
      return '{0} {1}'.format(nodeToCodeLine(node.type), node.name) 
  elif isinstance(node, javalang.tree.ClassReference):
    unsupportedAttributes = ["postfix_operators", "prefix_operators", "qualifier","selectors"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return '{0}.class'.format(nodeToCodeLine(node.type))
  elif isinstance(node, javalang.tree.BasicType):
    unsupportedAttributes = ["dimensions"]
    testAttributesNotHandledAreBlank(node, unsupportedAttributes)
    return str(node.name)
  else:
    print('error: unsupported node type: {0}'.format(type(node)))
    print('node: {0}'.format(node))
    traceback.print_stack() 
    sys.exit(1)



def getLinesFromTree(fileTree, lineIndexList):
  lineList = []
  node = fileTree.types[0].body[0]
  statementNodes = [ node for path,node in fileTree if isStatementOfInterest(node)]
  for statementNumber, s in enumerate(statementNodes): 
    if statementNumber in lineIndexList:
      stringOfNode = nodeToCodeLine(s)
      if stringOfNode.strip() == "":
        print('error: line is blank')
        sys.exit(1)
      if not stringOfNode[-1] == ';':
        stringOfNode = '{0};'.format(stringOfNode)
      lineList.append(stringOfNode)
  return lineList






def isStatementOfInterest(nodeToTest):
  if isinstance(nodeToTest, javalang.tree.MethodInvocation) or \
     isinstance(nodeToTest, javalang.tree.SuperMethodInvocation) or \
     isinstance(nodeToTest, javalang.tree.Assignment):
     return True
  # if isinstance(nodeToTest, javalang.tree.StatementExpression) or \
  #   isinstance(nodeToTest, javalang.tree.SuperMethodInvocation):
  #   if isinstance(nodeToTest.expression, javalang.tree.Cast):
  #     expressionToTest = nodeToTest.expression.expression
  #   else: 
  #     expressionToTest = nodeToTest.expression
  #   if isinstance(expressionToTest, javalang.tree.MethodInvocation) or \
  #   isinstance(expressionToTest, javalang.tree.SuperMethodInvocation) or \
  #   isinstance(expressionToTest, javalang.tree.Assignment):
  #     return True
  #   else:
  #     print('error node type unsupported')
  #     print("{0}: {1}".format(type(nodeToTest.expression), nodeToTest.expression))
  #     print("is a statement type: {0}".format(isinstance(nodeToTest, javalang.tree.StatementExpression)))
  #     sys.exit(1)
  elif isinstance(nodeToTest, javalang.tree.CompilationUnit) or \
    isinstance(nodeToTest, javalang.tree.ClassDeclaration) or \
    isinstance(nodeToTest, javalang.tree.MethodDeclaration) or \
    isinstance(nodeToTest, javalang.tree.FormalParameter) or \
    isinstance(nodeToTest, javalang.tree.ReferenceType) or \
    isinstance(nodeToTest, javalang.tree.StatementExpression) or \
    isinstance(nodeToTest, javalang.tree.MemberReference) or \
    isinstance(nodeToTest, javalang.tree.Cast) or \
    isinstance(nodeToTest, javalang.tree.Annotation) or \
    isinstance(nodeToTest, javalang.tree.Literal) or \
    isinstance(nodeToTest, javalang.tree.BinaryOperation) or \
    isinstance(nodeToTest, javalang.tree.LocalVariableDeclaration) or \
    isinstance(nodeToTest, javalang.tree.VariableDeclarator) or \
    isinstance(nodeToTest, javalang.tree.IfStatement) or \
    isinstance(nodeToTest, javalang.tree.BlockStatement) or \
    isinstance(nodeToTest, javalang.tree.ClassCreator) or \
    isinstance(nodeToTest, javalang.tree.This) or \
    isinstance(nodeToTest, javalang.tree.ClassReference) or \
    isinstance(nodeToTest, javalang.tree.ReturnStatement)or \
    isinstance(nodeToTest, javalang.tree.BasicType) or \
    isinstance(nodeToTest, javalang.tree.SuperMemberReference) or \
    isinstance(nodeToTest, javalang.tree.ForStatement) or \
    isinstance(nodeToTest, javalang.tree.ForControl) or \
    isinstance(nodeToTest, javalang.tree.VariableDeclaration) or \
    isinstance(nodeToTest, javalang.tree.TryStatement) or \
    isinstance(nodeToTest, javalang.tree.CatchClause) or \
    isinstance(nodeToTest, javalang.tree.TernaryExpression) or \
    isinstance(nodeToTest, javalang.tree.ArrayCreator) or \
    isinstance(nodeToTest, javalang.tree.TypeArgument) or \
    isinstance(nodeToTest, javalang.tree.ArrayInitializer) or \
    isinstance(nodeToTest, javalang.tree.ThrowStatement) or \
    isinstance(nodeToTest, javalang.tree.CatchClauseParameter) or \
    isinstance(nodeToTest, javalang.tree.LambdaExpression):
    return False
  else:
    print('unsupported expression: {0}'.format(nodeToTest))
    print('type of expression: {0}'.format(type(nodeToTest)))
    traceback.print_stack() 
    sys.exit(1)
    return False

def cleanFileLinesBeforeParsing(fileToEdit):
  linesInFile = []
  openParensCount = 0
  tempLine = ""
  with open(fileToEdit,'r') as fin:
    print('original contents:')
    for line in fin:
      print(line, end="")
      for c in line:
        if c == ';':
          openParensCount = 0
          break
        elif c == '(':
          openParensCount += 1
        elif c == ')':
          openParensCount -= 1
      if openParensCount > 0:
        tempLine = tempLine + line.rstrip()
      else:
        openParensCount = 0
        if tempLine != "":
          line = line.lstrip()
          line = tempLine + line
          tempLine = ""
        linesInFile.append(line)
  with open(fileToEdit,'w') as fout:
    for line in linesInFile:
      print(line, file=fout, end = "")



#later change this to take a parameter or argument; but hard coding for initial testing
#TODO: clean up this method, it's getting too big and has too many subfunctions
#to be easily readable
def getParseInfo(fileToRead):
  cleanFileLinesBeforeParsing(fileToRead)
  #I can't remember if these variables persist after the method exits if I return
  #them. Try it and see
  variableTypeDict = {}
  variableDependencyChains = {}
  with open(fileToRead,'r') as fileFin:
    fileInput = fileFin.read()
    filePath = os.getcwd()+os.sep + fileToRead
    print('reading file: {0}'.format(filePath))
    print(fileInput)
    print('')
    firstLineIndex = 0
    fileInputLines = fileInput.splitlines()
    while(fileInputLines[firstLineIndex].strip() == ''):
      firstLineIndex = firstLineIndex+1
      if firstLineIndex > len(fileInputLines) - 1:
        break
    if not 'class' in fileInput[firstLineIndex]:
      fileInput = 'class Test{{\n {0}\n}}'.format(fileInput)
    try:
      fileTree = javalang.parse.parse(fileInput)
    except javalang.parser.JavaSyntaxError as j:
      print('syntax error: {0}'.format(j))
      print(fileInput)
      print('error: unable to parse {0}'.format(fileToRead))
      input('stopping here to check unparsable file')
      sys.exit(1)
    #nodeToLineNumberList = createNodeToLineNumberList(fileInput, fileTree)
    # debating on if I should put a break after the 
    #for path, node in testTree:
    #  print("{0}".format(testTree.types[0].body))
    #  print("")
    #  print("")
    #  time.sleep(1)
    #  if isinstance(node, javalang.tree.MethodDeclaration):
    #node should always be the method of interest, since the current assumption is
    #that these classes will consist of only the method I am interested in evaluating;
    #will need to change later if that assumption changes
    node = fileTree.types[0].body[0]
    for p in node.parameters:
      varName = p.name
      if varName in variableTypeDict:
        print("error {0} already in {1}".format(varName, variableTypeDict))
        sys.exit(1)
      else:
        variableTypeDict[varName] = p.type.name
    #print(variableTypeDict)
    def extractArgType(arg):
      #print(arg)
      #print(arg.member)
      #print("")
      #print(varName)
      varName = getFullNameOfArg(arg)
      return getTypeOfVar(variableTypeDict, varName)
    foundColorArgs = False
    #collect all variable declarations in the node
    for path, n in node:
      #use 1 as the starting index instead of 0 as the starting index
      #print(nodeToCodeLine(s))
      if isinstance(n, javalang.tree.LocalVariableDeclaration): 
        for d in n.declarators:
          if d.name == 'colorArgs':
            foundColorArgs = True
          if d.name in variableTypeDict:
            print("error {0} already in {1}".format(varName, variableTypeDict))
            sys.exit(1)
          else:
            variableTypeDict[d.name] = n.type.name
      #I'm starting to think I've stopped using the code in this elif branch. 
      #I'm going to try comment it out and see what happens 
      #elif isinstance(s, javalang.tree.StatementExpression):
        #if isinstance(s.expression, javalang.tree.SuperMethodInvocation):
          #handle super call
          #methodName = s.expression.member
          #methodParamTypes = map(extractArgType, s.expression.arguments)
          ##print('method name: {0}'.format(methodName))
          #print('method param types: {0}'.format(list(methodParamTypes)))
          #print('statement number: {0}'.format(statementNumber))
        #elif isinstance(s.expression, javalang.tree.MethodInvocation):
          #handle basic method invocation
          #if isinstance(s.expression.value, javalang.tree.Cast)
            #methodExpr = s.expression.value.expression
          #else:
            #methodExpr = s.epression.value
          #methodName = methodExpr.member
          #methodParamTypes = map(extractArgType, s.expression.arguments)
          #print('method name: {0}'.format(methodName))
          #print('method param types: {0}'.format(list(methodParamTypes)))
          #print('statement number: {0}'.format(statementNumber))
        #elif isinstannce(s.expression, javalang.tree.AssignmentExpression):

        #else:
      #  if not (isinstance(s, javalang.tree.StatementExpression) \
      #    or isinstance(s, javalang.tree.SuperMethodInvocation)  \
      #    or isinstance(s, javalang.tree.AssignmentExpression)):
      #    print("error: did not handle {0}".format(s.expression))
      #    sys.exit(1)
      #else: 
      #  print("error: didn't process {0}".format(s))
      #  sys.exit(1)
    #iterate though again to build the sequence chain for each variable 
    #collecting the variables in the first pass
    #print('variable dict at start of chain building: {0}'.format(variableTypeDict))
    for var in variableTypeDict:
      variableDependencyChains[getTypeOfVar(variableTypeDict, var)] = []

    
    #statementNodes = [ s for s in node.body if isStatementOfInterest(s)]
    statementNodes = [ node for path,node in fileTree if isStatementOfInterest(node)]
    #print('statement nodes:\n') 
    for statementNumber, s in enumerate(statementNodes): 
      if s == None:
        print('error: s should not be None')
        sys.exit(1)
      def processMethodCall(variableDependencyChains, statementNumber, methodCall):
        print('in process method call')
        if not (methodCall.qualifier == None or methodCall.qualifier == "" or methodCall.qualifier == "super"):
          print('in first if of process method call')
          if methodCall.qualifier[0].islower():
            typeOfQ = getTypeOfVar(variableTypeDict, methodCall.qualifier)
            if not typeOfQ == None:
              variableDependencyChains[typeOfQ].append(statementNumber)
        #methodParams = [ getFullNameOfArg(a) for a in methodCall.arguments if (not isinstance(a, javalang.tree.Literal)) ]  
        try: 
          methodParams = [ getFullNameOfArg(a) for a in methodCall.arguments ]  
        except AttributeError:
          print('error: method call does not have arguments')
          print('method call: {0}'.format(methodCall))
          traceback.print_stack() 
          sys.exit(1)
        methodParams = [ m for m in methodParams if not m==None ]
        #methodParams = map(getFullNameOfArg, s.expression.arguments)
        for p in methodParams:
          #can't remember everything this check was blocking, but it blocks the static
          #files, which I currently don't want
          #if p[0].islower():
          print('param: {0}'.format(p))
          typeOfP = getTypeOfVar(variableTypeDict, p) 
          if typeOfP == None:
            #if the variable is a global variable, then don't worry about it, since
            #global variables are not supported at the moment.
            #Currently using the heuristic that variables that start and stop 
            #with quotes or numbers are not global variables
            #
            #Currently thinking that I don't care about constants declared in the code;
            #may change my mind later
            continue
           # if p[0] == "\"" and p[-1] == "\"" or p[0].isdigit() and p[-1].isdigit():
              #I'm pretty sure all method params should have types other
              #than global variables, so I'd have 
              #to look into why this situation fails
           #   print('error: type of {0} is None'.format(p))
           #   print('file contents:\n {0}'.format(fileInput))
           #   print('variable of interest: {0}'.format(p))
           #   print('variable type dict: {0}'.format(variableTypeDict))
           #   print('method call: {0}'.format(methodCall))
           #   print(fileTree)
           #   sys.exit(1)
          if typeOfP == "StaticFile":
            #print('{0} is a static file'.format(p))
            #sys.exit(1)
            #add static variables to the variable dict so they are replaced later,
            #but don't add them earlier so they are not included in the variable dependency
            #chain - currently I don't think it matter if the static file calls are different
            variableTypeDict[p] = "StaticFile"
          else:
            if typeOfP in variableDependencyChains:
              variableDependencyChains[typeOfP].append(statementNumber)
            else:
              #this else should only execute for the first occurrence of a Literal
              #all other types should already be added
              if typeOfP == 'true' or typeOfP == 'false':
                if typeOfP in variableDependencyChains:
                  variableDependencyChains[typeOfP].append([statementNumber])
                else:
                  variableDependencyChains[typeOfP] = [statementNumber]
              else:
                #skipping global variables
                if typeOfP is not None:
                  print('error: type {0} not found in dependency chain dict for variable {1}'.format(typeOfP, p))
                  #print('is type of bool: {0}'.format(isinstance(p, bool)))
                  print('python type of true or false: {0}'.format(type(p)))
                  print('dependency chain dict: {0}'.format(variableDependencyChains))
                  sys.exit(1)
        return variableDependencyChains

      #we only care about statement expressions this time (when considering
      #only statementexpressions and variabledeclarations) - although may 
      #expand to handle more later
      if isinstance(s, javalang.tree.Assignment) and not isinstance(s.expressionl, javalang.tree.This):
        print('past is instance')
        try:
          typeQ = getTypeOfVar(variableTypeDict, s.expressionl.member)
        except Exception as e:
          print(s.expressionl)
          print(type(s.expressionl))
          print(e)
          sys.exit(1)
        if typeQ:
          variableDependencyChains[typeQ].append(statementNumber)
        if isinstance(s.value, javalang.tree.Cast):
          methodCall = s.value.expression
        else:
          methodCall = s.value
        #make sure method call is an actual method call and ignore all others
        if not isinstance(methodCall, javalang.tree.MemberReference) and \
        not isinstance(methodCall, javalang.tree.Literal) and \
        not isinstance(methodCall, javalang.tree.TernaryExpression) and \
        not isinstance(methodCall, javalang.tree.This):
        #print(methodCall)
        #print('chain before: {0}'.format(variableDependencyChains))
          variableDependencyChains = processMethodCall(variableDependencyChains, statementNumber, methodCall)
        #print('chain after: {0}'.format(variableDependencyChains))
      elif hasattr(s, 'expressionl') and not isinstance(s.expressionl, javalang.tree.This): 
        print('in second elif')
        #print(s)
        #print('chain before: {0}'.format(variableDependencyChains))
        variableDependencyChains = processMethodCall(variableDependencyChains, statementNumber, s)
        #print('chain after: {0}'.format(variableDependencyChains))
      elif isinstance(s, javalang.tree.MethodInvocation):
        variableDependencyChains = processMethodCall(variableDependencyChains, statementNumber, s)
    #print('final dependency chains: {0}'.format(variableDependencyChains))
    for typeName in variableDependencyChains:
      if len(variableDependencyChains[typeName]) < 1:
        #print('possible error: this code violates the assumption that all locally declared types are used')
        #print('filename: {0}'.format(fileToRead))
        #print('original code:\n{0}'.format(fileInput))
        with open(errorFile, 'a') as errorFout:
          errorFout.write('possible error: this code violates the assumption that all locally declared types are used\n')
          errorFout.write('filename: {0}'.format(fileToRead))
          errorFout.write('\n')
          errorFout.write('original code:\n{0}'.format(fileInput))
          errorFout.write('\n')

        #sys.exit(1)
    #print(variableDependencyChains)
    #print(variableTypeDict)
    return (variableDependencyChains, variableTypeDict, fileTree)

def getTypesInStatementNumber(statementNumber, typeName, dependencyChains):
  typeList = [typeName]
  for otherTypeName in dependencyChains.keys():
    #print('otherTypeName {0} typeName {1} = {2}'.format(otherTypeName,typeName, otherTypeName == typeName))
    if not otherTypeName == typeName:
      for otherStatementNumber in dependencyChains[otherTypeName]:
        if otherStatementNumber == statementNumber:
          typeList.append(otherTypeName)
  return typeList
            
#returns list of tuples which contain first the type name then the list number 
#(1 or 2) and the statement number in that list which did not have a match
#Currently, this method pays attention to line ordering

#Note: this will return multiple entries for the same line - if you are looking
#for unique lines, you will need to filter by line later
def checkIfEveryCallHasTheExpectedTypesWithIt(chain1, chain2, listNumber):
  resultList = []
  #print('in check if expected types')
  for typeName in chain1.keys():
    #print("in first for")
    #print("end of chain1")
    previousStatementNumberInChain2Lines = -1
    for statementNumber in chain1[typeName]:
      #print("in second for")
      typesToLookFor = getTypesInStatementNumber(statementNumber, typeName, chain1)
      #print("placeholder: {0}".format(typesToLookFor))
      foundMatch = False
      if typeName in chain2: 
        for chain2StatementNumber in chain2[typeName]:
          #print('in third for')
          if chain2StatementNumber > previousStatementNumberInChain2Lines:
            chain2Types = getTypesInStatementNumber(chain2StatementNumber, typeName, chain2) 
            #print(chain2Types)
            #if statementNumber == 1:
            if typesToLookFor == chain2Types:
              previousStatementNumberInChain2Lines = chain2StatementNumber
              foundMatch = True
              break

      if not foundMatch:
        resultList.append((typeName, listNumber, statementNumber))
  #get the total number of statements for sanity check
  #skipping this case for now
  #statementSet = set()
  #for typeName in chain1.keys():
  #  for statementNumber in chain1[typeName]:
  #    statementSet.add(statementNumber)
  #totalStatementCount = len(statementSet)
  #if (listNumber == 1 and totalStatementCount > 1 and totalStatementCount - len(resultList) < 2):
  #  print('possible error: too many lines to delete')
  #  print(chain1)
  #  print('\n')
  #  print(chain2)
  #  print(resultList)
  #  sys.exit(1)
  return resultList

def checkUnmatchedTypesForBothLists(list1, list2):
  result = checkIfEveryCallHasTheExpectedTypesWithIt(list1, list2, 1) + checkIfEveryCallHasTheExpectedTypesWithIt(list2, list1, 2)
  return result


#how should I handle ordering of methods? sometimes the order matters and other
#times it doesn't
#currently the method is implemented as if ordering doesn't matter
#returns lineNumbers that zero indexed
def checkMethodCallsInLines(fileTree1, fileTree2):
  #for path, node in fileTree1:
  def getMethodListFromTree(fileTree):
    node = fileTree.types[0].body[0]
    methodList = []
    for statementNumber, s in enumerate(node.body):
      if isinstance(s, javalang.tree.StatementExpression):
       if isinstance(s.expression, javalang.tree.MethodInvocation) or \
       isinstance(s.expression, javalang.tree.SuperMethodInvocation):
         methodList.append((s.expression.member, statementNumber))
    return methodList
  def methodInTupleList(listOfMethodTuples, methodToCheck):
    for i in listOfMethodTuples:
      if i[0] == methodToCheck:
        return True
    return False
  # returns a list of method name, list number, line number of unique methods
  def getUniqueItemsInLists(list1, list2):
    uniqueList = []
    for i in list1:
      if not methodInTupleList(list2, i[0]):
        uniqueList.append((i[0],1, i[1]))
    for i in list2:
      if not methodInTupleList(list1, i[0]):
        uniqueList.append((i[0],2, i[1]))
    return uniqueList

  methodList1 = getMethodListFromTree(fileTree1)
  methodList2 = getMethodListFromTree(fileTree2)
  return getUniqueItemsInLists(methodList1, methodList2)

#return the possible range of indexes to put the type statement. 
#If the statement could start on any index before a certain value, the start 
#index returned will be 0 (since placing the line in a negative line number
#of the method doesn't make sense). If the ending index can be anything after a
#value, the returned ending index will be None to indicate maximum length of the 
#method.      

#This method assumes you are trying to find the location you can add the 
#typeMismatch from chain2 to chain 1

#TODO: check if you are assuming only one mismatch in a row
def findPossibleRangeOfTypeDifference(chain1, chain2, typeMismatch):
  if typeMismatch[1] == 1:
    print('currently not supported to find where an extra statement in the first list can be added to the first list')
    sys.exit(1)
    #chainOfInterest = chain1
  else:
    chainOfInterest = chain2
  # not sure this is right - will write it down and then think through it more
  #if indexOfMismatch == 0:
  #  startIndex = 0
  #initialize the start and end index to the whole method
  startIndex = -1
  endIndex = None
  #This is similar to the section of code above but the chain types are switched
  #may want to refactor into one method later
  typesToCheck = getTypesInStatementNumber(typeMismatch[2], typeMismatch[0], chain2) 
  for typeName in typesToCheck:
    startIndexForType = 0
    endIndexForType = None
    previousStatementNumberInChain1Lines = -1 
    indexOfMismatch = chainOfInterest[typeName].index(typeMismatch[2])
    for indexNumber, statementNumber in enumerate(chainOfInterest[typeName]):
      #not worth checking the indexOfMismatch because I know a match will not be found
      #need to iterate through the rest to find the matches sequentially (haven't 
      #implemented a better way)

      if not statementNumber == indexOfMismatch:
        typesToLookFor = getTypesInStatementNumber(statementNumber, typeName, chainOfInterest)
        foundMatch = False
        for chain1StatementNumber in chain1[typeName]:
          if chain1StatementNumber > previousStatementNumberInChain1Lines:
            chain1Types = getTypesInStatementNumber(chain1StatementNumber, typeName, chain2) 
            #if statementNumber == 1:
            if typesToLookFor == chain1Types:
              previousStatementNumberInChain1Lines = chain1StatementNumber
              foundMatch = True
              break
        if indexNumber < indexOfMismatch:
          #It would be more readable for previousStatement..Lines to be chain1StatementNumber
          #but I don't think that is in scope. I'll try it first
          #startIndexForType = previousStatementNumberInChain1Lines 
          startIndexForType = chain1StatementNumber 
        if indexNumber > indexOfMismatch:
          #endIndexForType = previousStatementNumberInChain1Lines 
          endIndexForType = chain1StatementNumber
          break
    if startIndexForType > startIndex:
      startIndex = startIndexForType
    #currently startIndex is the previous line number that was found with the type
    #now convert it to the first line that the new type statement can be added to
    startIndex = startIndex + 1
    if (not endIndexForType == None) and ((endIndex == None) or (endIndexForType < endIndex)):
      endIndex = endIndexForType
  return (startIndex, endIndex)

    
def main():
  #originalFile='/Users/zack/git/DirectiveTool/original_onCreateOptionsMenu.txt' 
  #downloadedFile='/Users/zack/git/DirectiveTool/downloaded_onCreateOptionsMenu.txt' 
  originalFile='/Users/zack/git/DirectiveTool/original_onCreate.txt' 
  downloadedFile='/Users/zack/git/DirectiveTool/downloaded_onCreate.txt' 
  (originalDependencyChains, originalVariableTypeDict, originalFileTree) =  \
    getParseInfo(originalFile)
  (downloadedDependencyChains, downloadedVariableTypeDict, downloadedFileTree) = \
    getParseInfo(downloadedFile)
  typeMismatches = checkUnmatchedTypesForBothLists(originalDependencyChains, downloadedDependencyChains)
  methodCallMismatches = checkMethodCallsInLines(originalFileTree, downloadedFileTree)
  #If type mismatches occur in list 1, (assuming the original list is list 1) then 
  #those lines can be deleted). If the type mismatch occurs in list 2, I have to figure
  #out the possible range in list 1 that the type can be added
  #since type mismatches were based on ordering, now I need to figure out the range the statement 
  #can be added
  #
  #changing the results a bit so I can test the implementation of this method, 
  #will remove the result changes later
  #typeMismatches = [(typeMismatches[0][0], 2, typeMismatches[0][2])]
  for typeMismatch in typeMismatches:
    #findPossibleRangeOfTypeDifference(originalDependencyChains, downloadedDependencyChains, typeMismatch)
    #switching the chain ordering to test on the example I have. 
    #Will use the call ordering above when I finish testing
    (startIndex, endIndex) = findPossibleRangeOfTypeDifference(downloadedDependencyChains, originalDependencyChains, typeMismatch)

if __name__ == "__main__":
  main()


#testFile = '/Users/zack/git/DirectiveTool/testFile.txt'


