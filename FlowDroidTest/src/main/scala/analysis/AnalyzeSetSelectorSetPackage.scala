package analysis

import java.util

import soot.{SootMethod, ValueBox}
import soot.jimple.SpecialInvokeExpr
import soot.jimple.internal._
import soot.toolkits.graph.UnitGraph
import soot.toolkits.scalar.ForwardFlowAnalysis
import scala.collection.JavaConverters._
import scala.collection.mutable

//TODO: check this analysis. I wasn't checking only intent variables earlier. Now I am but I havne't
//tested the change yet.
class AnalyzeSetSelectorSetPackage(graph: UnitGraph) extends ForwardFlowAnalysis[soot.Unit, AnalyzeSetSelectorSetPackage.AnalysisInfo](graph) {
  var numberOfCaughtProblems = 0
  //The analysis seems to get stuck on multiple case statements in a function, so ending the analysis early in that case
  val endTime = System.currentTimeMillis + 300 * 1000 // 60 seconds * 1000 ms/sec
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
  override protected def flowThrough(in: AnalyzeSetSelectorSetPackage.AnalysisInfo, d: soot.Unit, out: AnalyzeSetSelectorSetPackage.AnalysisInfo): Unit = {
    if(System.currentTimeMillis() > endTime){
      throw new RuntimeException("analysis timed out")
    }
    //println("in flow through")
    val possibleM = DetectionUtils.extractMethodCallInStatement(d)
    if(possibleM.isDefined){
      copy(in,out)
      //this could throw an error for Intents
      if(possibleM.get.getDeclaringClass.getName.contains("Intent")) {
        val methodName = possibleM.get.getName
        //we know we can cast d to a Stmt because extractMethodCallInStatement did not return false
        //d.asInstanceOf[soot.jimple.Stmt].
        //  (soot.jimple.Stmt)d
        //println(s"method to check ${methodName}")
        for (ub <- d.getUseBoxes.asScala) {
          ub match {
            case vb: ValueBox =>
              val valueName = vb.getValue.toString()
              //println("found value box")
              if (methodName.contains("setSelector") && !d.toString().endsWith("null)")) {
                //println(s"found setSelector with ${valueName}: ${d.toString()}")
                //println(s"${possibleM.get.}")
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

              } else if (methodName.contains("setPackage") && !d.toString().endsWith("null)")) {
                //println(s"found setPackage with ${valueName}: ${d.toString()}")
                //println("found setPackage")
                val varInfoOption = out.getVar(valueName)
                if (varInfoOption.isDefined) {
                  varInfoOption.get.hasSetPackage = true
                  checkForViolation(varInfoOption.get)
                }
                else {
                  out.addVar(valueName, false, true)
                }
              }
            case _ => ()
          }
        }
      }
    } else {
      copy(in,out)
    }
  }

  /**
    * Returns the flow object corresponding to the initial values for each graph node.
    */
  override protected def newInitialFlow(): AnalyzeSetSelectorSetPackage.AnalysisInfo = {
    return new AnalyzeSetSelectorSetPackage.AnalysisInfo();
  }

  /**
    * Compute the merge of the <code>in1</code> and <code>in2</code> sets, putting the result into <code>out</code>. The
    * behavior of this function depends on the implementation ( it may be necessary to check whether <code>in1</code> and
    * <code>in2</code> are equal or aliased ). Used by the doAnalysis method.
    */
  override protected def merge(in1: AnalyzeSetSelectorSetPackage.AnalysisInfo, in2: AnalyzeSetSelectorSetPackage.AnalysisInfo, out: AnalyzeSetSelectorSetPackage.AnalysisInfo): Unit = {
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
  override protected def copy(source: AnalyzeSetSelectorSetPackage.AnalysisInfo, dest: AnalyzeSetSelectorSetPackage.AnalysisInfo): Unit = {
    dest.varMap = source.varMap.clone()
  }

  def checkForViolation(d: AnalyzeSetSelectorSetPackage.DirectiveInfo): Boolean = {
    if (d== null){
      return false
    }
    if(numberOfCaughtProblems != 1 && d.hasSetPackage.&&(d.hasSetSelector)){
      Predef.println("error: code calls both setSelector and setPackage on the same intent")
      //just determine if there is an error - earlier I was trying to count all errors and
      //I was getting the number of control flow paths that included the error instead.
      //Since this analysis only checks one method at a time, we only throw an error per
      //method call
      numberOfCaughtProblems = 1
      println(s"number of caught problems: ${numberOfCaughtProblems}")
      return true
    }
    return false
  }

  def getCaughtProblems(): Int = {
    return numberOfCaughtProblems
  }
}

object AnalyzeSetSelectorSetPackage {

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

    override def equals(obj: Any): Boolean = {
      obj match {
        case ai: AnalysisInfo => {
          if(this.varMap.size != ai.varMap.size){
            return false
          }
          else {
            for ((varName,di) <- ai.varMap){
              if(!varMap.contains(varName)){
                return false
              } else {
                if(ai.varMap(varName).hasSetSelector != varMap(varName).hasSetSelector){
                  return false
                }
                if(ai.varMap(varName).hasSetPackage != varMap(varName).hasSetPackage){
                  return false
                }
              }
            }
            return true
          }
        }
        case _ => return false
      }
    }


  }

}
