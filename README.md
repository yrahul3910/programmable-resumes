# Programmable Resumes

This project implements programmable resumes, a modular approach to defining a resume. This allows users to customize exactly what information goes in their CV for different roles, while preserving all the data about past projects, employments, etc.

There are 3 parts:

- A JSON file with all the information necessary.
- A spec file that specifies what information goes, in what order, and other conditions such as most recent publications only.
- A Python parser file that defines how to convert to LaTeX.

End-users will only be expected to write a the spec file and the JSON file, while developers for templates will provide the parser file and auxiliary files (such as LaTeX class files).

## Data file (JSON)

A `data.json` file must be defined with the following spec:

```json
{
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
    "dates": string,
    "details": string[]?
  }],
  "employment": [{
    "organization": string,
    "location": string,
    "position": string,
    "dates": string,
    "details": string[],
    "tags": string[]?
  }],
  "projects": [{
    "title": string,
    "dates": string,
    "skills": string[],
    "links": [{
      "display": string,
      "url": string
    }]?,
    "details": string[]
  }],
  "publications": [{
    "latex": string
  }],
  "skills": [{
    "name": string,
    "type": string
  }],
  "honors": [{
    "date": string,
    "title": string
  }],
  "funding": [{
    "amount": string,
    "title": string,
    "date": string
  }],
  "service": [{
    "title": string,
    "details": string
  }]
}
```

## Python Parser File

A `spec.py` file should be defined. It must have the following structure:

```python
class DataParser:
  def parse_xxx(self) -> str:
    ...
```

The `parse_xxx` function should read the `data.json` file and return a LaTeX string that for that section of the CV. Each of the `xxx` is one of the keys in `data.json` (example: `parse_personalInfo`)

## Spec File

The spec file is a file called `Specfile`, and like a Dockerfile, is a series of commands. Each command performs a variety of actions, and can usually take arguments to modify behavior. 

Each Specfile starts with a `VERSION` command that defines the Specfile version you are writing. Typically, you will follow this with a `INCLUDE` command to add a *preamble*, which contains custom LaTeX commands, LaTeX preambles, document class, etc. Following this, you will use several `PARSE` commands. At the first `PARSE` command, the `\begin{document}` will be inserted. Each `PARSE` command makes a call to the parser class you defined. You can pass args to these functions using a `key=value` syntax, or a `key="value"` syntax if you have spaces.

```
VERSION 1.0

INCLUDE preamble.tex
PARSE education
PARSE employment
PARSE honors
PARSE projects max=5
PARSE skills
```

The Specfile lets you do more advanced manipulation as well. You can use a `SET` command to create a variable. A variable can have any type that is valid in Python, though it is recommended you stick to strings and numeric values. You can also use the `SET` command with backticks to include Python code. For example, suppose you wanted to include today's month and year in your employment (say, as an end date). You might do something like so:

```
PARSE employment end=`datetime.datetime.now().strftime("%b %Y")`
```

You can also use the `INCLUDE` command to include Python code. The command will process the file based on its extension. This is useful if you need to define functions or more complex logic. You can access variables using curly braces, like so:

```
PARSE projects max=5 role={role}
```

where `role` is a variable that has been defined at some point.

## Developer Guide

This section discusses the internal working of the system. If you are not a contributor to the project, you may ignore this section.

The program starts by reading the Specfile. The Specfile is used to create a main Python file, which in turn is used to create a LaTeX file. Finally, this LaTeX file is processed using the command-line. The program is powered by pysh, a superset of Python that adds Shell functionality.