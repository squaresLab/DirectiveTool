import java.util

import soot.{SootMethod, ValueBox}
import soot.jimple.SpecialInvokeExpr
import soot.jimple.internal._
import soot.toolkits.graph.UnitGraph
import soot.toolkits.scalar.ForwardFlowAnalysis
import scala.collection.JavaConverters._
import scala.collection.mutable

//TODO: test this
class SetSelectorSetPackageAnalysis(graph: UnitGraph) extends ForwardFlowAnalysis[soot.Unit, SetSelectorSetPackageAnalysis.AnalysisInfo](graph) {
  var numberOfCaughtProblems = 0
  doAnalysis()
  //println("setting number of caught problems to 0")
  /**
    * Given the merge of the <code>out</code> sets, compute the <code>in</code> set for <code>s</code> (or in to out,
    * depending on direction).
    *
    * This function often causes confusion, because the same interface is used for both forward and backward flow analyses.
    * The first parameter is always the argument to the flow function (i.e. it is the "in" set in a forward analysis and the
    * "out" set in a backward analysis), and the third parameter is always the result of the flow function (i.e. it is the
    * "out" set in a forward analysis and the "in" set in a backward analysis).
    *
    * @param in
    * the input flow
    * @param d
    * the current node
    * @param out
    * the returned flow
    **/
  override protected def flowThrough(in: SetSelectorSetPackageAnalysis.AnalysisInfo, d: soot.Unit, out: SetSelectorSetPackageAnalysis.AnalysisInfo): Unit = {
    val possibleM = DetectionUtils.extractMethodCallInStatement(d)
    if(possibleM.isDefined){
      copy(in,out)
      //this could throw an error for Intents
      possibleM.get.getDeclaringClass.getName.contains("Intent")
      val methodName = possibleM.get.getName
      //we know we can cast d to a Stmt because extractMethodCallInStatement did not return false
      //d.asInstanceOf[soot.jimple.Stmt].
      //  (soot.jimple.Stmt)d
      //println(s"method to check ${methodName}")
      for(ub <- d.getUseBoxes.asScala) {
        ub match {
          case vb: ValueBox =>
            val valueName = vb.getValue.toString()
            //println("found value box")
            if (methodName.contains("setSelector")) {
              //println("found setSelector")
              val varInfoOption = out.getVar(valueName)
              if (varInfoOption.isDefined) {
                varInfoOption.get.hasSetSelector = true
                checkForViolation(varInfoOption.get)
                //println(s"var option info: hasSetSelector: ${varInfoOption.get.hasSetSelector}, hasSetPackage ${varInfoOption.get.hasSetPackage}")
              }
              else {
                out.addVar(valueName, true, false)
              }

            } else if (methodName.contains("setPackage")) {
              //println("found setPackage")
              val varInfoOption = out.getVar(valueName)
              if (varInfoOption.isDefined) {
                varInfoOption.get.hasSetPackage= true
                checkForViolation(varInfoOption.get)
              }
              else {
                out.addVar(valueName, false, true)
              }
            }
          case _ => ()
        }
      }
    } else {
      copy(in,out)
    }
  }

  /**
    * Returns the flow object corresponding to the initial values for each graph node.
    */
  override protected def newInitialFlow(): SetSelectorSetPackageAnalysis.AnalysisInfo = {
    return new SetSelectorSetPackageAnalysis.AnalysisInfo();
  }

  /**
    * Compute the merge of the <code>in1</code> and <code>in2</code> sets, putting the result into <code>out</code>. The
    * behavior of this function depends on the implementation ( it may be necessary to check whether <code>in1</code> and
    * <code>in2</code> are equal or aliased ). Used by the doAnalysis method.
    */
  override protected def merge(in1: SetSelectorSetPackageAnalysis.AnalysisInfo, in2: SetSelectorSetPackageAnalysis.AnalysisInfo, out: SetSelectorSetPackageAnalysis.AnalysisInfo): Unit = {
    out.clear()
    for (variable <- in1.varMap.keySet){
      if (in2.varMap.contains(variable)){
        out.addVar(variable, (in1.varMap(variable).hasSetSelector.||(in2.varMap(variable).hasSetSelector)),(in1.varMap(variable).hasSetPackage.||(in2.varMap(variable).hasSetPackage)))
        checkForViolation(out.getVar(variable).getOrElse(null))
      } else {
        out.addVar(variable, in1.varMap(variable).hasSetSelector, in1.varMap(variable).hasSetPackage)
      }
    }
    for(variable <- in2.varMap.keySet) {
      if (!out.varMap.contains(variable)) {
        out.addVar(variable, in2.varMap(variable).hasSetSelector, in2.varMap(variable).hasSetPackage)
      }
    }
  }

  /** Creates a copy of the <code>source</code> flow object in <code>dest</code>. */
  override protected def copy(source: SetSelectorSetPackageAnalysis.AnalysisInfo, dest: SetSelectorSetPackageAnalysis.AnalysisInfo): Unit = {
    dest.varMap = source.varMap
  }

  def checkForViolation(d: SetSelectorSetPackageAnalysis.DirectiveInfo): Boolean = {
    if (d== null){
      return false
    }
    if(d.hasSetPackage.&&(d.hasSetSelector)){
      Predef.println("error: code calls both setSelector and setPackage on the same intent")
      numberOfCaughtProblems += 1
      println(s"number of caught problems: ${numberOfCaughtProblems}")
      return true
    }
    return false
  }

  def getCaughtProblems(): Int = {
    return numberOfCaughtProblems
  }
}

object SetSelectorSetPackageAnalysis {

  class DirectiveInfo(var hasSetSelector: Boolean = false, var hasSetPackage: Boolean = false){

  }
  class AnalysisInfo(var varMap: mutable.HashMap[String, DirectiveInfo] = new mutable.HashMap[String, DirectiveInfo]()){ //extends java.util.BitSet{

    def addVar(varName:String, hasSetSelector: Boolean = false, hasSetPackage:Boolean = false): Unit ={
      varMap.+=(varName -> new DirectiveInfo(hasSetSelector,hasSetPackage))
    }

    def getVar(varName: String): Option[DirectiveInfo] = {
      if (varMap.contains(varName)){
        return new Some(varMap(varName))
      } else {
        return None
      }
    }

    def clear(): Unit = {
      varMap = new mutable.HashMap[String,DirectiveInfo]()
    }


  }

}
