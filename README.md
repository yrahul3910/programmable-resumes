# Programmable Resumes

![](overlap.png)

This project implements programmable resumes, a modular approach to defining a resume. This allows users to customize exactly what information goes in their CV for different roles, while preserving all the data about past projects, employments, etc.

There are 4 parts:

- A data JSON file with all the information necessary (called the data file).
- A config JSON file that contains code executed for different variants of your CV (optional)
- A spec file that specifies what information goes, in what order, and other conditions such as most recent publications only.
- A Python parser file that defines how to convert to LaTeX (called a template spec file)

End-users will only be expected to write a the spec file and the JSON file, while developers for templates will provide the parser file and auxiliary files (such as LaTeX class files).

## Requirements

- Python 3.9+
- LaTeX installation (e.g. TeXLive)

## Usage

### End-users

As an end-user who is writing their own CV, create a `data.json` file and a `Specfile` (both described below). Download a template, which should include a template spec file (`spec.py`), a preamble (`preamble.tex`), and any auxiliary files. Make sure you have a LaTeX installation, and that your TeX command of choice (`pdflatex`, `xelatex`, etc.) is in your PATH. Also ensure you have a Python 3.9+ installation. 

### Template developers

As a template developer, you are expected to publish a template spec file, along with any auxiliary files your template might need. Typically, this will include a preamble of some sort and a LaTeX class file. You may also include auxiliary files as necessary. You should also include a `README.md` file that describes how to use your template. See the `examples/` directory for two examples.

### Installation

