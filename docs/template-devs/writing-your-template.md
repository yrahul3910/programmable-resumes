# Writing your template

## Template Spec File

A `spec.py` file should be defined with the following structure:

```python
class DataParser:
  def parse_xxx(self) -> str:
    ...
```

The `parse_xxx` function should read the `data.json` file and return a LaTeX string that for that section of the CV. Each of the `xxx` is one of the keys in `data.json` (example: `parse_personalInfo`). See the `examples/` directory for examples.

## The `Specfile`

See [the end-user documentation](../end-users/getting-started.md) for how the `Specfile` is used. `progres` handles most of those implementation details for you, so we only describe here what you as the template dev need to create a template.

The `BEGIN` command will call `parse_begin()` on the `DataParser` class you define. Usually, this should just write out `\begin{document}` to the file, like so:

```py
def parse_begin(self):
    self.file.write(r"\begin{document}")
    self.file.write("\n")
```

The `IMPORT` command is the point at which your `DataParser` class is imported. This is why it always comes before the `BEGIN` statement. Generally, we separate these out since it provides the flexibility for both you and end-users to add functionality between these two steps.

## Additional files

You may also want to distribute additional files with your template. For example, you might want some functionality moved to a different Python file; or some of your LaTeX separated into its own file. End-users can import both of these types of files, so feel free to do so, and include that in your documentation
