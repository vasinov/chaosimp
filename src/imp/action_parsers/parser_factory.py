from action_parsers.imp_run_script_parser import *


def to_action_parser(data):
    if data['type'] == "imp:run-script":
        return ImpRunScriptParser(data["name"], data["path"])
