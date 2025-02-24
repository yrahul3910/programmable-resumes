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

## Setup

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

* `--output / -o`: The output directory. Defaults to `out/`
* `--debug / -d`: Enable debug mode. This prints out stack traces from stderr during compilation.

### Supported Templates

We currently support the following LaTeX templates. If you would like to add your template, or request support for one, please create either an issue or a PR. To use these templates, see the `examples/` folder, and copy the files. Add in your `Specfile` and `data.json`, and run `progres`. Note that Awesome CV works best with `xelatex`, so make sure your Specfile has `USE xelatex`.

- [Awesome CV](https://github.com/posquit0/Awesome-CV/)
- [LaTeX Resume Template](https://github.com/rajnikant7008/Latex-Resume-Template)

# Usage

See the [documentation](./docs/index.md) for docs specific to end-users as well as template devs.

## Developer Guide

This section discusses the internal working of the system. If you are not a contributor to the project, you may ignore this section.

The program starts by reading the Specfile. The Specfile is used to create a main Python file, which in turn is used to create a LaTeX file. Finally, this LaTeX file is processed using the command-line. The program is powered by [pysh](https://github.com/yrahul3910/pysh), a superset of Python that adds Shell functionality. Pysh has a [VS Code extension](https://marketplace.visualstudio.com/items?itemName=RahulYedida.pysh-highlighting) for syntax highlighting.
