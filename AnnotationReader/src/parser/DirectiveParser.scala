package parser

import lexer._
import lexer.DirectiveToken

import scala.util.parsing.combinator.Parsers
import scala.util.parsing.input.{NoPosition, Position, Reader}


object DirectiveParser extends Parsers{
  override type Elem = DirectiveToken

  class TokenReader(tokens: Seq[DirectiveToken]) extends Reader[DirectiveToken] {
    override def first: DirectiveToken = tokens.head
    override def atEnd: Boolean = tokens.isEmpty
    override def pos: Position = tokens.headOption.map(_.pos).getOrElse(NoPosition)
    override def rest: Reader[DirectiveToken] = new TokenReader(tokens.tail)
  }

/*  def filterUnimportantIndentation(tokens: Seq[DirectiveToken]): Seq[DirectiveToken] = {
    def recursiveFilterIndentation(head: DirectiveToken, tail: Seq[DirectiveToken]): Seq[DirectiveToken] = {
      match (head, tail.head) {
        //case (i: INDENT.type, d: DEDENT.type) => Seq[DirectiveToken]
        //case (d: DEDENT.type, i: INDENT.type) => Seq[DirectiveToken]
        //case _ =>  Seq[DirectiveToken]
      }
    }
  }
  */

  def apply(tokens: Seq[DirectiveToken]): Either[ParserError, DirectiveAST] = {
    val reader = new TokenReader(tokens)
    program(reader) match {
      case NoSuccess(msg, next) => Left(ParserError(Location(next.pos.line, next.pos.column), msg + "\n" + next.rest.first))
      case Success(result, _) => Right(result)
    }
  }

  def program: Parser[DirectiveAST] = positioned {
    phrase(block)
  }

  def block: Parser[DirectiveAST] = positioned {
    rep1(stateBlock) ^^ { case stmtList => stmtList reduceRight AndThen}
  }

  def stateBlock: Parser[DirectiveAST] = positioned {
    val stateHeader = STATES_HEADER ^^ (_ => StateHeader)
    val newLine = NEW_LINE ^^ (_ => NewLine)
    val indent = INDENT ^^ (_ => IndentItem)
    val dedent = DEDENT ^^ (_ => DedentItem)
    val objectInfo = (identifier~COLON~stateCombination) ^^ {
      case (IDENTIFIER(objectName) ~ _ ~ stateEquation ) => ObjectInfo(Object(objectName),stateEquation)
    }
    val stateListAssignment = (identifier~EQUALS~stateList) ^^ {
      case (IDENTIFIER(state)~_~stateGroup)=> StateGroupAssignment(StateName(state),stateGroup)
    }
    val binaryStateAssignment = (BINARY_STATE ~ identifier ~ LEFT_ANGLE_BRACKET ~ identifier ~ RIGHT_ANGLE_BRACKET ~ EQUALS ~ stateList ) ^^ {
      case (_ ~ IDENTIFIER(bName) ~ _ ~ IDENTIFIER(parentState) ~ _ ~ EQUALS ~ stateGroup) => BinaryStateGroup(StateName(bName),StateName(parentState), stateGroup)
    }
    stateHeader | objectInfo |  stateListAssignment | newLine | binaryStateAssignment | indent | dedent
  }

  def stateList: Parser[List[DirectiveAST]] = {
    repsep(identifier, COMMA) ^^ { case stateItems => stateItems.map {
      case IDENTIFIER(name) => StateName(name)
      }
    }
  }


  def stateCombination: Parser[DirectiveAST] = positioned {
    /* val andStatement = (identifier ~ AND ~ stateCombination) ^^ {
      //decide if you want PermutedStateGroups to be two ASTs or one list
      case (IDENTIFIER(name) ~ _ ~ combinationResult) => PermutedStateGroups(StateName(name), combinationResult)
    }
    val orStatement = (identifier ~ OR ~ stateCombination) ^^ {
      case (IDENTIFIER(name) ~ _ ~ combinationResult) => OrthogonalStateGroups(StateName(name), combinationResult)
    }
    //also figure out how to make the identifier type match
    //maybe by creating an AST node for identifiers
    andStatement | orStatement | stateId
    */
    identifier ~ rep( ((AND ~ identifier) | (OR ~ identifier))) ^^ {
      case IDENTIFIER(name) ~ itemList => (itemList foldLeft[DirectiveAST] StateName(name)) {
        case (acc, AND ~ IDENTIFIER(name)) => PermutedStateGroups(StateName(name), acc)
        case (acc, OR ~ IDENTIFIER(name)) => OrthogonalStateGroups(StateName(name), acc)
      }
    }
  }

  def identifier: Parser[IDENTIFIER] = positioned {
    accept("identifier", {case id @ IDENTIFIER(name) => id})
  }

  def stateId: Parser[StateName] = positioned {
    identifier ^^ {case IDENTIFIER(name) => StateName(name)}
  }
}
