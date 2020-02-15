package analysis

import java.io.IOException

import org.xmlpull.v1.XmlPullParserException
import soot.jimple.Stmt
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.SetupApplication
import soot.jimple.infoflow.solver.cfg.InfoflowCFG
import soot.jimple.toolkits.ide.icfg.OnTheFlyJimpleBasedICFG
import soot.options.Options

import scala.collection.JavaConverters._
import scala.collection.mutable
import scala.collection.mutable.ListBuffer

object DetectInvalidGetResources {


  @throws[IOException]
  @throws[XmlPullParserException]
  def main(args: Array[String]): Unit = { // Initialize Soot
    runAnalysis(args)
  }

  def runAnalysis(args: Array[String]): Unit = {
    val startTime = System.nanoTime()
    System.setProperty(org.slf4j.impl.SimpleLogger.DEFAULT_LOG_LEVEL_KEY, "TRACE")
    //Scene.v().addBasicClass(android.util.Log, BODIES)
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
    analyzer.constructCallgraph()
    /*println("")
    println("scene classes")
    for (m <- Scene.v().getClasses(2).asScala) {
      if (m.toString.startsWith("com"))
        println(m.toString)
    }
     */
    /*println("")
    println("entry points")
    for (m <- Scene.v().getEntryPoints.asScala) {
      println(m)
    }
    */
    val cfg = new InfoflowCFG(new OnTheFlyJimpleBasedICFG(Scene.v().getEntryPoints()));
    var problemCount = 0
    /*
    for (edge <- Scene.v().getCallGraph.iterator().asScala) {
      println(s"source: + ${edge.getSrc.method().getDeclaringClass.getName} ${edge.getSrc.method.getName}")
      for (uBox <- edge.getSrc.method().retrieveActiveBody().getAllUnitBoxes.asScala) {
        uBox.getUnit() match {
          case stmt: Stmt =>
            println(stmt.toString())
          case x =>
            println(x.toString())
        }
      }
      println(s"target: + ${edge.getSrc.method().getDeclaringClass.getName} ${edge.getTgt.method.getName}")
      println("")
    }

     */

    // println("printing cfg")
    /*    for (entry <- Scene.v().getReachableMethods.listener().asScala) {
          entry match {
            case m: SootMethod =>
              if (DetectionUtils.isCustomClassName(m.getDeclaringClass.toString)) {
                println(s"calls for ${m}")
                for (call <- cfg.getCallsFromWithin(m).asScala) {
                  println(call)
                }
                println("")
              }
            case _ =>
              ()
          }
        }

     */

    /*    println("classes of interest")
        for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
          println(s"${cl}");
          if (cl.toString().contains("BackgroundTestFragment$ResourcesTask")){
            println("found the class of interest")
            println("methods in class:")
            for (m: SootMethod <- cl.getMethods().asScala) {
              println(m.getName())
            }
            println(s"outer class ${cl.getOuterClass.toString()}")
          }
          if (DetectionUtils.classIsSubClassOfAsyncTask(cl)) {
            println("is a subclass of asyncTask")
          }

        }
      */

    //    println("printing bodies")

    var classesToCheck = new ListBuffer[SootClass]
    for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      //println(s"class: ${cl.getName}")
      if (DetectionUtils.classIsSubClassOfAsyncTask(cl)) {
        for (m: SootMethod <- cl.getMethods().asScala) {
          //println(s"method: ${m.getName}")
          /*if (cl.getName == "com.example.android.lnotifications.OtherMetadataFragment" && m.getName == "onCreateView") {
            println("here")
            println(s"is concrete: ${m.isConcrete}")
            println(s"has active body: ${m.hasActiveBody}")
          }*/
          //println(s"looking at method : ${m}, is concrete: ${m.isConcrete()}, and active body: ${m.hasActiveBody}")
          if (m.isConcrete && m.hasActiveBody) {
            //if (m.getName.contains("onCreateView")) {
            //println("new method")
            //println(s"class: ${m.getDeclaringClass.getName} method: ${m.getName}")
            for (stmt <- m.getActiveBody.getUnits.asScala) {
              //println(stmt)
              //getOuterClassUnsafe returns null if no outer class exists while getOuterClass throws an exception
              if (stmt.toString().contains("android.content.res.Resources getResources()") && cl.getOuterClassUnsafe() != null && DetectionUtils.classIsSubClassOfFragment(cl.getOuterClass())) {
                //println("start of call chain")
                //at the moment, the whole call chain isn't needed, just the failing method
                classesToCheck += cl

              }
            }
          }
        }
      }
    }
    for (cl <- classesToCheck) {
      println(cl.toString)
      val methodNameToCheckFor = cl.toString
      var (startingMethod, calledByList) = analysis.DetectIncorrectGetActivityMain.getStartingMethodAndCallChain(methodNameToCheckFor)
      val checkingClasses = true
      var callChains: List[ControlFlowChain] = List()
      val fullCallChains: ListBuffer[ControlFlowChain] = new ListBuffer[ControlFlowChain]()
      if (startingMethod.isDefined) {
        analysis.DetectIncorrectGetActivityMain.createCallChainsDepthFirst(calledByList, fullCallChains, List[ControlFlowItem](new ControlFlowItem(startingMethod.get, checkingClasses)), methodNameToCheckFor, checkingClasses)
      }
      callChains = fullCallChains.toList
      var alreadyReportedErrors = new mutable.HashMap[String, Boolean]()
      for (chain <- callChains) {
        if (chain.controlChain.length > 0) {
          val controlChainLength = chain.controlChain.length
          //since we can't save the initalization as the method, use the method the initalization was declared in
          var controlItem = chain.controlChain(controlChainLength-1)
          println(alreadyReportedErrors)
          println(controlItem.methodCall.toString)
          if (!alreadyReportedErrors.contains(controlItem.methodCall.toString)) {
            if (!chain.controlChain.exists(call => FragmentLifecyleMethods.isMethodWhenGetResourcesWorks(call.methodCall)) &&
            chain.controlChain.exists(call => DetectionUtils.classIsSubClassOfFragment(call.methodCall.getDeclaringClass))) {
              alreadyReportedErrors += (chain.controlChain.reverse(0).methodCall.toString -> true)

              //val testString = chain.controlChain.slice(chain.controlChain.length - 2, chain.controlChain.length).toString()
              //            if (!foundControlFlowItemStrings.contains(testString)) {
              val errorString = "@@@@@ Found a problem: getResources may be called when " +
                "the Fragment is not attached to an Activity" +
                s": call sequence ${chain.controlChain}"
              println(errorString)
              //println(s"${m.toString}   ${m.getDeclaringClass.toString}")
              //println("end of call chain")
              //println(s"@@@@@ Found a problem: calling getResources on a background fragment in ${m.getName()} of ${cl.getName()} with outer Fragment class ${cl.getOuterClass.getName}")
              System.out.flush()
              //System.err.println(s"@@@@@ Found a problem: calling getResources on a background fragment in ${m.getName()} of ${cl.getName()} with outer Fragment class ${cl.getOuterClass.getName}")
              System.err.println(errorString)
              System.err.flush()
              problemCount = problemCount + 1
              //foundControlFlowItemStrings += s"List(${m.toString()}, <android.app.Fragment: void setArguments(android.os.Bundle)>)"
            }
          }
        }
      }
    }
    println(s"total number of caught problems: ${problemCount}")
    val totalTime = System.nanoTime() - startTime
    println(s"total time (in nanoseconds): ${totalTime}")
    println(s"total time (in seconds): ${totalTime / 1000000000}")
  }
}
