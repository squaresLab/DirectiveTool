package lexer

import scala.util.parsing.combinator.RegexParsers

object DirectiveLexer extends RegexParsers {

  override def skipWhitespace: Boolean = true
  override val whiteSpace = "[ \t\r\f]".r

  def apply(code: String): Either[LexerError, List[DirectiveToken]] = {
    parse(tokens, code) match {
      case Failure(message, next) => Left(LexerError(Location(next.pos.line, next.pos.column), message))
      case Error(message, next) => Left(LexerError(Location(next.pos.line, next.pos.column), message))
      case Success(result, _) => Right(result)
    }
  }

  private def processIndentation(tokens: List[DirectiveToken], indents: List[Int] = List(0)): List[DirectiveToken] = {
    tokens.headOption match {

      //if there is an increase in the indentation level, we save the new level and
      //produce an INDENT AST item
      case Some(INDENTATION(spaces)) if spaces > indents.head =>
        INDENT :: processIndentation(tokens.tail, spaces :: indents)

      //if there is a decrease, we pop from the stack util we have matched the new
      //level and we produce a DEDENT for each saved INDENT
      case Some(INDENTATION(spaces)) if spaces < indents.head =>
        val (dropped, kept) = indents.partition(_ > spaces)
        (dropped map (_ => DEDENT)) ::: processIndentation(tokens.tail, kept)


      // if the indentation level stays unchanged, no tokens are produced
      case Some(INDENTATION(spaces)) if spaces == indents.head =>
        NEW_LINE :: processIndentation(tokens.tail, indents)

      //other tokens are ignored
      case Some(token) =>
        token :: processIndentation(tokens.tail, indents)

      //the final step is to produce a DEDENT for indentation level still remaining,
      //thus closing the remaining open INDENTS
      case None =>
        indents.filter(_ > 0).map(_ => DEDENT)
    }
  }

  def identifier: Parser[IDENTIFIER] = {
    "[a-zA-Z][_a-zA-Z1-9]+".r ^^ { str => IDENTIFIER(str)}
  }

  def indentation: Parser[INDENTATION] = positioned {
    "\n[ ]*".r ^^ { whitespace =>
      val nSpaces = whitespace.length - 1
      INDENTATION(nSpaces)
    }
  }



  def tokens: Parser[List[DirectiveToken]] = {
    phrase(rep1(colon | equals | comma | or | and | leftAngleBracket | rightAngleBracket| binaryState | statesHeader | indentation | identifier)) ^^
    { rawTokens => processIndentation(rawTokens)}
  }

  def colon = positioned {":"                   ^^ {_ => COLON}}
  def equals = positioned {"="                  ^^ {_ => EQUALS}}
  def comma = positioned {","                   ^^ {_ => COMMA}}
  def statesHeader = positioned { "States:"     ^^ {_ => STATES_HEADER}}
  def or = positioned { "or"                    ^^ {_ => OR}}
  def and = positioned{ "and"                   ^^ {_ => AND}}
  def leftAngleBracket = positioned {"<"        ^^ {_ => LEFT_ANGLE_BRACKET}}
  def rightAngleBracket = positioned { ">"      ^^ {_ => RIGHT_ANGLE_BRACKET}}
  def binaryState = positioned { "binary-state" ^^ {_ => BINARY_STATE}}
}
