package analysis

import org.xmlpull.v1.XmlPullParserException
import java.io.IOException
import java.security.KeyStore.TrustedCertificateEntry
import java.util

import soot.jimple.Stmt
import soot.{PhaseOptions, Scene, SootClass, SootMethod}
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.SetupApplication
import soot.jimple.infoflow.solver.cfg.InfoflowCFG
import soot.jimple.toolkits.ide.icfg.OnTheFlyJimpleBasedICFG
import soot.options.Options

import scala.collection.JavaConverters._

object DetectInvalidInflateCallMain {
  @throws[IOException]
  @throws[XmlPullParserException]
  def main(args: Array[String]): Unit = { // Initialize Soot
    runAnalysis(args)
  }

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
    analyzer.getConfig.getAnalysisFileConfig.setSourceSinkFile("./SourcesAndSinks.txt")
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
    for (m <- Scene.v().getClasses(2).asScala){
      if (m.toString.startsWith("com"))
        println(m.toString)
    }
    println("")
    println("entry points")
    for (m <- Scene.v().getEntryPoints.asScala){
      println(m)
    }

     */
    val cfg = new InfoflowCFG(new OnTheFlyJimpleBasedICFG(Scene.v().getEntryPoints()));
    var problemCount = 0
    /*
    for (edge <- Scene.v().getCallGraph.iterator().asScala){
      println(s"source: + ${edge.getSrc.method().getDeclaringClass.getName} ${edge.getSrc.method.getName}")
      for (uBox <- edge.getSrc.method().retrieveActiveBody().getAllUnitBoxes.asScala){
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

   println("printing cfg")
/*    for( entry <- Scene.v().getReachableMethods.listener().asScala){
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
    println("printing bodies")
*/

     */
    for (cl: SootClass <- Scene.v().getClasses(SootClass.BODIES).asScala) {
      //println(s"class: ${cl.getName}")
      /*if (cl.getName().contains("FilmDetailsFragment")){
        println(cl.getName())
        println("running sub class with print")
        println(!DetectionUtils.classIsSubClassOfDialogFragment(cl))
      }*/
      if (DetectionUtils.classIsSubClassOfFragment(cl) && !DetectionUtils.classIsSubClassOfDialogFragment(cl)) {
        //println(s"****${cl.getName()} is subclass of Fragment")
        for (m: SootMethod <- cl.getMethods().asScala) {
          //println(s"method: ${m.getName}")
          /*if (cl.getName == "com.example.android.lnotifications.OtherMetadataFragment" && m.getName == "onCreateView") {
            println("here")
            println(s"is concrete: ${m.isConcrete}")
            println(s"has active body: ${m.hasActiveBody}")
          }*/
          if (m.isConcrete && m.hasActiveBody) {
            if (m.getName.contains("onCreateView")) {
              var hasNoFalse = false
              var isReturned = false
              var returnedItem: Option[String] = None
              //println("new method")
              //println(s"class: ${m.getDeclaringClass.getName} method: ${m.getName}")
              for (stmt <- m.getActiveBody.getUnits.asScala) {
                println(stmt)
                if (stmt.toString().contains("android.view.LayoutInflater: android.view.View inflate(")) {
                  // 0 is how soot stores the final false parameter
                  if (!stmt.toString().endsWith("0)")) {
                    hasNoFalse = true
                    if (stmt.toString().startsWith("return ")) {
                      isReturned = true
                    } else if (stmt.toString().contains("=")) {
                      returnedItem = Some(stmt.toString().replaceAll(" ", "").split("=")(0))
                    }
                  }
                }
                if (stmt.toString().startsWith("return ") && returnedItem.isDefined) {
                  if (stmt.toString().contains(returnedItem.get)) {
                    isReturned = true
                  }
                }
              }
              if (isReturned && hasNoFalse) {
                isReturned = false
                hasNoFalse = false
                println("start of call chain")
                //at the moment, the whole call chain isn't needed, just the failing method
                println(s"${m.toString}   ${m.getDeclaringClass.toString}")
                println("end of call chain")
                //The two classes that are printed here are often the same class
                // - I don't remember when they are different; maybe the two should be replaced with one
                println("@@@@@ Found a problem: inflate is missing the false parameter in onCreateView in class " + m.getDeclaringClass.getName + " in file of class: " + cl.toString)
                System.out.flush()
                System.err.println("@@@@@ Found a problem: inflate is missing the false parameter in onCreateView in class " + m.getDeclaringClass.getName + " in file of class: " + cl.toString)
                System.err.flush();
                problemCount = problemCount + 1
              }
            }
          }
        }
      }
    }
    println(s"total number of caught problems: ${problemCount}")
    val totalTime = System.nanoTime() - startTime
    println(s"total time (in nanoseconds): ${totalTime}")
    println(s"total time (in seconds): ${totalTime / 1000000000}")

    //println(s"main method of scene: ${Scene.v().getMainMethod}")

    // Iterate over the callgraph
    /* println("printing callgraph")
     val callGraph = Scene.v.getCallGraph
     //val callGraph = cfg.
     println(s"size of call graph: ${callGraph.size()}")
     for (edge <- Scene.v.getCallGraph.iterator.asScala) {
       val smSrc = edge.src
       val uSrc = edge.srcStmt
       val smDest = edge.tgt
       println(s"Edge from ${uSrc} in ${smSrc} to ${smDest}")
     }
     */
    /*val lifecycleMethods = AndroidEntryPointConstants.getActivityLifecycleMethods
    for( l <- lifecycleMethods){
      cfg.
    }*/
  }


}


