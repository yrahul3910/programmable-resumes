# Documentation for Awesome CV

This is the Awesome CV template, ported to `progres`. It expects a `postition` and `address` variable to be set, which you can do in your `Specfile`. It works best with `xelatex`, so set that up in `Specfile`.

## Features

* **Anonymous mode:** Anonymous mode anonymizes your personal information and updates the links in your personal projects to the website's canonical addresses.
* Publications are not currently supported by this template!
* Supported links in your personal information section include the keys: "github", "linkedin", "googlescholar", "stackoverflow", "twitter", "skype", "medium", "gitlab", "kaggle".
* `parse_employment` accepts an `after_date` parameter that's a string of the format "YYYY-MM-DD", so in your `Specfile`, you can use `PARSE employment after_date="YYYY-MM-DD"`.
* `parse_projects` accepts a `latest_k` integer parameter.

