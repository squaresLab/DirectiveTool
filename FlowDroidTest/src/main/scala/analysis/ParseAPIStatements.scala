package analysis

import analysis.AnalyzeExclusiveCallsOnAVariableType
import analysis.DetectIncorrectGetActivityMain.{createCallChainsDepthFirst, getStartingMethodAndCallChain}
import soot.toolkits.graph.ExceptionalUnitGraph
import soot.{SootClass, SootMethod}

import scala.collection.JavaConverters._
import scala.collection.mutable
import scala.collection.mutable.ListBuffer
import util.control.Breaks._

object ParseAPIStatements {

  def main(args: Array[String]): Unit = {
    //TODO: figure out how to make this code work with spaces in the statement or without

    //Done:
    //val statementToParse: String =  "checkSubclassOf(\"Activity\").methodToCheck(\"onCreate\").firstMustOccurBeforeSecond(\"setContentView\", \"findViewById\")"
    //val statementToParse: String = "checkSubclassOf(\"AsyncTask\").checkClassesWithOuterClassThatSubclassOf(\"Fragment\").absent(\"getResources\")"
    //val statementToParse: String = "instanceOf(\"Intent\").exclusiveOrInstance(\"setPackage\", \"setSelector\")"
    //val statementToParse: String  = "checkSubclassOf(\"Activity\").methodToCheck(\"onCreate\").firstCannotFollowSecond(\"setContentView\", \"setTheme\"))"
    //val statementToParse: String = "checkSubclassOf(\"Fragment\").not(checkSubclassOf(\"DialogFragment\")).methodToCheck(\"onCreateView\").contains(\"inflate(*,*,false)\")"
    //val statementToParse: String = "checkSubclassOf(\"Fragment\").if(contains(\"onCreateOptionsMenu\")) then (methodToCheck(\"onCreate\").contains(\"setHasOptionsMenu(true)\")"
    val statementToParse: String = "checkSubclassOf(\"Fragment\").in(\"getActivity\", \"activityAttachedState\"))"

    //Not done:
    //maybe change and to multipleCheckCountFirst
    //val statementToParse: String  = "and(and(methodToCheck(\"onClick\").contains(\"setArguments\"), and (methodToCheck(\"onTabSelected\").contains(\"add\")), methodToCheck(\"onTabUnselected\").contains(\"hide\")))"

    val setHasOptionsMenuErrorTemplate = "@@@@@ Found a problem: setHasOptionsMenu(true) must be called in the onCreate method to display the OptionsMenu in %s"
    //notes: requireCallOrder - both are not required but the first one must come before the second one -> error if the second
    //one occurs without the first. Might want to change name to firstMustBeBeforeSecond.
    //I also don't know if not in the specification language makes sense; you can't invert and int return
    //val statementToParse: String = "checkSubclassOf(\"Fragment\").or(if(methodToCheck(\"onCreate\").contains(\"setHasOptionsMenu(true);\")) then defined(\"onCreateOptionsMenu\"), if (checkSubClass(Fragment), defined(“onCreateOptionsMenu”))) then (methodToCheck(“onCreate”).contains(“setHasOptionsMenu(true))"


    //new statements to test
    //for the statement below, need to add something about the first parameter being the same and null doesn't count
    //val statementToParse: String = "if(methodToCheck(\"onResume\").contains(\"Context.registerReceiver\").firstParameterMustMatch() then (methodToCheck(\"onPause\").contains(\"Context.unregisterReceiver\").firstParameterMustMatch())"

    val methodShorthandToFullDeclaration: Map[String, String] = Map("getResources" -> "android.content.res.Resources getResources()")

    //I'm not sure the right way to do this, but I'll guess for my current case and then adjust this when I
    //get more examples - I'm not sure how much of the check to pull out here and make variable vs hardcoding the rest
    //this variable contains the state checking methods for each checker that needs a state check
    //(used with the in keyword))
    val getActivityAttachedCheck = (call:ControlFlowItem) => {FragmentLifecyleMethods.isMethodWhenFragmentInitialized(call.methodCall)}
    val stateChecks: Map[String, ControlFlowItem => Boolean] = Map("activityAttachedState" -> getActivityAttachedCheck)

    def getPositionOfEndingParenthesisInNestedString(stringToCheck: String): Option[Int] = {
      var modifierEndLoc: Option[Int] = None
      var indexLoc = 0
      breakable {
        for (c <- stringToCheck) {
          var nestingCount = 0
          if (c == '(') {
            nestingCount += 1
          }
          else if (c == ')') {
            if (nestingCount < 2) {
              modifierEndLoc = Some(indexLoc)
              break
            } else {
              nestingCount -= 1
            }
          }
          indexLoc += 1
        }
      }
      return modifierEndLoc
    }

    /* I am writing this quickly, might want to refactor later
     */
    def parseStatement(parsingObj: ParseCodeObj): ParseCodeObj = {
      parsingObj.stringToParse = parsingObj.stringToParse.trim()

      //might want to refactor this, but only keep track of previous class if it's for the
      //in keyword
      //Currently, classForStateCheck isn't used, but I could see it being useful, so I'll
      //leave it
      if(!parsingObj.stringToParse.startsWith("in(")){
        parsingObj.classForStateCheck = None
      }

      //TODO: change and to the new meaning
      if (parsingObj.stringToParse.startsWith("and(")) {
        //save but don't parse it yet, we need to read from the end to the front
        val firstPartOfAnd = parsingObj.stringToParse.substring("and(".length(), parsingObj.stringToParse.indexOf(','))
        //I'm not confident this works on more complex statements; check and see later
        val middleOfStmt = parsingObj.stringToParse.substring(parsingObj.stringToParse.indexOf(','))
        if (!middleOfStmt.startsWith(",")) {
          throw new RuntimeException("missing comma in and statement")
        }
        val secondPartOfStmt = middleOfStmt.substring(1)
        parsingObj.stringToParse = secondPartOfStmt
        val partiallyUpdatedParsingObj = parseStatement(parsingObj)
        //I'm not sure if this next check is really helping and it currently messes up when
        //the code has nested ands
        /*println(s"partially updated string: ${partiallyUpdatedParsingObj.stringToParse}")
        if (!partiallyUpdatedParsingObj.stringToParse.startsWith(")")) {
          throw new RuntimeException(s"missing end of and statement: |${partiallyUpdatedParsingObj.stringToParse}|")
        }*/
        //need to add a meaning to the and statement
        //updatedParsingObj.stringToParse = updatedParsingObj.stringToParse.substring(1)
        partiallyUpdatedParsingObj.stringToParse = firstPartOfAnd
        val updatedParsingObj = parseStatement(partiallyUpdatedParsingObj)
        return updatedParsingObj
      }
      else if (parsingObj.stringToParse.startsWith("or(")) {
        parsingObj.stringToParse = parsingObj.stringToParse.substring("or(".length())
        val firstPartOfOr = parseStatement(parsingObj)
        if (!firstPartOfOr.stringToParse.startsWith(",")) {
          throw new RuntimeException("first part of or did not parse to the correct point")
        }
        //creating a new parsing obj for the second part of the or
        firstPartOfOr.stringToParse = firstPartOfOr.stringToParse.substring(1)
        val startOfSecondParsingObj = new ParseCodeObj(firstPartOfOr.stringToParse, None)
        val secondParsingResult = parseStatement(startOfSecondParsingObj)
        //TODO: figure out how to combine the two code results
        return secondParsingResult
      }
      /*      else if (parsingObj.stringToParse.startsWith("if(")){

            }

       */
      else if (parsingObj.stringToParse.startsWith("contains(")) {
        val modifierEndLoc = getPositionOfEndingParenthesisInNestedString(parsingObj.stringToParse).get
        var methodToCheckFor = parsingObj.stringToParse.substring("contains(".length() + 1, modifierEndLoc)
        methodToCheckFor = methodToCheckFor.replaceAll("\"","")
        var methodName = methodToCheckFor
        if (methodToCheckFor.contains('(')) {
          val methodItems = methodToCheckFor.substring(0, methodToCheckFor.length).split('(')
          methodName = methodItems(0)
          val paramList = methodItems(1).split(',')
        }

        //eventually I need to add handling of the paramList
        def checkContainsWrapper(methodToCheckForString: String): (SootClass) => Int = {
          def checkContains(cl: SootClass): Int = {
            //maybe figure out a way to extract the error messages from these functions
            var problemCount = 0
            for (m: SootMethod <- cl.getMethods().asScala) {
              if (!m.hasActiveBody) {
                m.retrieveActiveBody()
              }
              if (m.isConcrete && m.hasActiveBody) {
                if (m.getName == methodToCheckForString) {
                  problemCount += 1
                }
              }
            }
            return problemCount
          }
          return checkContains
        }
        parsingObj.stringToParse = parsingObj.stringToParse.substring(modifierEndLoc + 1)
        parsingObj.codeResult = Some(checkContainsWrapper(methodToCheckFor))
        parsingObj.checkEndOfContexts()
        return parsingObj
      }
      else if (parsingObj.stringToParse.startsWith("checkSubclassOf(")) {
        val endString = "\")"
        var endLoc = parsingObj.stringToParse.indexOf(endString)
        val classOfInterest = parsingObj.stringToParse.substring("checkSubclassOf(".length() + 1, endLoc)
        parsingObj.classForStateCheck = Some(classOfInterest)
        println(parsingObj.stringToParse(endLoc + endString.length))
        if (parsingObj.stringToParse(endLoc + endString.length) == '.') {
          endLoc += 1
        }
        parsingObj.stringToParse = parsingObj.stringToParse.substring(endLoc + endString.length)
        println(s"string to parse after checkSubclassOf: ${parsingObj.stringToParse}")
        val wasInNot = parsingObj.inNot
        parsingObj.checkEndOfContexts()
        val updatedParsingObj = parseStatement(parsingObj)
        //you might want to remove the check below if it is followed by an in

        //parsingObj.addToCodeResult(s"if(DetectionUtils.classIsSubClass(cl,$classOfInterest)){\n", "}\n")
        def classFilterWrapper(innerFunc: SootClass => Int, filterClass: String, excludeSubclass: Boolean = false): SootClass => Int = {
          def classFilter(cl: SootClass): Int = {
            var caughtProblems = 0
            if (excludeSubclass) {
              //not sure if there is an easier way to negate the check in scala
              if (!DetectionUtils.classIsSubClass(cl, filterClass)) {
                caughtProblems = innerFunc(cl) + caughtProblems
              }
            }
            else {
              if (DetectionUtils.classIsSubClass(cl, filterClass)) {
                caughtProblems = innerFunc(cl) + caughtProblems
              }
            }
            return caughtProblems
          }

          return classFilter
        }

        updatedParsingObj.codeResult = Some(classFilterWrapper(updatedParsingObj.codeResult.get.asInstanceOf[SootClass => Int], classOfInterest, wasInNot))
        return parsingObj
      }
      else if (parsingObj.stringToParse.startsWith("checkClassesWithOuterClassThatSubclassOf(")) {
        val endString = "\")."
        val endLoc = parsingObj.stringToParse.indexOf(endString)
        val classOfInterest = parsingObj.stringToParse.substring("checkClassesWithOuterClassThatSubclassOf(".length() + 1, endLoc)
        parsingObj.stringToParse = parsingObj.stringToParse.substring(endLoc + endString.length)

        val updatedParsingObj = parseStatement(parsingObj)

        //parsingObj.addToCodeResult(s"if(DetectionUtils.classIsSubClass(cl,$classOfInterest)){\n", "}\n")
        def classFilterWrapper(innerFunc: SootClass => Int, filterClass: String): SootClass => Int = {
          def classFilter(cl: SootClass): Int = {
            var caughtProblems = 0
            if (DetectionUtils.classIsSubClass(cl.getOuterClass(), filterClass)) {
              caughtProblems = innerFunc(cl) + caughtProblems
            }
            return caughtProblems
          }

          return classFilter
        }

        parsingObj.codeResult = Some(classFilterWrapper(parsingObj.codeResult.get.asInstanceOf[SootClass => Int], classOfInterest))
        println(s"fourth: ${parsingObj.stringToParse}")
        //Coming back to this after a while, I think this should be updatedParsingObj.
        // I'll need to investigate
        return parsingObj
      }
      else if (parsingObj.stringToParse.startsWith("instanceOf(")) {
        val endString = "\")."
        val endLoc = parsingObj.stringToParse.indexOf(endString)
        parsingObj.instanceType = Some(parsingObj.stringToParse.substring("instanceOf(".length() + 1, endLoc))
        parsingObj.stringToParse = parsingObj.stringToParse.substring(endLoc + endString.length)
        println(s"string to parse after checkSubclassOf: ${parsingObj.stringToParse}")
        val updatedParsingObj = parseStatement(parsingObj)
        return updatedParsingObj
      }
      else if (parsingObj.stringToParse.startsWith("if(")) {
        parsingObj.stringToParse = parsingObj.stringToParse.substring("if(".length())
        val tempParsingObj = new ParseCodeObj(parsingObj.stringToParse, None)
        tempParsingObj.addToContexts("if")
        val ifParsingObj = parseStatement(tempParsingObj)
        if (ifParsingObj.stringToParse.startsWith("then(")){
          ifParsingObj.stringToParse = ifParsingObj.stringToParse.substring("then(".length())
        }else{
          println(s"parsing error for ${ifParsingObj.stringToParse}. It should be on the then( segment")
          sys.exit(1)
        }
        val secondParsingObj = new ParseCodeObj(ifParsingObj.stringToParse, None)
        secondParsingObj.addToContexts("then")
        val thenParsingObj = parseStatement(secondParsingObj)

        //not sure if I should add a context here or not, try without it and check later
        //parsingObj.addToCodeResult(s"if(DetectionUtils.classIsSubClass(cl,$classOfInterest)){\n", "}\n")
        def ifHandlerWrapper(ifFunc: SootClass => Int, thenFunc: SootClass => Int): SootClass => Int = {
          def ifHandler(cl: SootClass): Int = {
            var caughtProblems = 0
            //convert the count returns to booleans
            if (ifFunc(cl) > 0 && thenFunc(cl) < 1) {
              //how do I define the error message print out? For now, I'm going to hard code the
              //choice but I need to later make a way to chose the right one for the right situation
              println(setHasOptionsMenuErrorTemplate.format(cl.getName))
              caughtProblems += 1
            }
            return caughtProblems
          }

          return ifHandler
        }

        parsingObj.codeResult = Some(ifHandlerWrapper(ifParsingObj.codeResult.get.asInstanceOf[SootClass => Int], thenParsingObj.codeResult.get.asInstanceOf[SootClass => Int]))
        parsingObj.stringToParse = thenParsingObj.stringToParse
        return parsingObj
      }
      else if (parsingObj.stringToParse.startsWith("methodToCheck(")) {
        val endLoc = parsingObj.stringToParse.indexOf(')')
        //remove the quotes on the ends
        val methodOfInterest = parsingObj.stringToParse.substring("methodToCheck(".length() + 1, endLoc - 1)
        //assuming . is the next character; determine the method modifier
        val methodModifier = parsingObj.stringToParse.substring(endLoc + 2)
        println(s"method of interest: ${methodOfInterest}")
        println(s"method modifier: ${methodModifier}")
        println("this is a test statement")
        //this option throws an error if second happens before first occurs
        if (methodModifier.startsWith("firstMustOccurBeforeSecond(")) {
          val commaLoc = methodModifier.indexOf(',')
          val method1 = methodModifier.substring("firstMustOccurBeforeSecond(".length() + 1, commaLoc - 1)
          val modifierEndLoc = methodModifier.indexOf(')')
          val method2 = methodModifier.substring(commaLoc + 3, modifierEndLoc - 1)
          println(s"method 1: ${method1}")
          println(s"method 2: ${method2}")

          def performAnalysisWrapper(analysisMethod1: String, analysisMethod2: String): SootMethod => Int = {
            def performAnalysis(m: SootMethod): Int = {
              val s = new GeneralTwoMethodOrderingAnalysis(new ExceptionalUnitGraph(m.getActiveBody), method1, method2)
              return s.getCaughtProblems()
            }

            return performAnalysis
          }
          //parsingObj.addToCodeResult(s"val s = new GeneralTwoMethodOderingAnalysis(new ExceptionalUnitGraph(m.getActiveBody, $method1, $method2))\nproblemCount += s.getCaughtProblems()", "")
          parsingObj.codeResult = Some(performAnalysisWrapper(method1, method2))
          parsingObj.stringToParse = methodModifier.substring(modifierEndLoc + 1)
          println(s"statement at end of first must occur before second: ${parsingObj.stringToParse}")
        }
        else if (methodModifier.startsWith("contains(")) {
          val modifierEndLoc = getPositionOfEndingParenthesisInNestedString(methodModifier).get
          val methodToCheckFor = methodModifier.substring("contains(".length() + 1, modifierEndLoc)
          if (methodToCheckFor.contains('(')) {
            val methodItems = methodToCheckFor.substring(0, methodToCheckFor.length).split('(')
            val methodName = methodItems(0)
            val paramList = methodItems(1).split(',')
            //eventually I should figure out how to not check for such a specific case - probably need
            //to try to cast the soot stmt to a method call and then the params; but this check is
            //what I am currently doing in the checker; so I moved it here. Also might be easier to
            //make more general when I have another example
            if (methodName == "inflate" && paramList.slice(0, paramList.length - 1).forall(_ == "*")
              && paramList(paramList.length - 1) == "false") {
              println("in inflate param is false")

              def checkLastInflateParamIsFalseWrapper(): (SootClass) => Int = {
                def checkLastInflateParamIsFalse(cl: SootClass): Int = {
                  //maybe figure out a way to extract the error messages from these functions
                  var problemCount = 0
                  for (m: SootMethod <- cl.getMethods().asScala) {
                    if (!m.hasActiveBody) {
                      m.retrieveActiveBody()
                    }
                    if (m.isConcrete && m.hasActiveBody) {
                      for (stmt <- m.getActiveBody.getUnits.asScala) {
                        println(stmt)
                        if (stmt.toString().contains("android.view.LayoutInflater: android.view.View inflate(")) {
                          // 0 is how soot stores the final false parameter
                          if (!stmt.toString().endsWith("0)")) {
                            println("start of call chain")
                            //at the moment, the whole call chain isn't needed, just the failing method
                            println(s"${m.toString}   ${m.getDeclaringClass.toString}")
                            println("end of call chain")
                            //The two classes that are printed here are often the same class
                            // - I don't remember when they are different; maybe the two should be replaced with one
                            println("@@@@@ Found a problem: inflate is missing the false parameter in onCreateView in class " + m.getDeclaringClass.getName)
                            System.out.flush()
                            System.err.println("@@@@@ Found a problem: inflate is missing the false parameter in onCreateView in class " + m.getDeclaringClass.getName)
                            System.err.flush();
                            problemCount = problemCount + 1
                          }
                        }
                      }
                    }
                  }
                  return problemCount
                }

                return checkLastInflateParamIsFalse
              }

              parsingObj.stringToParse = methodModifier.substring(modifierEndLoc + 1)
              parsingObj.codeResult = Some(checkLastInflateParamIsFalseWrapper())
            }
            else if(methodName == "setHasOptionsMenu" && paramList.size == 1 && paramList(0) == "true"){
              println("in inflate param is false")

              //I can easily use variables for checking setHasOptionsMenu, but checking that
              //the parameter is true, is harder
              def checkSetHasOptionsMenuTrueWrapper(): (SootClass) => Int = {
                def checkSetHasOptionsMenuTrue(cl: SootClass): Int = {
                  //maybe figure out a way to extract the error messages from these functions
                  var problemCount = 0
                  for (m: SootMethod <- cl.getMethods().asScala) {
                    if (!m.hasActiveBody) {
                      m.retrieveActiveBody()
                    }
                    if (m.isConcrete && m.hasActiveBody) {
                      for (stmt <- m.getActiveBody.getUnits.asScala) {
                        val invokeCall = DetectionUtils.extractInvokeStmtInStmt(stmt)
                        if (invokeCall.isDefined && invokeCall.get.getMethod.getName == "setHasOptionsMenu"
                          && DetectionUtils.isTrue(invokeCall.get.getArg(0))) {
                          problemCount += 1
                        }
                      }
                    }
                  }
                  return problemCount
                }
                return checkSetHasOptionsMenuTrue
              }

              parsingObj.stringToParse = methodModifier.substring(modifierEndLoc + 1)
              parsingObj.codeResult = Some(checkSetHasOptionsMenuTrueWrapper())
              parsingObj.checkEndOfContexts()
            } else {
              println(s"current method is not handled: ${methodToCheckFor}. Please create code to do so")
              sys.exit(1)
            }

          }
          println(methodToCheckFor)
          return parsingObj
          /*def methodContainsWrapper(analysisMethod1: String, analysisMethod2: String): SootMethod => Int = {
            def methodContains(m:SootMethod): Int = {

            }
          }

           */

        }
        //this one throws an error only if second happens and then first happens (second by itself is fine)
        else if (methodModifier.startsWith("firstCannotFollowSecond(")) {
          val commaLoc = methodModifier.indexOf(',')
          val method1 = methodModifier.substring("firstCannotFollowSecond(".length() + 1, commaLoc - 1)
          val modifierEndLoc = methodModifier.indexOf(')')
          val method2 = methodModifier.substring(commaLoc + 3, modifierEndLoc - 1)
          println(s"method 1: ${method1}")
          println(s"method 2: ${method2}")

          def cannotFollowWrapper(analysisMethod1: String, analysisMethod2: String): SootMethod => Int = {
            def cannotFollow(m: SootMethod): Int = {
              var problemCount: Int = 0
              //var foundMethod1: Boolean = false
              var foundMethod1: Boolean = false
              //TODO: I don't think this check pays attention to different paths; update later
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                println(stmt)
                val methodInStatementOption = DetectionUtils.extractMethodCallInStatement(stmt)
                methodInStatementOption match {
                  case Some(methodInStatement) =>
                    if (methodInStatement.getName == analysisMethod1) {
                      println(s"found ${analysisMethod1}")
                      foundMethod1 = true

                    }
                    else if (methodInStatement.getName == analysisMethod2) {
                      println(s"found method 2: ${analysisMethod2}")
                      if (foundMethod1) {
                        println(s"@@@@@ Found a problem: ${analysisMethod1} is called after ${analysisMethod2} in " + m.getDeclaringClass.getName)
                        System.out.flush()
                        System.err.println(s"@@@@@ Found a problem: ${analysisMethod1} is called after ${analysisMethod2} in" + m.getDeclaringClass.getName)
                        System.err.flush();
                        problemCount = problemCount + 1
                      }
                    }
                  case None =>
                    ()
                }
              }
              return problemCount
            }

            return cannotFollow
          }

          parsingObj.codeResult = Some(cannotFollowWrapper(method1, method2))
          parsingObj.stringToParse = methodModifier.substring(modifierEndLoc + 1)
          println(s"statement at end of first must occur before second: ${parsingObj.stringToParse}")
        }

        //parsingObj.addToCodeResult("for (m: SootMethod <- cl.getMethods().asScala) {\nif(m.hasActiveBody && m.isConcrete) {\nif(m.getName.equals(\""+methodOfInterest+"\")) {", "}\n}\n}")
        def filterMethodWrapper(innerFunc: SootMethod => Int, methodOfInterest: String): SootClass => Int = {
          def filterMethod(cl: SootClass): Int = {
            var numberOfProblems = 0
            for (m: SootMethod <- cl.getMethods().asScala) {
              if (m.hasActiveBody && m.isConcrete) {
                if (m.getName.equals(methodOfInterest)) {
                  numberOfProblems = innerFunc(m) + numberOfProblems
                }
              }
            }
            return numberOfProblems
          }

          return filterMethod
        }

        if (parsingObj.codeResult.isDefined) {
          parsingObj.codeResult = Some(filterMethodWrapper(parsingObj.codeResult.get.asInstanceOf[SootMethod => Int], methodOfInterest))
        } else {

        }
        println(s"statement at end of method to check: ${parsingObj.stringToParse}")
        return parsingObj
      } else if (parsingObj.stringToParse.startsWith("absent(")) {
        val endLoc = parsingObj.stringToParse.indexOf("\")")
        println(s"first: ${parsingObj.stringToParse}")
        val methodOfInterest = parsingObj.stringToParse.substring("absent(".length() + 1, endLoc)
        parsingObj.stringToParse = parsingObj.stringToParse.substring(endLoc + 2)
        println(s"second: ${parsingObj.stringToParse}")

        //val updatedParsingObj = parseStatement(parsingObj)
        //parsingObj.addToCodeResult(s"if(DetectionUtils.classIsSubClass(cl,$classOfInterest)){\n", "}\n")
        //TODO: figure out how to abstract out the found a problem statements; probably just need to
        //have the developer define the error message and the API string
        def absentWrapper(methodOfInterest: String): SootClass => Int = {
          def absent(cl: SootClass): Int = {
            var problemCount: Int = 0
            for (m: SootMethod <- cl.getMethods().asScala) {
              if (m.isConcrete && m.hasActiveBody) {
                for (stmt <- m.getActiveBody.getUnits.asScala) {
                  if (stmt.toString().contains(methodShorthandToFullDeclaration(methodOfInterest))) {
                    println("start of call chain")
                    //at the moment, the whole call chain isn't needed, just the failing method
                    println(s"${m.toString}   ${m.getDeclaringClass.toString}")
                    println("end of call chain")
                    println(s"@@@@@ Found a problem: calling getResources on a background fragment in ${m.getName()} of ${cl.getName()} with outer Fragment class ${cl.getOuterClass.getName}")
                    System.out.flush()
                    System.err.println(s"@@@@@ Found a problem: calling getResources on a background fragment in ${m.getName()} of ${cl.getName()} with outer Fragment class ${cl.getOuterClass.getName}")
                    System.err.flush()
                    problemCount = problemCount + 1
                  }
                }
              }
            }
            return problemCount
          }

          return absent
        }

        parsingObj.codeResult = Some(absentWrapper(methodOfInterest))
        println(s"third: ${parsingObj.stringToParse}")
        return parsingObj
      } else if (parsingObj.stringToParse.startsWith("exclusiveOrInstance(")) {
        //exclusiveOrInstance("setPackage", "setSelector")
        val stringToParse = parsingObj.stringToParse.substring("exclusiveOrInstance(".length())
        println(s"string to parse: ${stringToParse}")
        val commaLoc = stringToParse.indexOf(',')
        val endLoc = stringToParse.indexOf(')')
        val method1String = stringToParse.substring(1, commaLoc - 1)
        //the last substring call removes the " from the beginning of the method
        val method2String = stringToParse.substring(commaLoc + 1, endLoc - 1).trim().substring(1)
        println(s"method 1: ${method1String}")
        println(s"method 2: ${method2String}")

        def exclusiveOrInstanceWrapper(varTypeName: String, method1: String, method2: String): SootClass => Int = {
          def exclusiveOrInstance(cl: SootClass): Int = {
            var problemCount = 0
            if (DetectionUtils.isCustomClassName(cl.getName())) {
              for (m: SootMethod <- cl.getMethods().asScala) {
                if (m.hasActiveBody && m.isConcrete) {
                  if (!m.getName.contains("dummyMainMethod")) {
                    println(s"running analysis class: ${cl.getName()} method: ${m.getName()}")
                    val s = new AnalyzeExclusiveCallsOnAVariableType(new ExceptionalUnitGraph(m.getActiveBody), varTypeName, method1, method2)
                    if (s.getCaughtProblems() > 0) {
                      println(s"@@@@@ problem in class ${cl.getName()}")
                    }
                    println(s"caught problems: ${s.getCaughtProblems()}")
                    problemCount += s.getCaughtProblems()
                  }
                }
              }
            }
            return problemCount
          }

          return exclusiveOrInstance
        }

        parsingObj.codeResult = Some(exclusiveOrInstanceWrapper(parsingObj.instanceType.get, method1String, method2String))
        parsingObj.stringToParse = stringToParse.substring(endLoc + 1)
        return parsingObj
      }
      else if (parsingObj.stringToParse.startsWith("not(")) {
        parsingObj.stringToParse = parsingObj.stringToParse.substring("not(".length())
        parsingObj.addToContexts("not")
        val updatedParsingObj = parseStatement(parsingObj)
        return updatedParsingObj

      }
      else if (parsingObj.stringToParse.startsWith("in(")) {
        //exclusiveOrInstance("setPackage", "setSelector")
        val stringToParse = parsingObj.stringToParse.substring("in(".length())
        println(s"string to parse: ${stringToParse}")
        val commaLoc = stringToParse.indexOf(',')
        val endLoc = stringToParse.indexOf(')')
        val method1String = stringToParse.substring(1, commaLoc - 1)
        //the last substring call removes the " from the beginning of the method
        val stateName = stringToParse.substring(commaLoc + 1, endLoc - 1).trim().substring(1)
        println(s"method 1: ${method1String}")
        println(s"method 2: ${stateName}")

        //actually, what really would make sense for the isSubclass would be to pass that information here,
        //but that would require looking ahead in the parsing, or sending the information forward and
        def inHandlerWrapper(methodNameToCheckFor: String, stateCheckFunction: ControlFlowItem => Boolean,checkingClasses: Boolean = true): SootClass => Int = {
          var alreadyChecked = false
          def inHandler(cl: SootClass): Int = {
            //this only needs to run once, not once for each class
            var problemCount = 0
            if (! alreadyChecked) {
              println("inHandler called")
              var callChains: List[ControlFlowChain] = List()
              var (startingMethod, calledByList) = getStartingMethodAndCallChain(methodNameToCheckFor)
              val fullCallChains: ListBuffer[ControlFlowChain] = new ListBuffer[ControlFlowChain]()
              if (startingMethod.isDefined) {
                createCallChainsDepthFirst(calledByList, fullCallChains, List[ControlFlowItem](new ControlFlowItem(startingMethod.get, checkingClasses)), methodNameToCheckFor, checkingClasses)
              }
              callChains = fullCallChains.toList
              var alreadyReportedErrors = new mutable.HashMap[String, Boolean]()
              println(s"length of call chains: ${callChains.length}, length of distinct call chains: ${callChains.distinct.length}")
              for (chain <- callChains) {
                println("new chain")
                println(s"${chain.controlChain}")
                Console.flush
                val reversedList = chain.controlChain.reverse
                val methodCallWithError = reversedList(1)
                println(s"method call with error: ${methodCallWithError.methodCall.toString}")
                print("already reported errors: ")
                for (m <- alreadyReportedErrors) {
                  print(s"${m._1} ")
                }
                print("\n")
                if (!alreadyReportedErrors.contains(methodCallWithError.methodCall.toString)) {
                  //println("checking call chain")
                  //check if the chain contains a call to a method that demonstrates the fragment has been initialized
                  println(s"${!chain.controlChain.exists(call => FragmentLifecyleMethods.isMethodWhenFragmentInitialized(call.methodCall))}")
                  println(s"${!checkingClasses}")
                  println(s"${!chain.controlChain.forall(call => DetectionUtils.classIsSubClassOfFragment(call.methodCall.getDeclaringClass))}")
                  if (!chain.controlChain.exists(call => FragmentLifecyleMethods.isMethodWhenFragmentInitialized(call.methodCall))
                    && (!checkingClasses || !chain.controlChain.forall(call => DetectionUtils.classIsSubClassOfFragment(call.methodCall.getDeclaringClass)))) {
                    alreadyReportedErrors += (chain.controlChain.reverse(1).methodCall.toString -> true)
                    val errorString = "@@@@@ Found a problem: getActivity may be called when " +
                      "the Fragment is not attached to an Activity" +
                      s": call sequence ${chain.controlChain}"
                    println(errorString)
                    System.out.flush()
                    System.err.println(errorString)
                    System.err.flush()
                    problemCount += 1
                  }
                }
              }
              alreadyChecked = true
            }
            return problemCount
          }

          return inHandler
        }

        parsingObj.codeResult = Some(inHandlerWrapper(method1String, stateChecks(stateName)))
        parsingObj.stringToParse = stringToParse.substring(endLoc + 1)
        return parsingObj
      }
      else {
        throw new RuntimeException(s"unable to parse |${parsingObj.stringToParse}|")
      }
    }

    val cleanedStatementToParse = statementToParse.replaceAll(" ", "")
    val p = new ParseCodeObj(cleanedStatementToParse, None)
    val result = parseStatement(p)
    println(s"result parse string: ${result.stringToParse}")
    //println(s"result code result: ${result.codeResult}")
    GeneralDetectionMethod.executeDetectionTemplate(args, result.codeResult.get.asInstanceOf[SootClass => Int])
  }
}
