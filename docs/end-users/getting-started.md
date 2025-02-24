# End-users: getting started

## Pre-requisites

You need a few things installed to use `progres` on your machine. 

The first is Python installation. If you're on macOS or Linux, you probably already have this installed! Verify this by running `python3 -V` in a terminal. If you're on Windows, visit the [Python website](https://python.org) to download Python.

The second thing is a LaTeX installation. LaTeX is a typesetting engine that can produce consistent PDFs and is cross-platform. TeXLive is the usual distribution for LaTeX (which is simply the language): see [their website](https://www.tug.org/texlive/) for installation instructions. TeXLive, and other LaTeX "distributions" come in several versions. In general, you'll want the "full" version, because it allows template authors to use any package there to develop their template.

Finally, you'll want to install `progres` itself. The simplest way to do this is to clone the repository, navigate to the directory, and then install the package:

```
git clone https://github.com/yrahul3910/programmable-resumes
cd programmable-resumes
python3 -m pip install .
```

This should get `progres` installed; try it out by running `progres -h`.

## Writing your resume

The `progres` philosophy is to have a data file with _all_ your information, and then filter out details based on the roles you're applying to. It's worth also having an unfiltered version or "master" CV.

### The `data.json` file

Create a `data.json` file and a `Specfile` (both described below). Download a template, which should include a template spec file (`spec.py`), a preamble (`preamble.tex`), and any auxiliary files. The format of the `data.json` file is shown in [this documentation page](../data-json.md).

### The `Specfile`

The spec file is a file called `Specfile`, and like a Dockerfile, is a series of commands. Each command performs a variety of actions, and can usually take arguments to modify behavior. 

Each Specfile starts with a `VERSION` command that defines the Specfile version you are writing. Typically, you will follow this with a `INCLUDE` command to add a *preamble*, which contains custom LaTeX commands, LaTeX preambles, document class, etc. You can include as many preambles as you'd like. Usually, the template developer will give you a preamble as well. Following this, you will use several `PARSE` commands. Each `PARSE` command makes a call to the parser class you defined. You can pass args to these functions using a `key=value` syntax, or a `key="value"` syntax if you have spaces.

```
VERSION 3.0.0

INCLUDE preamble.tex

IMPORT
BEGIN
PARSE education
PARSE employment
PARSE honors
PARSE projects max=5
PARSE skills
```

In general, this will be the structure of the `Specfile`. Unless otherwise specified by the template authors, this structure should work. Note that some `PARSE` commands can take arguments. These arguments are not universal, and template developers are responsible for documenting these options to you.

The `Specfile` lets you do more advanced manipulation as well. You can use a `SET` command to create a variable. A variable can have any type that is valid in Python, though it is recommended you stick to strings and numeric values. After all your `SET` commands, but before your `BEGIN` command, you should use the `IMPORT` command. At this point, the template develoepr's `DataParser` class will be imported. The `USE` command defines what LaTeX processor is used to create the final PDF. For example, Awesome CV requires `xelatex`. If this is not specified, `pdflatex` is used by default. The `PYTHON` command is either a path or the command to use for the Python executable. This should be at least 3.9. By default, `python3` is used.

You can also use the `INCLUDE` command to include Python code. The command will process the file based on its extension. This is useful if you need to define functions or more complex logic. Within Python files that you write, you can write out to the final LaTeX file using a `outFile` object.

### The config file

The config file is optional, and used in conjunction with the `CONFIG` command in the `Specfile`. The config file is a file named `configs.json`, that has the following structure:

```json
{
  "version": string,
  "configs: {
    "configName": string[]
  }
}
```

The version key contains the `progres` version you're using. Because this feature was implemented in version 2.0.0, this should be the minimum version. The `configs` key contains a mapping of config names to a list of Python statements. This is best used in conjunction with the tags defined in your `data.json` file. For employment, most templates will only include positions if **all the tags match, or if the tag list for the position is empty**. For projects, templates usually includes them if **any tag matches, or if the tag list for the project is empty**. Tags are set as Python variables, so this is the perfect place to define those configs. In the `examples/` directory, you'll see an example of this. For example, the LaTeX-Resume-Template example, in `computeRole.py`, along with the configs, define several boolean variables. In `spec.py`, these variables are checked against the tags of the projects and employment to decide if they should be included.

In your `Specfile`, add the `CONFIG` command where you want these Python statements to be executed. Almost always, you want these to be before any `PARSE` commands.

## Compiling your resume

It's time to generate your PDFs! The simplest way to compile is to go to the directory where your files are, and run

```
progres
```

This compiles your resumes and places them in an `out` directory. You might prefer to have the directory be called something else; use the `-o` flag for this, like so:

```
progres -o pdf
```

`progres` includes a "debug" flag that lets you see the progress (heh) being made:

```
progres -d
```

This is helpful if something goes wrong, since it makes it slightly easier to see what step it failed at.

## Best practices

It's recommended that you check in your files, including the compiled PDFs, into source control (and use something like GitHub). Of course, add a `.gitignore` with the usual entries (the one you'll likely want is `__pycache__/`).
