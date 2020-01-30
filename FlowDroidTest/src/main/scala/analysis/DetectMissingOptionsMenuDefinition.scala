package analysis

import analysis.DetectMissingSetHasOptionsMenu.buildAnalysis
import soot.jimple.infoflow.InfoflowConfiguration
import soot.jimple.infoflow.InfoflowConfiguration.{CallgraphAlgorithm, ImplicitFlowMode}
import soot.jimple.infoflow.android.InfoflowAndroidConfiguration.CallbackAnalyzer
import soot.jimple.infoflow.android.SetupApplication
import soot.options.Options
import soot.{PhaseOptions, Scene, SootClass, SootMethod}

import scala.collection.JavaConverters._

object DetectMissingOptionsMenuDefinition {

  def main(args: Array[String]): Unit = {
    val fullAnalysis = DetectMissingSetHasOptionsMenu.buildAnalysis(checkForProblem)
    fullAnalysis(args)
  }

  def runAnalysis(args: Array[String]): Unit = {
    val fullAnalysis = buildAnalysis(checkForProblem)
    fullAnalysis(args)

  }

  def checkForProblem(problemCount: Int, cl: SootClass, containsHasSetOptionsMenu: Boolean, containsOnCreateOptionsMenu: Boolean): Int = {
    var newProblemCount = problemCount
    if (containsHasSetOptionsMenu && !containsOnCreateOptionsMenu) {
      val errorString = "@@@@ Found a problem: onCreateOptionMenu must " +
        s"be overridden in ${cl.getName} to display the OptionsMenu"
      newProblemCount = DetectMissingSetHasOptionsMenu.notifyOfProblem(problemCount, cl.getName, errorString)

    }
    return newProblemCount
  }
}

