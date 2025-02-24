# End-user documentation

## Index

* [Getting started](./getting-started.md)

## A high-level description

There are 4 parts to creating a resume using `progres`:

- A data JSON file with all the information necessary (called the data file).
- A config JSON file that contains code executed for different variants of your CV (optional)
- A `Specfile` that specifies what information goes, in what order, and other conditions such as most recent publications only.
- A Python parser file that defines how to convert to LaTeX (called a template spec file)

As the end-user, you usually do not need to write the last one; that is usually provided by template authors. You should follow their instructions on how to incorporate their template into your `Specfile`.
