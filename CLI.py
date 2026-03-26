import re
import configparser

from Topology import Topology
from Interpreter import Interpreter
from Engine import Engine


config = configparser.ConfigParser()
config.read("config.ini")

topology = None
interpreter = None
engine = None


# ---------------- INIT ---------------- #

def init_engine():
    global config, topology, interpreter, engine

    if "Path" not in config:
        config["Path"] = {}
    if "Setting" not in config:
        config["Setting"] = {}

    config["Setting"].setdefault("threadNum", "32")
    config["Setting"].setdefault("batchSize", "-1")

    if not config["Path"].get("ASRelFilePath"):
        print("ASRelFilePath not set")
        return

    topology = Topology()
    interpreter = Interpreter()

    try:
        interpreter.loadRoutingInformation(config, topology)
    except Exception as e:
        print(f"Init failed: {e}")
        return

    engine = Engine(config)
    print("  Engine initialized")


# ---------------- RELOAD ---------------- #

def reload_data():
    global config, topology, interpreter

    if topology is None:
        print("  Run init first")
        return

    try:
        interpreter.loadRoutingInformation(config, topology)
        print("  Reloaded (state preserved)")
    except Exception as e:
        print(f"  Reload failed: {e}")


# ---------------- LOAD ---------------- #

def handle_load(cmd):
    match = re.match(r"load\s+(\w+)\s*=\s*(.+);", cmd)
    if not match:
        print("  Invalid load command")
        return

    key, value = match.group(1), match.group(2)

    if "Path" not in config:
        config["Path"] = {}

    config["Path"][key] = value
    print(f"Loaded {key} = {value}")
    print("⚠️ Use init; or reload;")


# ---------------- EXECUTE ---------------- #

def execute_command_block(block):
    global engine, topology

    if engine is None:
        print("  Run init first")
        return

    try:
        with open("temp_cli.txt", "w") as f:
            f.write(block)

        engine.parseDescriptionFile("temp_cli.txt", topology)

    except Exception as e:
        print(f"  Error: {e}")


# ---------------- VALIDATION ---------------- #

def is_valid_block_line(line):
    """
    Prevent garbage like 'sdf;' inside block
    """
    valid_patterns = [
        r"AS \d+ peer AS \d+",
        r"filter in",
        r"filter out",
        r"add rule",
        r"remove rule \d+",
        r"show rule",
        r"match\s+\".+\"",
        r"action\s+\".+\"",
        r"AS \d+ enable ROV",
        r"end",
        r"end;"
    ]

    for pattern in valid_patterns:
        if re.match(pattern, line.strip()):
            return True

    return False


# ---------------- CLI ---------------- #

def run_cli():
    print("Welcome to InternetSim CLI")

    buffer = ""
    collecting_block = False

    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break

        if not line:
            continue

        # EXIT
        if line == "exit;":
            print("Exiting...")
            break

        # LOAD
        if line.startswith("load"):
            handle_load(line)
            continue

        # INIT
        if line == "init;":
            init_engine()
            continue

        # RELOAD
        if line == "reload;":
            reload_data()
            continue

        # BLOCK START
        if line.startswith("Change routing policy:") or line.startswith("Change non-BGP policy:"):
            collecting_block = True
            buffer = line + "\n"
            continue

        # BLOCK MODE
        if collecting_block:

            #   detect invalid line early
            if not is_valid_block_line(line):
                print(f"  Invalid line in block: {line}")
                collecting_block = False
                buffer = ""
                continue

            buffer += line + "\n"

            if line == "end;":
                collecting_block = False
                execute_command_block(buffer)
                buffer = ""

            continue

        # NORMAL COMMAND
        if not line.endswith(";"):
            print("  Command must end with ';'")
            continue

        execute_command_block(line)


# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    run_cli()