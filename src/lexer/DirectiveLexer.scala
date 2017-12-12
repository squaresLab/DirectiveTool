package lexer

import scala.util.parsing.combinator.RegexParsers

object DirectiveLexer extends RegexParsers {

  override def skipWhitespace: Boolean = true
  override val whiteSpace = "[ \t\r\f]".r

  def apply(code: String): Either[LexerError, List[DirectiveToken]] = {
    parse(tokens, code) match {
      case Failure(message, next) => Left(LexerError(Location(next.pos.line, next.pos.column), message+"\n"+next.rest.first))
      case Error(message, next) => Left(LexerError(Location(next.pos.line, next.pos.column), message+"\n"+next.rest.first))
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
        //NEW_LINE :: processIndentation(tokens.tail, indents)
        processIndentation(tokens.tail, indents)

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
    "[a-zA-Z][_a-zA-Z0-9]+".r ^^ { str => IDENTIFIER(str)}
  }

  def refIdentifier: Parser[REFERENCE_IDENTIFIER] = {
    "@[_a-zA-Z0-9]+".r ^^ { str => REFERENCE_IDENTIFIER(str)}
  }

  def objectMethodCall: Parser[METHOD_CALL] = {
    """[a-zA-Z][_a-zA-Z0-9]+\.[_a-zA-Z]+\(.*\)""".r ^^ { str =>
      val callInfo = str.split('.')
      METHOD_CALL(callInfo(0),callInfo(1))
    }
  }

  def indentation: Parser[INDENTATION] = positioned {
    "\n[ ]*".r ^^ { whitespace =>
      val nSpaces = whitespace.length - 1
      INDENTATION(nSpaces)
    }
  }



  def tokens: Parser[List[DirectiveToken]] = {
    phrase(rep1(colon | equals | comma | or | and | leftAngleBracket | rightAngleBracket|
      binaryState | statesHeader |  period | indentation | directiveHeader | allowWhen |
      require | in | not | objectMethodCall | identifier | refIdentifier )) ^^
    { rawTokens => processIndentation(rawTokens)}
  }

  def colon = positioned {":"                   ^^ {_ => COLON}}
  def equals = positioned {"="                  ^^ {_ => EQUALS}}
  def comma = positioned {","                   ^^ {_ => COMMA}}
  def period = positioned{"."                   ^^ {_ => PERIOD}}
  def statesHeader = positioned { "States:"     ^^ {_ => STATES_HEADER}}
  def or = positioned { "or"                    ^^ {_ => OR}}
  def and = positioned{ "and"                   ^^ {_ => AND}}
  def leftAngleBracket = positioned {"<"        ^^ {_ => LEFT_ANGLE_BRACKET}}
  def rightAngleBracket = positioned { ">"      ^^ {_ => RIGHT_ANGLE_BRACKET}}
  def binaryState = positioned { "Binary-state" ^^ {_ => BINARY_STATE}}
  def directiveHeader = positioned { "Directives:" ^^ {_ => DIRECTIVE_HEADER}}
  def allowWhen = positioned {"allow-when"      ^^ {_ => ALLOW_WHEN}}
  def require = positioned{"require"            ^^ {_ => REQUIRE}}
  def in = positioned{"in"                      ^^ {_ => IN}}
  def not = positioned{"not"               ^^ {_ => NOT}}
}
