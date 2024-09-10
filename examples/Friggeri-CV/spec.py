import os
import json
from datetime import datetime
from packaging.version import parse as parse_version


class DataParser:
    VERSION = "3.0.0"

    def __init__(self, file, vars):
        self.file = file
        self.vars = vars

        if not os.path.exists("data.json"):
            raise RuntimeError("data.json not found")

        with open("data.json", "r") as f:
            self.data = json.load(f)
        
        if "version" not in self.data:
            raise RuntimeError("data.json missing version")

        if parse_version(self.data["version"]) > parse_version(self.VERSION):
            raise RuntimeError("data.json version is newer than spec.py version")
    
    def _get_str_from_date(self, date):
        try:
            return datetime.fromisoformat(date).strftime("%b %Y")
        except TypeError:
            return "Unknown"
    
    def _get_str_from_dates(self, dates):
        [start, end] = dates
        try:
            start = datetime.fromisoformat(start).strftime("%b %Y")
        except TypeError:
            start = "Present"
        
        try:
            end = datetime.fromisoformat(end).strftime("%b %Y")
        except TypeError:
            end = "Present"
        
        return f"{start} - {end}"

    def parse_begin(self):
        self.file.write(r"\documentclass[]{friggeri-cv}" + "\n")
        self.file.write(r"\begin{document}" + "\n")
    
    def parse_personalInfo(self):
        info = self.data["personalInfo"]
        self.file.write(r"\header{")
        self.file.write(info["name"])
        self.file.write("}")

        self.file.write(r"\begin{aside}" + "\n")
        self.file.write(r"\section{contact}" + "\n")
        self.file.write(info["contact"]["phone"] + r"\faPhone" + "\n")
        self.file.write(r"\href{mailto:" + info["contact"]["email"] + "}{" + info["contact"]["email"] + r"}")
        self.file.write("\n")
        hrefs = [r"\href{" + link["url"] + "}{" + link["display"] + r"~\faBookmark}" for link in info["links"]]
        self.file.write("\n".join(hrefs))
        self.file.write(r"\end{aside}" + "\n")

    def parse_education(self):
        if len(self.data["education"]) == 0:
            return

        self.file.write(r"\section{education}" + "\n")
        self.file.write(r"\begin{entrylist}" + "\n")
        for entry in self.data["education"]:
            self.file.write(r"\courseentry{" + self._get_str_from_dates(entry["dates"]) + "}{" + entry["degree"] + "}{" + entry["institution"] + "}{}{}" + "\n")
        self.file.write(r"\end{entrylist}" + "\n")
    
    def parse_employment(self, after_date="1970-01-01"):
        if len(self.data["employment"]) == 0:
            return
        
        after_date = datetime.fromisoformat(after_date)

        self.file.write(r"\section{experience}" + "\n")
        self.file.write(r"\begin{entrylist}" + "\n")

        # This template prefers a flattened set of positions
        # for each organization, so we'll flatten the data
        # structure here.
        positions = []
        for entry in self.data["employment"]:
            for position in entry["positions"]:
                positions.append({
                    "dates": self._get_str_from_dates(entry["dates"]),
                    "org": entry["organization"],
                    "location": entry["location"],
                    "role": position["role"],
                    "details": position["details"],
                    "tags": position["tags"]
                })

        for entry in positions:
            # TODO Check the tags in position. If that self.vars[tag] is True, then we 
            # include this position in the CV.

            dates = self._get_str_from_dates(position["dates"])

            try:
                pos_end_date = datetime.fromisoformat(position["dates"][1])

                if pos_end_date < after_date:
                    continue
            except TypeError:
                # Probably got null, which means we should not filter
                pass

            self.file.write(r"\entry{" + self._get_str_from_dates(entry["dates"]) + "}{" + entry["organization"] + "}{" + entry["location"] + "}{" + entry["role"] + r"\\")
            self.file.write("\n")
            self.file.write(r"\begin{itemize}")

            for detail in entry["details"]:
                self.file.write(r"\item " + detail)
                self.file.write("\n")

            self.file.write(r"\end{itemize}}")

        self.file.write(r"\end{entrylist}" + "\n")
    
    def parse_publications(self):
        self.file.write(r"\addbibresource{bibliography.bib}")
        self.file.write("\n")

        # TODO Check that the bibliography file exists and contains each section.
        self.file.write(r"\section{publications}" + "\n")
        self.file.write(r"\printbibsection{article}{Journal Articles}" + "\n")
        self.file.write(r"\printbibsection[keyword={conference}]{inproceedings}{Conference Proceedings}" + "\n")
        self.file.write(r"\printbibsection[keyword={workshop}]{inproceedings}{Workshop Proceedings}" + "\n")
    
    def parse_funding(self):
        self.file.write(r"\section{funding}" + "\n")
        self.file.write(r"\begin{entrylist}" + "\n")
        for entry in self.data["funding"]:
            self.file.write(r"\entry{" + self._get_str_from_dates(entry["dates"]) + "}{" + entry["amount"] + ", " + entry["title"] + "}{}{}\n")
        self.file.write(r"\end{entrylist}" + "\n")
    
    def parse_service(self):
        self.file.write(r"\section{service}" + "\n")
        self.file.write(r"\begin{entrylist}" + "\n")
        for entry in self.data["service"]:
            self.file.write(r"\entry{}{" + entry["title"] + "}{" + entry["details"] + "}{}{}\n")
        self.file.write(r"\end{entrylist}" + "\n")
    
    def parse_honors(self):
        self.file.write(r"\section{honors}" + "\n")
        self.file.write(r"\begin{entrylist}" + "\n")
        for entry in self.data["honors"]:
            self.file.write(r"\entry{" + self._get_str_from_date(entry["date"]) + "}{" + entry["title"] + "}{}{}\n")
        self.file.write(r"\end{entrylist}" + "\n")
    
    def parse_projects(self, latest_k=999):
        pass
    
    def parse_skills(self):
        pass
