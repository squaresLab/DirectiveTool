package lexer

sealed trait CompilerError

case class LexerError(location: Location, message: String) extends CompilerError
case class ParserError(location: Location, message: String) extends CompilerError

case class Location(line: Int, column: Int) {
  override def toString: String = s"$line:$column"
}
