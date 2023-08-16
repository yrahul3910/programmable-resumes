import subprocess
import os

class list(list):
    def map(self, f):
        return list(map(f, self))

import os
from packaging.version import parse as parse_version

CUR_VERSION = "1.0.0"
SPECFILE_NAME = "Specfile"
COMMANDS = [
    "VERSION",
    "INCLUDE",
    "SET",
    "PARSE",
    "BEGIN",
    "USE",
    "IMPORT"
]

line_num = 1
indentation = 0.
indent_type = None
out_file = open("tmp.py", "w")


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
    global indentation, indent_type, line_num, out_file

    if indent_type == "spaces":
        out_file.write(" " * int(4 * indentation))
    elif indent_type == "tabs":
        out_file.write("\t" * int(indentation))


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
    global line_num, indentation, indent_type

    _ = subprocess.Popen(f'cat {SPECFILE_NAME}', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
    _ = [str(x) for x in _.split('\n')]
    specs = _
    parser = "pdflatex"  # Default

    out_file.write("outFile = open(\"main.tex\", \"w\")\n")

    # Parse version
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
            # Parse it as Python code
            out_file.writelines([line + "\n"])
        elif command == "USE":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: USE command must have a processor argument.")

            parser = line.split()[1]
        elif command == "BEGIN":
            out_file.write(get_indent_string() + "parser.parse_begin()\n")
        elif command == "IMPORT":
            out_file.writelines([
                "from spec import DataParser\n",
                "parser = DataParser(outFile, globals() | locals())\n",
            ])
        elif command == "PARSE":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: PARSE command must have a file name.")

            args = line.split()[1:]
            # TODO: Implement argument passing
            out_file.write(get_indent_string() + f"parser.parse_{args[0]}()\n")
        elif command == "SET":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: SET command must have a variable name and a value.")
            
            args = line.split("SET")[1]
            print_indentation()
            out_file.write(args.strip() + "\n")
        elif command == "INCLUDE":
            if len(line.split()) < 2:
                raise SyntaxError(f"L{line_num}: INCLUDE command must have a file name.")

            args = line.split("INCLUDE")[1]
            print_indentation()

            if args.strip().endswith("tex"):
                out_file.writelines([
                    get_indent_string() + f"with open(\"{args.strip()}\") as f:\n",
                    get_indent_string(1) + f"lines = f.readlines()\n",
                    get_indent_string() + f"outFile.writelines(lines + ['\\n'])\n",
                ])
            elif args.strip().endswith("py"):
                _ = subprocess.Popen(f'cat {args}', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
                _ = [str(x) for x in _.split('\n')]
                lines = _
                lines = [get_indent_string() + line + "\n" for line in lines]
                out_file.writelines(lines)
            else:
                raise ValueError(f"L{line_num}: Cannot INCLUDE file that is not .tex or .py, got '{args[0]}'")
            
        elif command == "VERSION":
            raise SyntaxError(f"L{line_num}: Cannot use VERSION command here.")

    out_file.writelines([
        "outFile.writelines([\"\\end{document}\"])\n",
        "outFile.close()\n"
    ])
    out_file.close()

    _ = subprocess.Popen(f'sleep 1 && python3.9 tmp.py && sleep 1 && yes "" | {parser} main.tex', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
    _
    _ = subprocess.Popen(f'rm main.aux main.log tmp.py main.out main.tex', shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode('utf-8').rstrip()
    _


if __name__ == "__main__":
    _main()
