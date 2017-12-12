package compilation

import lexer.{DirectiveLexer, DirectiveToken}
import parser.DirectiveParser

import scala.io.Source

object RunCompiler {

  def main(args: Array[String]): Unit = {
    val stateInputString = Source.fromFile("testStateInput.txt").mkString
    val lexerOutput = DirectiveLexer(stateInputString)
    println(lexerOutput)
    val printAST = (tokens: List[DirectiveToken]) => {
      val parserOutput = DirectiveParser(tokens)
      println(parserOutput)
    }
    lexerOutput match {
      case Right(tokens) => printAST(tokens)
      case Left(err) => println(err)
    }
  }

}
