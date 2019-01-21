import java.io.{FileOutputStream, PrintStream}

import com.sun.org.apache.xalan.internal.xsltc.dom.MatchingIterator
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.options.Options

import scala.collection.JavaConverters._
import scala.collection.mutable.ListBuffer
import scala.util.matching.Regex
import RegexUtils._

/*
What would I need to check for this directive?:
- Tabs are changed in onTabSelected
- Fragment is hidden in onTabUnselected
- (wait, this would always be wrong because the tab is instantiated, nevermind on this) Tab is not the first tab (remove this check because I can't figure out how to make it app specfic)
- Tab is referenced in setArguments
*/

object DetectSetArgumentsMain {



  def main(args: Array[String]): Unit = {
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    val apkLocation = DetectionUtils.getAPKLocation(args)
    val analyzer = new SetupApplication(
      "/Users/zack/Library/Android/sdk/platforms/android-21/android.jar",
      apkLocation)
    //  "/Users/zack/git/ViolationOfDirectives/Application/build/intermediates/instant-run-apk/debug/Application-debug.apk")
    //There seems to be an analysis blocker at Infoflow.java on line 293 that stops building the callgraph
    //if this is not set
    analyzer.getConfig.setTaintAnalysisEnabled(true)
    analyzer.getConfig.setMergeDexFiles(true)
    analyzer.getConfig.setCodeEliminationMode(InfoflowConfiguration.CodeEliminationMode.NoCodeElimination)
    analyzer.getConfig.getAnalysisFileConfig.setSourceSinkFile("/Users/zack/Documents/intelliJWorkspace/FlowDroidTest/SourcesAndSinks.txt")
    Scene.v().releaseCallGraph()
    //Options.v().set_process_multiple_dex(true)
    Options.v().set_process_multiple_dex(false)
    PhaseOptions.v().setPhaseOption("cg", "verbose")
    println(PhaseOptions.v().getPhaseOptions("cg"))
    analyzer.getConfig.setImplicitFlowMode(ImplicitFlowMode.AllImplicitFlows)
    analyzer.getConfig().setCallgraphAlgorithm(CallgraphAlgorithm.VTA)
    //fast analyzer adds all possible callbacks, not just those that are reachable
    //unfortunately, the analyzer is saying that onClick methods which are reachable
    //are not, so currently using the fast analyzer
    analyzer.getConfig.getCallbackConfig.setCallbackAnalyzer(CallbackAnalyzer.Fast)
    analyzer.constructCallgraph()
    var possibleProblemCount = 0
    var tabsAreAdded = false
    var tabsAreHidden = false
    //var tabIsReferencedInHasSetArguments = false
    var possibleErrorString = ""
    for(cl:SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      //println(s"class: ${cl.getName}")
      for (m: SootMethod <- cl.getMethods().asScala) {
        //println(s"method: ${m.getName}")
        if (m.isConcrete && m.hasActiveBody) {
          println("new method")
          println(s"class: ${m.getDeclaringClass.getName} method: ${m.getName}")
          for (stmt <- m.getActiveBody.getUnits.asScala) {
            //m.getActiveBody.getParameterRefs.indexOf(0).
            println(stmt)
            //determine the class of the first tab and make sure that class is not added twice
          }
        }

        def superClassIsActionBarTabListener(c: SootClass): Boolean = {
          if (c.getName().contains("TabListener")){
            return true
          }
          else if (c.hasSuperclass) {
            return superClassIsActionBarTabListener(c.getSuperclass)
          }
          else {
            return false
          }
        }

        def checkStatement(statementToLookFor: Regex, m: SootMethod): Boolean = {
          var thisVariableName = ""
          var fragmentVariableName = ""
          for (stmt <- m.getActiveBody.getUnits.asScala) {
            //Goal is to get the the fragment variable reference of the current class object
            //The first line sets a variable reference to this, so save the variable reference
            //that refers to this
            if (stmt.toString().contains(":= @this")) {
              thisVariableName = stmt.toString().split(" ")(0)
            }
            //Using the variable reference that refers to this, save the variable reference
            //that refers to this.fragment
            if (thisVariableName != "" && stmt.toString().contains(thisVariableName)) {
              if (stmt.toString().contains("android.app.Fragment")) {
                fragmentVariableName = stmt.toString().split(" ")(0)
              }
            }
            if (statementToLookFor matches stmt.toString()) {
              //this next check might be better if it checked if the fragmentVariableName was used in the
              //parameter list. But due to the typing constraints, I don't think the fragmentVariableName
              //can be anywhere else, so I'd have to see more examples to determine if I am right or not
              //
              //If the statement is the right method call and refers to the fragment reference,
              //then return that the method was successfully found
              if (fragmentVariableName != "" && stmt.toString().contains(fragmentVariableName)) {
                System.err.println(s"statement of interest: ${stmt}")
                return true
              }

            }
          }
          return false
        }

        if (m.getName == "onTabSelected" && superClassIsActionBarTabListener(m.getDeclaringClass)) {
          tabsAreAdded = checkStatement("""virtualinvoke .*android\.app\.FragmentTransaction add.*""".r, m)
        }
        if (m.getName == "onTabUnselected" && superClassIsActionBarTabListener(m.getDeclaringClass)) {
          tabsAreHidden = checkStatement("""virtualinvoke .*android\.app\.FragmentTransaction hide.*""".r, m)
        }

        /*You don't check if the super class is a fragment
          for the method onClick because the
          on click listener is an inner class whose super class is not
          a Fragment
         */
        def superClassIsFragment(c: SootClass): Boolean = {
          println(s"class name ${c.getName()}")
          if (c.getName.contains("android.app.Fragment")) {
            return true
          }
          else {
            if (c.hasSuperclass) {
              return superClassIsFragment(c.getSuperclass)
            }
            else {
              return false
            }
          }
        }
        if (m.getName().contains("onClick")){
          println("for debugging")
          superClassIsFragment(m.getDeclaringClass)
        }
        println("")
        if (m.getName.contains("onClick")) {
          println(s"parent class of m ${m.getDeclaringClass.toString}")
          for (stmt <- m.getActiveBody.getUnits.asScala) {
            if (stmt.toString().contains("void setArguments(android.os.Bundle)")) {
              val errorString = "@@@@ Found a problem: onClick contains a call to " +
                "setArguments on a Fragment when the Fragment may already be initialized in " +
                s"class ${m.getDeclaringClass.getName}"
              possibleErrorString += errorString + "\n"
              //println(errorString)
              //System.out.flush()
              //System.err.println(errorString)
              //System.err.flush()
              possibleProblemCount += 1
            }
          }
        }
      }
    }
        /*
            def superClassIsActivity(c: SootClass) : Boolean = {
              if (c.getName.contains("android.app.Activity")){
                return true
              }
              else{
                if (c.hasSuperclass){
                  return superClassIsActivity(c.getSuperclass)
                }
                else {
                  return false
                }
              }
            }
            def stringContainsItemInList(stringToCheck: String, listOfStrings: List[String]) : Boolean = {
              for(item <- listOfStrings){
                //This next statement could be written in a more optimized way but doing this way
                //for simplicity of implementation the first timej
                if(stringToCheck.contains(item)){
                  return true
                }
              }
              return false
            }
            if (m.getName().contains("onCreate") && superClassIsActivity(m.getDeclaringClass)){
              val tabReferences: ListBuffer[String] = new ListBuffer[String]
              //currently deciding to do multiple passes through the output to make writing the
              //code easier; may want to go back later and optimize this depending on the overhead
              def createVariable(statementString: String) : Option[(String, String)] = {
                val NewInstancePattern = """(\$r[0-9]+) = staticinvoke <(.*): (.*) newInstance()>()""".r
                 statementString match {
                  //based on the example I have, className1 and className2 should be same string
                  case NewInstancePattern(variableName, className1, className2) => {
                      return Some((variableName,className1))
                  }
                  case _ => return None
                }
              }
              val classVariableMapping = new MyBiMap[String](m.getActiveBody.getUnits.asScala.flatMap(x => createVariable(x.toString())).toSeq)
              println(classVariableMapping)
              //looping through the code again once we have the tab variable-class mappings
              //to collect the tabVariables
              def extractTabVariable(statementString: String) : Option[String] = {
                val TabVarPattern = """(\$r[0-9]+ = virtualinvoke (\$r[0-9]+)\.<android\.app\.ActionBar\$Tab: android\.app\.ActionBar\$Tab newTab\(\)>\(\)""".r
                statementString match {
                    //based on the example I have, var1 and var2 should be the same string
                  case TabVarPattern(var1,var2) => {
                    return Some(var1)
                  }
                  case _ => return None
                }
              }
              val tabVariables = m.getActiveBody.getUnits.asScala.flatMap(x => extractTabVariable(x.toString()))
              def extractAllVariableReferencesFromLine(statementString: String) : (Regex.MatchIterator) = {
                val VariablePattern = """(\$r[0-9]+)""".r
                return VariablePattern.findAllIn(statementString)
              }
              def extractTabVariablesToClassVariables(statementString: String): Option[(String,Seq[String])] = {
                val VirtualInvokePattern = """^virtualinvoke.*""".r
                val StaticInvokePattern = """^staticinvoke.*""".r
                val lineVariables: Option[Regex.MatchIterator] = statementString match {
                  case VirtualInvokePattern => Some(extractAllVariableReferencesFromLine(statementString))
                  case StaticInvokePattern => Some(extractAllVariableReferencesFromLine(statementString))
                  case _ => None
                }
                lineVariables match {
                  case Some(x) => {
                    val allLineVars = x.toList
                    allLineVars.size match {
                      case 0 => return None
                      case 1 => return Some(allLineVars(0), Seq[String]())
                      case _ => return Some(allLineVars(0), allLineVars.tail)
                    }
                  }
                }
              }
              val variableInstantiationDependencies = m.getActiveBody.getUnits.asScala.flatMap(x => extractTabVariablesToClassVariables(x.toString()))

                val TabListenerPattern = """virtualinvoke (\$r[0-9]+)\.<android\.app\.ActionBar\$Tab: android\.app\.ActionBar\$Tab setTabListener(android\.app\.ActionBar\$TabListener)>\((\$r[0-9]+)\)""".r

                """specialinvoke (\$r[0-9]+\.<com\.example\.android\.lnotifications.LNotificationActivity$FragmentTabListener: void <init>(android.app.Activity,android.app.Fragment,java.lang.String)>($r0, $r8, "visibility")""".r
                if(stringContainsItemInList(stmt.toString(), tabReferences.toList)){
                  stmt match {
                    case TabListenerPattern(fragmentVariable, tabVariable) =>
                      println(s"fragment variable ${fragmentVariable}")
                      println(s"tab variable ${tabVariable}")
                    case _ => ()
                  }

                }
              }

            }

            if(m.getName.contains("onClick")){
              for(stmt <- m.getActiveBody.getUnits.asScala){
                 if(stmt.toString().contains("void setArguments(android.os.Bundle)")) {
                   val errorString = "@@@@ Found a problem: onClick contains a call to " +
                     "setArguments on a Fragment when the Fragment may already be initialized in " +
                     s"class ${m.getDeclaringClass.getName}"
                   println(errorString)
                   System.out.flush()
                   System.err.println(errorString)
                   System.err.flush()
                   problemCount += 1
                 }
              }
            }
            println("")
        }
      }
    }
    */
    if(tabsAreAdded && tabsAreHidden){
      System.err.print(possibleErrorString)
      println(s"total number of problems: ${possibleProblemCount}")
    }
  }
}
