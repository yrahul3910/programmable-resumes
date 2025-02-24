import os
import json
from datetime import datetime
from packaging.version import parse as parse_version


class DataParser:
    """
    Template spec file for Awesome CV. Expects a `position` and `address` variable to be set.
    """
    VERSION = "3.1.0"

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
        self.file.write(r"\begin{document}")
        self.file.write("\n")
        self.file.write(r"\makecvheader")
        self.file.write("\n")
        self.file.write(r"\makecvfooter{}{}{\thepage}")
        self.file.write("\n")

    def parse_personalInfo(self):
        info = self.data["personalInfo"]

        # Split name into first and last. Split by the last space in the name.
        if self.vars.get("ANONYMOUS_MODE", False):
            name = "Anonymous"
            first_name = "Anonymous"
            last_name = ""

            address = "Address" if "address" in self.vars else ""
            phone = "Phone" if info["contact"]["phone"] else ""
            email = "Email" if info["contact"]["email"] else ""
        else:
            name = info["name"].split(" ")
            first_name = " ".join(name[:-1])
            last_name = name[-1]

            address = self.vars.get("address", "")
            phone = info["contact"]["phone"]
            email = info["contact"]["email"]

        self.file.write(r"\name{" + first_name + "}{" + last_name + "}")
        self.file.write("\n")
        self.file.write(r"\position{" + self.vars.get("position") + r"}")
        self.file.write("\n")
        self.file.write(r"\address{" + address + r"}")
        self.file.write("\n")
        self.file.write(r"\mobile{" + phone + r"}")
        self.file.write("\n")
        self.file.write(r"\email{" + email + r"}")
        self.file.write("\n")

        supported_links = ["github", "linkedin", "googlescholar",
                           "stackoverflow", "twitter", "skype", "medium", "gitlab", "kaggle"]

        for item in supported_links:
            link = [x for x in info["links"]
                    if x["display"].lower().replace(" ", "") == item]

            if len(link) > 0:
                url = link[0]["url"]
                if self.vars.get("ANONYMOUS_MODE", False):
                    url = url.split(".com")[0] + ".com"

                self.file.write("\\" + item + "{" + link[0]["url"] + r"}")

                if item == "googlescholar":
                    self.file.write(r"{}")
                self.file.write("\n")
    
    def parse_education(self):
        if len(self.data["education"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Education}")
        self.file.write("\n")
        self.file.write(r"\begin{cventries}")
        self.file.write("\n")

        for entry in self.data["education"]:
            school = entry["institution"]
            location = entry["location"]
            degree = entry["degree"]
            dates = self._get_str_from_dates(entry["dates"])

            self.file.write(r"\cventry")
            self.file.write("\n")
            self.file.write(r"{" + degree + r"}")
            self.file.write("\n")
            self.file.write(r"{" + school + r"}")
            self.file.write("\n")
            self.file.write(r"{" + location + r"}")
            self.file.write("\n")
            self.file.write(r"{" + dates + r"}{")
            self.file.write("\n")

            if "details" in entry and len(entry["details"]) > 0:
                self.file.write(r"\begin{cvitems}")
                self.file.write("\n")

                for detail in entry["details"]:
                    self.file.write(r"\item{" + detail + r"}")
                    self.file.write("\n")

                self.file.write(r"\end{cvitems}")
                self.file.write("\n")
            
            self.file.write("}")
            self.file.write("\n")
        
        self.file.write(r"\end{cventries}")
    
    def parse_employment(self, after_date="1970-01-01"):
        if len(self.data["employment"]) == 0:
            return
        
        after_date = datetime.fromisoformat(after_date)
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Experience}")
        self.file.write("\n")
        self.file.write(r"\begin{cventries}")
        self.file.write("\n")

        for entry in self.data["employment"]:
            company = entry["organization"]
            location = entry["location"]
            positions = entry["positions"]

            for position in positions:
                # Check date
                dates = self._get_str_from_dates(position["dates"])
                if datetime.fromisoformat(position["dates"][1]) < after_date:
                    continue

                # Check tags
                if not position["tags"] or all([self.vars.get(tag, False) for tag in position["tags"]]):
                    self.file.write(r"\cventry")
                    self.file.write("\n")
                    self.file.write(r"{" + position["position"] + r"}")
                    self.file.write("\n")
                    self.file.write(r"{" + company + r"}")
                    self.file.write("\n")
                    self.file.write(r"{" + location + r"}")
                    self.file.write("\n")
                    self.file.write(r"{" + dates + r"}{")
                    self.file.write("\n")

                    if "details" in position and len(position["details"]) > 0:
                        self.file.write(r"\begin{cvitems}")
                        self.file.write("\n")

                        for detail in position["details"]:
                            self.file.write(r"\item{" + detail + r"}")
                            self.file.write("\n")

                        self.file.write(r"\end{cvitems}")
                        self.file.write("\n")
                    
                    self.file.write("}")
                    self.file.write("\n")
        
        self.file.write(r"\end{cventries}")
        self.file.write("\n")

    def parse_skills(self):
        if len(self.data["skills"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Skills}")
        self.file.write("\n")
        self.file.write(r"\begin{cvskills}")
        self.file.write("\n")

        # Get map from skill type to list of skills
        skills = {}
        for skill in self.data["skills"]:
            if skill["type"] not in skills:
                skills[skill["type"]] = []
            skills[skill["type"]].append(skill["name"])

        for skill in skills:
            self.file.write(r"\cvskill")
            self.file.write("\n")
            self.file.write(r"{" + skill + r"}")
            self.file.write("\n")
            self.file.write(r"{" + ", ".join(skills[skill]) + r"}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvskills}")
        self.file.write("\n")
    
    def parse_projects(self, latest_k=999):
        if len(self.data["projects"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Projects}")
        self.file.write("\n")
        self.file.write(r"\begin{cventries}")
        self.file.write("\n")

        # Re-arrange self.data["projects"] in descending order of completion date.
        self.data["projects"].sort(
            key=lambda p: datetime.fromisoformat(p["dates"][1]) if p["dates"][1] is not None else datetime(3000, 1, 1),
            reverse=True
        )

        i = 0
        k = 0

        while k < latest_k and i < len(self.data["projects"]) - 1:
            entry = self.data["projects"][i]
            i += 1

            if "hidden" in entry and entry["hidden"]:
                continue

            if not entry["tags"] or any([self.vars.get(tag, False) for tag in entry["tags"]]):
                k += 1
                self.file.write(r"\cventry")
                self.file.write("\n")
                self.file.write(r"{" + ", ".join(entry["skills"]) + r"}")
                self.file.write("\n")
                self.file.write(r"{" + entry["title"] + r"}")
                self.file.write("\n")

                links = [rf"\href{{{link['url']}}}{{{link['display']}}}" for link in entry["links"]]

                if self.vars.get("ANONYMOUS_MODE", False):
                    links = [link.split(".com")[0] + ".com" for link in links]

                self.file.write(r"{" + ", ".join(links) + r"}")
                self.file.write("\n")
                self.file.write(r"{" + self._get_str_from_dates(entry["dates"]) + r"}{")
                self.file.write("\n")

                if "details" in entry and len(entry["details"]) > 0:
                    self.file.write(r"\begin{cvitems}")
                    self.file.write("\n")

                    for detail in entry["details"]:
                        self.file.write(r"\item{" + detail + r"}")
                        self.file.write("\n")

                    self.file.write(r"\end{cvitems}")
                    self.file.write("\n")
                
                self.file.write("}")
                self.file.write("\n")
        
        self.file.write(r"\end{cventries}")
        self.file.write("\n")

    def parse_honors(self):
        if len(self.data["honors"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Honors \& Awards}")
        self.file.write("\n")
        self.file.write(r"\begin{cvhonors}")
        self.file.write("\n")

        for entry in self.data["honors"]:
            self.file.write(r"\cvhonor")
            self.file.write("\n")
            self.file.write(r"{" + entry["title"] + r"}")
            self.file.write("\n")
            
            if "details" in entry:
                self.file.write(r"{" + entry["issuer"] + r"}")
            else:
                self.file.write("{}")
            self.file.write("\n")

            if "location" in entry:
                self.file.write(r"{" + entry["location"] + r"}")
            else:
                self.file.write("{}")
            self.file.write("\n")
            self.file.write(r"{" + self._get_str_from_date(entry["date"]) + r"}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvhonors}")
        self.file.write("\n")

    def parse_funding(self):
        if len(self.data["funding"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Funding}")
        self.file.write("\n")
        self.file.write(r"\begin{cvhonors}")
        self.file.write("\n")

        for entry in self.data["funding"]:
            self.file.write(r"\cvhonor")
            self.file.write("\n")
            self.file.write(r"{" + entry["amount"] + r"}")
            self.file.write("\n")
            self.file.write(r"{" + entry["title"] + r"}")
            self.file.write("\n")
            self.file.write("{}")
            self.file.write("\n")
            self.file.write(r"{" + self._get_str_from_date(entry["date"]) + r"}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvhonors}")
        self.file.write("\n")
    
    def parse_publications(self, latest_k=999):
        # Not currently supported by Awesome CV
        pass

    def parse_talks(self):
        if len(self.data["talks"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Talks}")
        self.file.write("\n")
        self.file.write(r"\begin{cvhonors}")
        self.file.write("\n")

        for entry in self.data["talks"]:
            self.file.write(r"\cvhonor")
            self.file.write("\n")
            self.file.write(r"{" + entry["title"] + r"}")
            self.file.write("\n")
            self.file.write(r"{" + entry["event"] + r"}")
            self.file.write("\n")
            self.file.write(r"{" + entry["location"] + r"}")
            self.file.write("\n")
            self.file.write(r"{" + self._get_str_from_date(entry["date"]) + r"}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvhonors}")
        self.file.write("\n")

    def parse_service(self):
        if len(self.data["service"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Service}")
        self.file.write("\n")
        self.file.write(r"\begin{cvhonors}")
        self.file.write("\n")

        for entry in self.data["service"]:
            self.file.write(r"\cvhonor")
            self.file.write("\n")
            self.file.write(r"{" + entry["title"] + r"}")
            self.file.write("\n")
            self.file.write(r"{" + entry["details"] + r"}")
            self.file.write("\n")
            self.file.write("{}")
            self.file.write("\n")

            if "date" in entry:
                self.file.write(r"{" + self._get_str_from_date(entry["date"]) + r"}")
            else:
                self.file.write("{}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvhonors}")
        self.file.write("\n")
