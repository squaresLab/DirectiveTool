package analysis

import soot.jimple.SpecialInvokeExpr
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.jimple.internal._
import soot.options.Options
import soot.{PhaseOptions, Scene, SootClass, SootMethod}

import scala.collection.JavaConverters._


object DetectIncorrectSetInitialSavedState {
  def main(args: Array[String]): Unit = {
    runAnalysis(args)
  }
  /*  System.setOut(new PrintStream(new FileOutputStream(java.io.FileDescriptor.out)) {
      override def print(s: String): Unit = {
        super.print(s)
        if (s.contains("android.support")) throw new RuntimeException("Found you!")
      }
    })
    */
  def runAnalysis(args: Array[String]): Unit = {
    val startTime = System.nanoTime()
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")

    val apkLocation = DetectionUtils.getAPKLocation(args)
    val analyzer = new SetupApplication(
      DetectionUtils.getAndroidJarLocation(args),
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
    var problemCount = 0
    var possibleProblemCount = 0
    var tabsAreAdded = false
    var tabsAreHidden = false
    //var tabIsReferencedInHasSetArguments = false
    var possibleErrorString = ""
    //create a simple be inefficient control flow graph for setArguments because
    //FlowDroid can't seem to handle anonymous inner classes in it's control flow
    //graph creation

    //This method is going to be inefficient; consider changing it to something
    //more efficient if you need to
    def getControlChainAlreadyPresent[X](currentChains: List[List[ControlFlowItem]], newChain: List[ControlFlowItem], isCheckingClassName: Boolean = true): Option[List[ControlFlowItem]] = {
      for (listItem <- currentChains) {
        if (listItem == newChain) {
          //println("match")
          return Some(listItem)
        } else {
          //println("no match")
        }
      }
      return None
    }

    var stillChanging = true
    var wasChanged = false
    var stillOnFirstPass = true
    //may want to change this from a sequence to a hash table if this gets too large;
    //since it might become inefficient; I think the list will stay small though
    //so a list is better than a hash map in that case
    //Also, I might want to later add a class to the getActivityCall, so I can keep track
    //of which class is calling getActivity to make the checker better
    val methodNameToCheckFor = "setInitialSavedState"
    var callChains: List[ControlFlowChain] = List()
    val checkingClasses = true
    //not sure how to write this functionally; might want to figure out later to clean this
    //up but I'm going to implement the quick way first
    while (stillChanging) {
      stillChanging = false
      //unsure about this variable type at this point
      var newCallChains: List[ControlFlowChain] = List()
      for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
        //println("in class loop")
        //no idea why I need this xmlpull check. These for loops through the classes and methods seem to
        //work on other checkers
        if (DetectionUtils.isCustomClassName(cl.getName) && !cl.getName.contains("xmlpull")) {
          for (m: SootMethod <- cl.getMethods().asScala) {
            try {
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                //println("in second for")
                if (stillOnFirstPass && stmt.toString().contains(methodNameToCheckFor)) {
                  extractMethodCallInStatement(stmt) match {
                    case Some(m) => newCallChains = addControlFlowChain(newCallChains, new ControlFlowChain(List(new ControlFlowItem(m, checkingClasses))))
                    case None => ()
                  }
                  stillChanging = true
                }
                for (chainToCheck <- callChains) {
                  //println("in third for")
                  /*
                def checkForClassMatch(callClass: String, stmt: String, checkingForExactClasses: Boolean = true): Boolean = {
                  //turn off (i.e. set to false) if you want to just match by method name
                  //actually not that easy. I am still checking repeats with class and
                  //method name. Would have to figure out how to easily remove those class
                  // checks as well
                  if (!checkingForExactClasses) {
                    return true
                  }
                  else {
                    return stmt.contains(callClass)
                  }
                }

                //the contains callClass check does not match on call for super classes (fails on dynamic dispatch)
                */
                  //remove the true later; added for debugging

                  //If we find the method we are interested in. Add it to the call chain
                  val possibleMethod = extractMethodCallInStatement(stmt)
                  if (!possibleMethod.isEmpty && possibleMethod.get == chainToCheck.controlChain.head.methodCall) {
                    val newChain = (new ControlFlowItem(m, checkingClasses) +: chainToCheck.controlChain)
                    newCallChains = addControlFlowChain(newCallChains, new ControlFlowChain(newChain))
                    chainToCheck.wasExtended = true
                    stillChanging = true
                  }
                }
              }
            }
            catch {
              case r: RuntimeException => {
                //println(s"error with method ${m.getName} - skipping")
                //skip method with problem
              }
            }
          }
        }
      }
      val savedCallChains = callChains.filter(x => !x.wasExtended)
      newCallChains = newCallChains ++ callChains.filter(x => !x.wasExtended)
      callChains = newCallChains
      stillOnFirstPass = false
    }
/*    println("call chains")
    for (callChain <- callChains) {
      println(s"${callChain.controlChain}")
    }*/
    for (chain <- callChains) {
      //check if the chain contains a call to a method that demonstrates the fragment has been initialized
      //(note) I think this is right.  Might need to check my logic later
      if (chain.controlChain.exists(call => classIsSubClassOfFragment(call.methodCall.getDeclaringClass) && FragmentLifecyleMethods.isMethodWhenFragmentInitialized(call.methodCall))
      || (checkingClasses && chain.controlChain.forall(call => classIsSubClassOfFragment(call.methodCall.getDeclaringClass)))){
        println("start of call chain")
        for(chainItem <- chain.controlChain){
          println(s"${chainItem.methodCall.toString}   ${chainItem.methodCall.getDeclaringClass.toString}")
        }
        //these control chains are the opposite order from the order of getActivity and are throwing
        //off the code parsing the print errors
        val printedControlChain = chain.controlChain
        println("end of call chain")
        val errorString = "@@@@@ Found a problem: setInitialSavedState may be called when " +
          "the Fragment is attached to an Activity" +
          s": call sequence ${printedControlChain}"
        println(errorString)
        System.out.flush()
        System.err.println(errorString)
        System.err.flush()
        problemCount += 1
      }
    }
    println(s"total number of caught problems: ${problemCount}")
    val totalTime = System.nanoTime() - startTime
    println(s"total time (in nanoseconds): ${totalTime}")
    println(s"total time (in seconds): ${totalTime/1000000000}")
  }

  def classIsSubClassOfFragment(c: SootClass): Boolean = {
    if(c.toString() == "android.app.Fragment"){
      return true
    } else {
      if(c.hasSuperclass) {
        return classIsSubClassOfFragment(c.getSuperclass)
      } else {
        return false
      }
    }
  }

  def addControlFlowChain(controlFlowChainList: List[ControlFlowChain], controlFlowChainToAdd: ControlFlowChain): List[ControlFlowChain] = {
    if (controlFlowChainList.contains(controlFlowChainToAdd)){
      return controlFlowChainList
    } else {
      return controlFlowChainToAdd +: controlFlowChainList
    }
  }


  def extractMethodCallInStatement(u: soot.Unit): Option[SootMethod] = {
    def handleStmt(stmt: soot.jimple.Stmt): Option[SootMethod] = {
      stmt match {
        case assignmentStatment: JAssignStmt => {
          assignmentStatment.rightBox.getValue match {
            case staticExpr: JStaticInvokeExpr => {
              return Some(staticExpr.getMethod)
            }
            case invokeExpr: JVirtualInvokeExpr => {
              return Some(invokeExpr.getMethod)

            }
            case linkedBox: SpecialInvokeExpr=> {
              return Some(linkedBox.getMethod)
            }
            case _ => {
              return None}
          }
        }
        case invokeExpr: InvokeExprBox => {
          invokeExpr match {
            case staticExpr: JStaticInvokeExpr => {
              return Some(staticExpr.getMethod)
            }
            case invokeExpr: JVirtualInvokeExpr => {
              return Some(invokeExpr.getMethod)
            }
            case _ => return None
          }
        }
        case invokeSmt: JInvokeStmt => {
          return Some(invokeSmt.getInvokeExpr.getMethod)
        }
        case _ => return None
      }
    }

    u match {
      case s: soot.jimple.Stmt => return handleStmt(s)
      case _ => return None
    }
  }
}
                /*
                if ((callClass == "" || checkForClassMatch(callClass, stmt.toString(), checkingForExactClasses)) && stmt.toString().contains(callMethodName)) {
                  //this is a bit hacky. I'm not sure about the best way to handle looping between methods
                  //of different classes with the same name, since the calls may be to objects of the
                  //parent type as well.
                  //I'll come back to this if necessary
                  //-----------
                  //I'm not sure if this is the right way to represent the methods, but I'm adding the
                  //class name because the current method trace without them seems confusing
                  def getMethodToCheck(fullMethodName: String): String = {
                    val items = fullMethodName.split("""\.""")
                    //val items = fullMethodName.split("""\.""")
                    if (items.size < 2) {
                      return items(0)
                    } else {
                      return items.last
                    }
                  }

                  def doesMethodHaveCircularDependency[String](m: SootMethod, callChain: List[ControlFlowItem]): Boolean = {
                    return (callChain.head == m || (!callChain.tail.isEmpty && callChain.tail.head == m))
                  }

                  if (!doesMethodHaveCircularDependency(m, callToCheck)) {
                    val newControlFlowItem: ControlFlowItem = new ControlFlowItem(m)
                    newControlFlowItem +: callToCheck.methodChain)
                    //could probably impore getControlChainAlreadyPresent to handle cases were I am only checking that that method
                    //names match
                    if (getControlChainAlreadyPresent(newSetArgumentsCallChains, newControlFlowItem).isEmpty) {
                      //println("gets though second check")
                      newSetArgumentsCallChains = newControlFlowItem +: newSetArgumentsCallChains
                      callToCheck.wasExtended = true
                      stillChanging = true
                    }
                  }

                }
              }
            }
          }
        }
      }
      // println(s"items added = ${setArgumentsCallChains.filter(x => !x.wasExtended)}")
      newSetArgumentsCallChains = newSetArgumentsCallChains ++ setArgumentsCallChains.filter(x => !x.wasExtended)

      //println("!!!! finished loop once")
      setArgumentsCallChains = newSetArgumentsCallChains
      /*
      for(item <- setArgumentsCallChains){
        println( s"${item.methodCall} ${item.methodChain}")
      }*/
    }
    println("----------------------------------------------------")
    println("control chains")
    for (item <- setArgumentsCallChains) {
      println(s"${item.methodCall} ${item.methodChain}")
    }
    println("----------------------------------------------------")
    //would probably be a good idea to add a check that the class is a Fragment
    for (chain <- setArgumentsCallChains) {
      if (!FragmentLifecyleMethods.isMethodWhenFragmentInitialized(chain.methodCall.split("""\.""").last) &&
        !chain.methodChain.exists(x => FragmentLifecyleMethods.isMethodWhenFragmentInitialized(x.split("""\.""").last))) {
        val errorString = "@@@@ Found a problem: getActivity may be called when " +
          "the Fragment is not attached to an Activity" +
          s"call sequence ${chain.methodCall} ${chain.methodChain}"
        println(errorString)
        System.out.flush()
        System.err.println(errorString)
        System.err.flush()
        problemCount += 1
      }
    }
    println(s"total number of caught problems: ${problemCount}")
  }
  */
                //the code above was temporarilty commented out while I checked something
