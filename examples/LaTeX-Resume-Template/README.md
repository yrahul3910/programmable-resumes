# LaTeX Resume Template

This implements the necessary preamble and template spec file for [this MIT-licensed template](https://github.com/rajnikant7008/Latex-Resume-Template/tree/master).

## How to use

Please see the accompanying `Specfile` for an example on using this template. Currently, this template supports the following parsing arguments:

* `process_projects` supports `latest_k`, which defaults to 999. This decides how many projects the CV should be limited to. Note that projects are also filtered by their tags.
* `process_employment` supports `after_date`, which defaults to `"1970-01-01"`. This decides which employment positions are displayed. This filtering is done at the position-level, not the org-level.