Use `install.sh` to install the tool. This has `pysh` as a pre-requisite. [Pysh](https://github.com/yrahul3910/pysh) is a superset of Python, which allows Shell commands to be directly included in the code. This is mostly syntactic sugar. Alternatively, run

```sh
pip3 install .
```

which uses the transpiled Python code instead.

### Running the tool

Run

```
progres
```

to create your CV. `progres` accepts the following options:

* `--output / -d`: The output directory. Defaults to `out/`
* `--debug / -d`: Enable debug mode. This prints out stack traces from stderr during compilation.

### Supported Templates

We currently support the following LaTeX templates. If you would like to add your template, or request support for one, please create either an issue or a PR. To use these templates, see the `examples/` folder, and copy the files. Add in your `Specfile` and `data.json`, and run `progres`. Note that Awesome CV works best with `xelatex`, so make sure your Specfile has `USE xelatex`.

- [Awesome CV](https://github.com/posquit0/Awesome-CV/)
- [LaTeX Resume Template](https://github.com/rajnikant7008/Latex-Resume-Template)

# Usage

## Data file (JSON)

A `data.json` file must be defined with the following spec. Note that dates must be in ISO-8601 format (YYYY-MM-DD). If you wish to denote the present, use null instead. Writers of templates must include checks to ensure that null dates are handled correctly.

```json
{
  "version": string,
  "personalInfo": {
    "name": string,
    "suffix": string?,
    "contact": {
      "email": string,
      "phone": string
    },
    "links": [{
      "display": string,
      "url": string
    }]
  },
  "summary": string,
  "education": [{
    "institution": string,
    "location": string,
    "degree": string,
    "dates": string[],
    "details": string[]?
  }],
  "employment": [{
    "organization": string,
    "location": string,
    "positions": [{
      "position": string,
      "dates": string[],
      "details": string[],
      "tags": string[]?
    }]
  }],
  "projects": [{
    "title": string,
    "dates": string[],
    "skills": string[],
    "links": [{
      "display": string,
      "url": string
    }]?,
    "details": string[],
    "tags": string[]?
  }],
  "publications": string[],
  "talks": [{
    "title": string,
    "event": string,
    "date": string,
    "location": string
  }],
  "skills": [{
    "name": string,
    "type": string
  }],
  "honors": [{
    "date": string[],
    "location": string?,
    "details": string?,
    "title": string
  }],
  "funding": [{
    "amount": string,
    "title": string,
    "date": string
  }],
  "service": [{
    "title": string,
    "details": string,
    "date": string?
  }]
}
```

## Template Spec File

A `spec.py` file should be defined. It must have the following structure:

```python
class DataParser:
  def parse_xxx(self) -> str:
    ...
```

If you are an end-user, you will not be writing this file. Instead, this will be provided by a template developer. For example, see the `examples/` directory, each of which has a `spec.py` provided for you.

The `parse_xxx` function should read the `data.json` file and return a LaTeX string that for that section of the CV. Each of the `xxx` is one of the keys in `data.json` (example: `parse_personalInfo`). See the examples/ directory for examples.

## Spec File

The spec file is a file called `Specfile`, and like a Dockerfile, is a series of commands. Each command performs a variety of actions, and can usually take arguments to modify behavior. 

Each Specfile starts with a `VERSION` command that defines the Specfile version you are writing. Typically, you will follow this with a `INCLUDE` command to add a *preamble*, which contains custom LaTeX commands, LaTeX preambles, document class, etc. You can include as many preambles as you'd like. Usually, the template developer will give you a preamble as well. Following this, you will use several `PARSE` commands. Each `PARSE` command makes a call to the parser class you defined. You can pass args to these functions using a `key=value` syntax, or a `key="value"` syntax if you have spaces.

```
VERSION 1.0.0

INCLUDE preamble.tex

IMPORT
BEGIN
PARSE education
PARSE employment
PARSE honors
PARSE projects max=5
PARSE skills
```

The `BEGIN` command will call `parse_begin()` on the `DataParser` class you define. Usually, this should just write out `\begin{document}` to the file, like so:

```py
def parse_begin(self):
    self.file.write(r"\begin{document}")
    self.file.write("\n")
```

The Specfile lets you do more advanced manipulation as well. You can use a `SET` command to create a variable. A variable can have any type that is valid in Python, though it is recommended you stick to strings and numeric values. After all your `SET` commands, but before your `BEGIN` command, you should use the `IMPORT` command. At this point, your `DataParser` class will be imported. The `USE` command defines what LaTeX processor is used to create the final PDF. For example, Awesome CV requires `xelatex`. If this is not specified, `pdflatex` is used by default. The `PYTHON` command is either a path or the command to use for the Python executable. This should be at least 3.9. By default, `python3` is used.

You can also use the `INCLUDE` command to include Python code. The command will process the file based on its extension. This is useful if you need to define functions or more complex logic. Within Python files that you write, you can write out to the final LaTeX file using a `outFile` object.

## Config file

The config file is optional, and used in conjunction with the `CONFIG` command in the `Specfile`. The config file is a file named `configs.json`, that has the following structure:

```json
{
  "version": string,
  "configs: {
    "configName": string[]
  }
}
```

The version key contains the `progres` version you're using. Because this feature was implemented in version 2.0.0, this should be the minimum version. The `configs` key contains a mapping of config names to a list of Python statements. This is best used in conjunction with the tags defined in your `data.json` file. Since `progres` will only include projects and employment based on tags (which are set as Python variables), this is the perfect place to define those configs. In the `examples/` directory, you'll see an example of this. For example, the LaTeX-Resume-Template example, in `computeRole.py`, along with the configs, define several boolean variables. In `spec.py`, these variables are checked against the tags of the projects and employment to decide if they should be included.

In your `Specfile`, add the `CONFIG` command where you want these Python statements to be executed. Almost always, you want these to be before any `PARSE` commands. In a future version, multiple config JSON files will be supported for even greater flexibility.

## Developer Guide

This section discusses the internal working of the system. If you are not a contributor to the project, you may ignore this section.

The program starts by reading the Specfile. The Specfile is used to create a main Python file, which in turn is used to create a LaTeX file. Finally, this LaTeX file is processed using the command-line. The program is powered by [pysh](https://github.com/yrahul3910/pysh), a superset of Python that adds Shell functionality. Pysh has a [VS Code extension](https://marketplace.visualstudio.com/items?itemName=RahulYedida.pysh-highlighting) for syntax highlighting.