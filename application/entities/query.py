from logica.compiler.rule_translate import RuleCompileException
from logica.compiler.universe import LogicaProgram
from logica.parser_py.parse import ParseFile, ParsingException

from application.models import Query


def parse_query(query_text):
    return ParseFile(query_text)


def compile_to_sql(engine, query: Query):
    logica_query = query.query_text
    predicate = query.predicate
    engine = f'@Engine("{engine}");'
    try:
        parsed_query = parse_query(engine + logica_query)["rule"]
        return {"status": "COMPILED", "sql": LogicaProgram(parsed_query).FormattedPredicateSql(predicate)}
    except (ParsingException, RuleCompileException) as err:
        return {"status": "FAILED", "sql": err.args[0]}
