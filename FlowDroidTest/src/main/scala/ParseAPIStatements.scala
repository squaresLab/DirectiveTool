import soot.toolkits.graph.ExceptionalUnitGraph
import soot.{SootClass, SootMethod}

import scala.collection.JavaConverters._

object ParseAPIStatements {

  def main(args: Array[String]): Unit = {
    //TODO: figure out how to make this code work with spaces in the statement or without

    //Done:
    //val statementToParse: String =  "checkSubclassOf(\"Activity\").methodToCheck(\"onCreate\").requireCallOrder(\"setContentView\", \"findViewById\")"
    //val statementToParse: String = "checkSubclassOf(\"AsyncTask\").checkClassesWithOuterClassThatSubclassOf(\"Fragment\").absent(\"getResources\")"
    val statementToParse: String = "exclusiveOrInstance(\"setPackage\", \"setSelector\")"

    //Not done:
    //val statementToParse: String  = "and(and(method(\"onClick\").contains(\"setArguments\"), and (methodToCheck(\"onTabSelected\").contains(\"add\")), methodToCheck(\"onTabUnselected\").contains(\"hide\")))"

    val methodShorthandToFullDeclaration: Map[String, String] = Map("getResources" -> "android.content.res.Resources getResources()")

    /* I am writing this quickly, might want to refactor later
     */
    def parseStatement(parsingObj: ParseCodeObj): ParseCodeObj = {
      parsingObj.stringToParse = parsingObj.stringToParse.trim()
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
        println(s"second part of statement: ${secondPartOfStmt}")
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
      else if (parsingObj.stringToParse.startsWith("checkSubclassOf(")) {
        val endString = "\")."
        val endLoc = parsingObj.stringToParse.indexOf(endString)
        val classOfInterest = parsingObj.stringToParse.substring("checkSubclassOf(".length() + 1, endLoc)
        parsingObj.stringToParse = parsingObj.stringToParse.substring(endLoc+endString.length)
        println(s"string to parse after checkSubclassOf: ${parsingObj.stringToParse}")
        val updatedParsingObj = parseStatement(parsingObj)
        //parsingObj.addToCodeResult(s"if(DetectionUtils.classIsSubClass(cl,$classOfInterest)){\n", "}\n")
        def classFilterWrapper(innerFunc: SootClass => Int, filterClass: String): SootClass => Int = {
          def classFilter(cl: SootClass): Int = {
            var caughtProblems = 0
            if(DetectionUtils.classIsSubClass(cl,filterClass)) {
              caughtProblems = innerFunc(cl) + caughtProblems
            }
            return caughtProblems
          }
          return classFilter
        }
        parsingObj.codeResult = Some(classFilterWrapper(parsingObj.codeResult.get.asInstanceOf[SootClass => Int],classOfInterest))
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
        if (methodModifier.startsWith("requireCallOrder(")) {
          val commaLoc = methodModifier.indexOf(',')
          val method1 = methodModifier.substring("requireCallOrder(".length() + 1, commaLoc - 1)
          val modifierEndLoc = methodModifier.indexOf(')')
          val method2 = methodModifier.substring(commaLoc + 3, modifierEndLoc - 1)
          println(s"method 1: ${method1}")
          println(s"method 2: ${method2}")
          //while I can make this work, I'm not sure how a person creating the method is supposed to know that the method variable will be called m
          def performAnalysisWrapper(analysisMethod1: String, analysisMethod2: String): SootMethod => Int = {
            def performAnalysis (m: SootMethod): Int = {
              val s = new GeneralTwoMethodOrderingAnalysis(new ExceptionalUnitGraph(m.getActiveBody), method1, method2)
              return s.getCaughtProblems()
            }
            return performAnalysis
          }
          //parsingObj.addToCodeResult(s"val s = new GeneralTwoMethodOderingAnalysis(new ExceptionalUnitGraph(m.getActiveBody, $method1, $method2))\nproblemCount += s.getCaughtProblems()", "")
          parsingObj.codeResult = Some(performAnalysisWrapper(method1,method2))
          parsingObj.stringToParse = methodModifier.substring(modifierEndLoc + 1)
          println(s"statement at end of require call order: ${parsingObj.stringToParse}")
        }
        else if(methodModifier.startsWith("contains(")){
          val modifierEndLoc = methodModifier.indexOf(")")
          val methodToCheckFor = methodModifier.substring("requireCallOrder(".length() + 1, modifierEndLoc - 1)
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
        parsingObj.codeResult = Some(filterMethodWrapper(parsingObj.codeResult.get.asInstanceOf[SootMethod => Int], methodOfInterest))
        println(s"statement at end of method to check: ${parsingObj.stringToParse}")
        return parsingObj
      }else if (parsingObj.stringToParse.startsWith("absent(")) {
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
      } else if (parsingObj.stringToParse.startsWith("exclusiveOrInstance(")){
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
        def exclusiveOrInstanceWrapper(varTypeName: String, method1: String, method2: String): SootClass => Int ={
          def exclusiveOrInstance(cl: SootClass): Int ={
            var problemCount = 0
            if(DetectionUtils.isCustomClassName(cl.getName())) {
              for (m: SootMethod <- cl.getMethods().asScala) {
                if(m.hasActiveBody && m.isConcrete) {
                  if(!m.getName.contains("dummyMainMethod")) {
                    println(s"running analysis class: ${cl.getName()} method: ${m.getName()}")
                    val s = new AnalyzeExclusiveCallsOnAVariableType(new ExceptionalUnitGraph(m.getActiveBody), varTypeName, method1, method2)
                    if (s.getCaughtProblems() > 0){
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
        parsingObj.codeResult = Some(exclusiveOrInstanceWrapper("Intent", "setSelector", "setPackage"))
        parsingObj.stringToParse = stringToParse.substring(endLoc + 1)
        return parsingObj
      }
      else {
        throw new RuntimeException(s"unable to parse |${parsingObj.stringToParse}|")
      }
    }
    val p = new ParseCodeObj(statementToParse, None)
    val result = parseStatement(p)
    println(s"result parse string: ${result.stringToParse}")
    //println(s"result code result: ${result.codeResult}")
    GeneralDetectionMethod.executeDetectionTemplate(args, result.codeResult.get.asInstanceOf[SootClass=> Int])
  }
}
