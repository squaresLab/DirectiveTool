import java.util

import soot.{SootMethod, ValueBox}
import soot.jimple.SpecialInvokeExpr
import soot.jimple.internal._
import soot.toolkits.graph.UnitGraph
import soot.toolkits.scalar.{FlowSet, ForwardFlowAnalysis}

import scala.collection.JavaConverters._
import scala.collection.mutable

//TODO: made a change and need to test this again
class AnalyzeSetContentViewFindViewByIDOrdering(graph: UnitGraph) extends ForwardFlowAnalysis[soot.Unit, AnalyzeMethodOrdering.AnalysisInfo](graph) {
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
  override protected def flowThrough(in: AnalyzeMethodOrdering.AnalysisInfo, d: soot.Unit, out: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
    val possibleM = DetectionUtils.extractMethodCallInStatement(d)
    if(possibleM.isDefined){
      copy(in,out)
      val methodName = possibleM.get.getName
      println(s"${methodName}")
      if (methodName.contains("setContentView")) {
        println("found setContentView")
        out.di.hasMethod1 = true
      } else if (methodName.contains("findViewById")) {
        out.di.hasMethod2 = true
        println("found findViewById")
        checkForViolation(out)
      }
    } else {
      copy(in,out)
    }
  }

  /**
    * Returns the flow object corresponding to the initial values for each graph node.
    */
  override protected def newInitialFlow(): AnalyzeMethodOrdering.AnalysisInfo = {
    return new AnalyzeMethodOrdering.AnalysisInfo();
  }

  /**
    * Compute the merge of the <code>in1</code> and <code>in2</code> sets, putting the result into <code>out</code>. The
    * behavior of this function depends on the implementation ( it may be necessary to check whether <code>in1</code> and
    * <code>in2</code> are equal or aliased ). Used by the doAnalysis method.
    */
  override protected def merge(in1: AnalyzeMethodOrdering.AnalysisInfo, in2: AnalyzeMethodOrdering.AnalysisInfo, out: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
  }

  /** Creates a copy of the <code>source</code> flow object in <code>dest</code>. */
  override protected def copy(source: AnalyzeMethodOrdering.AnalysisInfo, dest: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
    dest.di.hasMethod2 = source.di.hasMethod2
    dest.di.hasMethod1 = source.di.hasMethod1
  }

  def checkForViolation(a: AnalyzeMethodOrdering.AnalysisInfo): Boolean = {
    if (a.di.hasMethod2 && !a.di.hasMethod1){
      numberOfCaughtProblems += 1
      return true
    }
    else {
      return false
    }
  }

  def getCaughtProblems(): Int = {
    return numberOfCaughtProblems
  }
}

object AnalyzeSetContentViewFindViewByIDOrdering{

  class DirectiveInfo (var hasSetContentView: Boolean = false, var hasFindViewByIdOrdering: Boolean = false){

  }
  class AnalysisInfo(){
    //has the path already called hasSetContentView or hasFindViewByIdOrdering
    val di: DirectiveInfo = new DirectiveInfo()

    def meet(other: AnalyzeMethodOrdering.AnalysisInfo): Unit = {
      return new DirectiveInfo(di.hasSetContentView && other.di.hasMethod1, di.hasFindViewByIdOrdering && other.di.hasMethod2)
    }
  }
  //I've decided I don't need a flow set for this case
  /*class AnalysisInfo extends FlowSet[DirectiveInfo](){ //extends java.util.BitSet{
    val d: DirectiveInfo = new DirectiveInfo()

    /**
      * returns an empty set, most often more efficient than: <code>((FlowSet)clone()).clear()</code>
      */
    override def emptySet(): FlowSet[DirectiveInfo] = {
      d.hasSetContentView = false
      d.hasFindViewByIDOrdering = false
      return this
    }

    /**
      * Copies the current FlowSet into dest.
      */
    override def copy(dest: FlowSet[DirectiveInfo]): Unit = {
      if(dest.isInstanceOf[AnalysisInfo]){
        val result = dest.asInstanceOf[AnalysisInfo]
        result.d.hasFindViewByIDOrdering = this.d.hasFindViewByIDOrdering
        result.d.hasSetContentView = this.d.hasSetContentView
        return result
      } else{
        return dest
      }

    }

    /**
      * Sets this FlowSet to the empty set (more generally, the bottom element of the lattice.)
      */
    override def clear(): Unit ={
      d.hasSetContentView = false
      d.hasFindViewByIDOrdering = false
    }

    /**
      * Returns the union (join) of this FlowSet and <code>other</code>, putting result into <code>this</code>.
      */
    override def union(other: FlowSet[DirectiveInfo]): Unit = {

    }

    /**
      * Returns the union (join) of this FlowSet and <code>other</code>, putting result into <code>dest</code>.
      * <code>dest</code>, <code>other</code> and <code>this</code> could be the same object.
      */
    override def union(other: FlowSet[DirectiveInfo], dest: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Returns the intersection (meet) of this FlowSet and <code>other</code>, putting result into <code>this</code>.
      */
    override def intersection(other: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Returns the intersection (meet) of this FlowSet and <code>other</code>, putting result into <code>dest</code>.
      * <code>dest</code>, <code>other</code> and <code>this</code> could be the same object.
      */
    override def intersection(other: FlowSet[DirectiveInfo], dest: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Returns the set difference (this intersect ~other) of this FlowSet and <code>other</code>, putting result into
      * <code>this</code>.
      */
    override def difference(other: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Returns the set difference (this intersect ~other) of this FlowSet and <code>other</code>, putting result into
      * <code>dest</code>. <code>dest</code>, <code>other</code> and <code>this</code> could be the same object.
      */
    override def difference(other: FlowSet[DirectiveInfo], dest: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Returns true if this FlowSet is the empty set.
      */
    override def isEmpty: Boolean = ???

    /**
      * Returns the size of the current FlowSet.
      */
    override def size(): Int = ???

    /**
      * Adds <code>obj</code> to <code>this</code>.
      */
    override def add(obj: DirectiveInfo): Unit = ???

    /**
      * puts <code>this</code> union <code>obj</code> into <code>dest</code>.
      */
    override def add(obj: DirectiveInfo, dest: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Removes <code>obj</code> from <code>this</code>.
      */
    override def remove(obj: DirectiveInfo): Unit = ???

    /**
      * Puts <code>this</code> minus <code>obj</code> into <code>dest</code>.
      */
    override def remove(obj: DirectiveInfo, dest: FlowSet[DirectiveInfo]): Unit = ???

    /**
      * Returns true if this FlowSet contains <code>obj</code>.
      */
    override def contains(obj: DirectiveInfo): Boolean = ???

    /**
      * Returns true if the <code>other</code> FlowSet is a subset of <code>this</code> FlowSet.
      */
    override def isSubSet(other: FlowSet[DirectiveInfo]): Boolean = ???

    /**
      * returns an iterator over the elements of the flowSet. Note that the iterator might be backed, and hence be faster in the
      * creation, than doing <code>toList().iterator()</code>.
      */
    override def iterator(): util.Iterator[DirectiveInfo] = ???

    /**
      * Returns an unbacked list of contained objects for this FlowSet.
      */
    override def toList: util.List[DirectiveInfo] = ???
  }
  */

}
