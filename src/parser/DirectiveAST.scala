package parser

import java.nio.file.DirectoryIteratorException

import scala.util.parsing.input.Positional

sealed trait DirectiveAST extends Positional

//not sure if the StateGroup is correct but putting it here for now; I'll
//determine if it is correct later
//sealed trait StateGroup
case class AndThen(block1: DirectiveAST, block2: DirectiveAST) extends DirectiveAST
case class StateInfo(block1: DirectiveAST, block2: DirectiveAST) extends DirectiveAST
case class ObjectInfo(block1: DirectiveAST, block2: DirectiveAST) extends DirectiveAST
case class Object(name: String) extends DirectiveAST
case class OrthogonalStateGroups(state1: StateName, state2: DirectiveAST) extends DirectiveAST
case class PermutedStateGroups(state1: StateName, state2: DirectiveAST) extends DirectiveAST
case class BinaryStateGroup(stateName: StateName, parentState: StateName, stateGroup: List[DirectiveAST]) extends DirectiveAST
case class ObjectAssignment(objectName: String) extends DirectiveAST
case class StateGroupAssignment(stateName: StateName, subStates: List[DirectiveAST]) extends DirectiveAST
case class StateName(name: String) extends DirectiveAST
case object StateHeader extends DirectiveAST
case object Test extends DirectiveAST
case object NewLine extends DirectiveAST
case object IndentItem extends DirectiveAST
case object DedentItem extends DirectiveAST

