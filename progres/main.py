import subprocess
import os

class list(list):
    def map(self, f):
        return list(map(f, self))

import os
import json
import argparse
import multiprocessing as mp
import multiprocessing.pool

from packaging.version import parse as parse_version
from progres.utils.args import parse_key_value_pairs
from progres.utils.config import check_config_exists
from progres.utils.io import IOWrapper


CUR_VERSION = "3.0.0"
SPECFILE_NAME = "Specfile"
COMMANDS = [
    "VERSION",
    "INCLUDE",
    "SET",
    "PARSE",
    "BEGIN",
    "USE",
    "IMPORT",
    "CONFIG"
]

line_num = 1
indentation = 0.
indent_type = None
wrapper = None


def get_indentation(line: str) -> None:
    """Gets the indentation of a line."""
    global indentation, indent_type, line_num

    indentation = 0

    for char in line:
        if (char == " " and indent_type == "tabs") or (char == "\t" and indent_type == "spaces"):
            raise IndentationError(f"L{line_num}: Mixed tabs and spaces are not allowed.")

        if char == " ":
            indent_type = "spaces"
            indentation += .25
        elif char == "\t":
            indent_type = "tabs"
            indentation += 1
        else:
            break


def print_indentation() -> None:
    """Prints the indentation of a line."""
    global indentation, indent_type, line_num, wrapper

    if indent_type == "spaces":
        wrapper.write_to_all(" " * int(4 * indentation))
    elif indent_type == "tabs":
        wrapper.write_to_all("\t" * int(indentation))


def get_indent_string(extra: int = 0) -> str:
    """Returns the indentation of a line."""
    global indentation, indent_type, line_num

    if indent_type == "spaces":
        return " " * int(4 * (indentation + extra))
    elif indent_type == "tabs":
        return "\t" * int(indentation + extra)
    else:
        if extra == 0:
            return ""
        else:
            indent_type = "spaces"
            indentation = 1
            return "    "


def _main():
    global line_num, indentation, indent_type, wrapper

    parser = argparse.ArgumentParser(description="Progres: Programmable Resumes.")
    parser.add_argument("--output", "-o", type=str, default="./out", help="Output directory")
    parser.add_argument("--debug", "-d", action="store_true", help="Debug mode")
    sys_args = parser.parse_args()

    proc = subprocess.Popen(f'cat {SPECFILE_NAME}', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    EXIT_CODE = proc.returncode
    __comm = proc.communicate()
    _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
    _ = [str(x) for x in _.split('\n')]
    specs = _

    configs = None
    if check_config_exists(specs):
        configs = json.load(open("configs.json", "r"))

        if "version" not in configs:
            raise RuntimeError("Config file must have a version key.")
        elif parse_version(CUR_VERSION) < parse_version(configs["version"]):
            raise RuntimeError("Current version is less than the version in the config file.")
    else:
        configs = { 
            "configs": {
                "default": [] 
            }
        }
    
    wrapper = IOWrapper(configs)
    parser = "pdflatex"  

    for config in configs["configs"]:
        wrapper.write_to_file(config, f"outFile = open(\"{config}.tex\", \"w\")\n")

    
    if not specs[0].startswith("VERSION"):
        raise SyntaxError(f"First line of specfile must be a VERSION command, got {specs[0]}")

    version = specs[0].split()[1]
    if parse_version(CUR_VERSION) < parse_version(version):
        raise RuntimeError("Current version is less than the version in the specfile.")
    
    for line in specs[1:]:
        line_num += 1
        get_indentation(line)

        if line.strip() == "":
            continue
        
        print(f"Processing {line}")

        command = line.split()[0]
        if command not in COMMANDS:
            
            wrapper.write_to_all(line + "\n")
        elif command == "USE":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: USE command must have a processor argument.")

            parser = line.split()[1]
        elif command == "BEGIN":
            wrapper.write_to_all(get_indent_string() + "parser.parse_begin()\n")
        elif command == "IMPORT":
            wrapper.write_to_all("from spec import DataParser\n")
            wrapper.write_to_all("parser = DataParser(outFile, globals() | locals())\n")
        elif command == "PARSE":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: PARSE command must have a file name.")

            args = line.split()[1:]
            section = args[0]

            rest = " ".join(args[1:])
            wrapper.write_to_all(get_indent_string() + f"parser.parse_{section}({parse_key_value_pairs(rest)})\n")
        elif command == "SET":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: SET command must have a variable name and a value.")
            
            args = line.split("SET")[1]
            print_indentation()
            wrapper.write_to_all(args.strip() + "\n")
        elif command == "INCLUDE":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: INCLUDE command must have a file name.")

            args = line.split("INCLUDE")[1]
            print_indentation()

            if args.strip().endswith("tex"):
                _lines = [
                    get_indent_string() + f"with open(\"{args.strip()}\") as f:\n",
                    get_indent_string(1) + f"lines = f.readlines()\n",
                    get_indent_string() + f"outFile.writelines(lines + ['\\n'])\n",
                ]

                for x in _lines:
                    wrapper.write_to_all(x)
            elif args.strip().endswith("py"):
                proc = subprocess.Popen(f'cat {args}', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.wait()
                EXIT_CODE = proc.returncode
                __comm = proc.communicate()
                _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
                _ = [str(x) for x in _.split('\n')]
                lines = _
                lines = [get_indent_string() + line + "\n" for line in lines]
                
                for line in lines:
                    wrapper.write_to_all(line)
            else:
                raise ValueError(f"L{line_num}: Cannot INCLUDE file that is not .tex or .py, got '{args[0]}'")
        elif command == "CONFIG":
            for config in configs["configs"]:
                for command in configs["configs"][config]:
                    wrapper.write_to_file(config, command + "\n")
        elif command == "VERSION":
            raise SyntaxError(f"L{line_num}: Cannot use VERSION command here.")

    wrapper.write_to_all("outFile.writelines([\"\\end{document}\"])\n")
    wrapper.write_to_all("outFile.close()\n")
    wrapper.close_all_files()

    
    cpu_count = mp.cpu_count()

    def f(config):
        print(f"Compiling config: {config}")
        proc = subprocess.Popen(f'sleep 1 && python3 {config}.py && sleep 1 && yes "" | {parser} {config}.tex', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        EXIT_CODE = proc.returncode
        __comm = proc.communicate()
        _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
        _
        
        if EXIT_CODE != 0:
            if sys_args.debug:
                print(f"{parser} failed:\n{STDERR}")

            raise RuntimeError(f"Failed to compile {config}.tex: failed at the {parser} step.")

        proc = subprocess.Popen(f'rm {config}.aux {config}.log {config}.py {config}.out {config}.tex', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        EXIT_CODE = proc.returncode
        __comm = proc.communicate()
        _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
        _
        proc = subprocess.Popen(f'mkdir -p {sys_args.output} && mv {config}.pdf {sys_args.output}/', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        EXIT_CODE = proc.returncode
        __comm = proc.communicate()
        _, STDERR = __comm[0].decode('utf-8').rstrip(), __comm[1].decode('utf-8').rstrip()
        _

    with multiprocessing.pool.ThreadPool(processes=cpu_count) as pool:
        pool.map(f, [config for config in configs["configs"].keys()])
    
    print("Done!")


if __name__ == "__main__":
    _main()