//This was code copied from another checker to use as an example
    /*
    for(cl:SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      //println(s"class: ${cl.getName}")
      for (m: SootMethod <- cl.getMethods().asScala) {
        //println(s"method: ${m.getName}")
        if (m.isConcrete && m.hasActiveBody) {
          println("new method")
          println(s"class: ${m.getDeclaringClass.getName} method: ${m.getName}")
          if(m.getName.contains("$")){
            println("stop for debugging")
          }
          for (stmt <- m.getActiveBody.getUnits.asScala) {
            //m.getActiveBody.getParameterRefs.indexOf(0).
            println(stmt)
            //determine the class of the first tab and make sure that class is not added twice
          }


          println(s"${m.getName()} matches displayActivityTitle ${m.getName.contains("displayActivityTitle")}")
          if (m.getName().contains("displayActivityTitle")) {
            val calledByList = Scene.v().getCallGraph().edgesInto(m)
            //println(s"size of calledByList: ${calledByList}")
            for (call: Edge <- calledByList.asScala) {
              println(s"source of edge: ${call.getSrc}")
              println(s"target of edge: ${call.getTgt}")
              println("")
            }

          }
        }

        def superClassIsActionBarTabListener(c: SootClass): Boolean = {
          //I was going to make this method not application specific but FlowDroid seems to
          //fail to be able to get the parent class of a nested class, even when the
          //parent class is declared in the file. I might have to add this functionality myself
          //if (c.getName().contains("ActionBar.TabListener")) {
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
            if (stmt.toString().contains(":= @this")) {
              thisVariableName = stmt.toString().split(" ")(0)
            }
            if (thisVariableName != "" && stmt.toString().contains(thisVariableName)) {
              if (stmt.toString().contains("android.app.Fragment")) {
                fragmentVariableName = stmt.toString().split(" ")(0)
              }
            }
            if (statementToLookFor matches stmt.toString()) {
              //this next check might be better if it checked if the fragmentVariableName was used in the
              //parameter list. But due to the typing constraints, I don't think the fragmentVariableName
              //can be anywhere else, so I'd have to see more examples to determine if I am right or not
              if (fragmentVariableName != "" && stmt.toString().contains(fragmentVariableName)) {
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


    if(tabsAreAdded && tabsAreHidden){
      System.err.print(possibleErrorString)
      println(s"total number of problems: ${possibleProblemCount}")
    }
  }
  */
  * */
