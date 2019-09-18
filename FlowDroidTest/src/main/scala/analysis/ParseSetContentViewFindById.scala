package analysis

import soot.{SootClass, SootMethod}
import soot.toolkits.graph.ExceptionalUnitGraph

import scala.collection.JavaConverters._

object ParseSetContentViewFindById {

  def main(args: Array[String]): Unit = {
    //TODO: figure out how to make this code work with spaces in the statement or without
    val statementToParse: String =  "and(subClass(\"Activity\"), methodToCheck(\"onCreate\").requireCallOrder(\"setContentView\", \"findViewById\"))"
    /* I am writing this quickly, might want to refactor later
     */
    def parseStatement(parsingObj: ParseCodeObj): ParseCodeObj = {
      parsingObj.stringToParse = parsingObj.stringToParse.trim()
      if (parsingObj.stringToParse.startsWith("and(")) {
        //save but don't parse it yet, we need to read from the end to the front
        val firstPartOfAnd = parsingObj.stringToParse.substring("and(".length(), parsingObj.stringToParse.indexOf(','))
        val middleOfStmt = parsingObj.stringToParse.substring(parsingObj.stringToParse.indexOf(','))
        if (!middleOfStmt.startsWith(",")) {
          throw new RuntimeException("missing comma in and statement")
        }
        val secondPartOfStmt = middleOfStmt.substring(1)
        println(s"second part of statement: ${secondPartOfStmt}")
        parsingObj.stringToParse = secondPartOfStmt
        val partiallyUpdatedParsingObj = parseStatement(parsingObj)
        if (!partiallyUpdatedParsingObj.stringToParse.startsWith(")")) {
          throw new RuntimeException(s"missing end of and statement: ${partiallyUpdatedParsingObj.stringToParse}")
        }
        //need to add a meaning to the and statement
        //updatedParsingObj.stringToParse = updatedParsingObj.stringToParse.substring(1)
        partiallyUpdatedParsingObj.stringToParse = firstPartOfAnd
        val updatedParsingObj = parseStatement(partiallyUpdatedParsingObj)
        return updatedParsingObj
      }
      else if (parsingObj.stringToParse.startsWith("subClass(")) {
        val endLoc = parsingObj.stringToParse.indexOf("\")")
        val classOfInterest = parsingObj.stringToParse.substring("subClass(".length() + 1, endLoc)
        parsingObj.stringToParse = parsingObj.stringToParse.substring(endLoc + 2)
        //val updatedParsingObj = parseStatement(parsingObj)
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
