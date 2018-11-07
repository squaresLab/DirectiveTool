import scala.collection.immutable.HashMap

class RelevantStateMap {

  var relevantStates = new HashMap[String,Boolean]()

  def addState(stateName: String, validState: Boolean): RelevantStateMap = {
    relevantStates += (stateName -> validState)
    this
  }

  /*return either the invalid states or the an empty list if all states are valid.
  or would we rather return true or false and not keep track of the invalid states? - change later if necessary
   */
  def checkIfAnyStateInvalid(states: List[String]) = {

  }


}
