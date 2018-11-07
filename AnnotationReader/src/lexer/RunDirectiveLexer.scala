package lexer

import scala.io.Source

object RunDirectiveLexer extends App {
  val stateInputString = Source.fromFile("testStateInput.txt").mkString
  println(stateInputString)
  val output = DirectiveLexer(stateInputString)
  println(output)
}