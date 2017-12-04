package lexer

import scala.util.parsing.input.Positional

sealed trait DirectiveToken extends Positional

case class IDENTIFIER(str: String) extends DirectiveToken
//case class LITERAL(str: String) extends DirectiveToken
case class INDENTATION(spaces: Int) extends DirectiveToken
case object EMPTY_LINE extends DirectiveToken
case object NEW_LINE extends DirectiveToken
case object STATES_HEADER extends DirectiveToken
case object OR extends DirectiveToken
case object AND extends DirectiveToken
case object INDENT extends DirectiveToken
case object DEDENT extends DirectiveToken
case object COLON extends DirectiveToken
case object EQUALS extends DirectiveToken
case object COMMA extends DirectiveToken
case object LEFT_ANGLE_BRACKET extends DirectiveToken
case object RIGHT_ANGLE_BRACKET extends DirectiveToken
case object BINARY_STATE extends DirectiveToken
