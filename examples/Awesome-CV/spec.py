import os
import json


class DataParser:
    """
    Template spec file for Awesome CV. Expects a `position` and `address` variable to be set.
    """

    def __init__(self, file, vars):
        self.file = file
        self.vars = vars

        if not os.path.exists("data.json"):
            raise RuntimeError("data.json not found")

        with open("data.json", "r") as f:
            self.data = json.load(f)
    
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
        name = info["name"].split(" ")
        first_name = " ".join(name[:-1])
        last_name = name[-1]

        self.file.write(r"\name{" + first_name + "}{" + last_name + "}")
        self.file.write("\n")
        self.file.write(r"\position{" + self.vars.get("position") + r"}")
        self.file.write("\n")
        self.file.write(r"\address{" + self.vars.get("address") + r"}")
        self.file.write("\n")
        self.file.write(r"\mobile{" + info["contact"]["phone"] + r"}")
        self.file.write("\n")
        self.file.write(r"\email{" + info["contact"]["email"] + r"}")
        self.file.write("\n")

        supported_links = ["github", "linkedin", "googlescholar",
                           "stackoverflow", "twitter", "skype", "medium", "gitlab", "kaggle"]

        for item in supported_links:
            link = [x for x in info["links"]
                    if x["display"].lower().replace(" ", "") == item]
            if len(link) > 0:
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
            dates = entry["dates"]

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
    
    def parse_employment(self):
        if len(self.data["employment"]) == 0:
            return
        
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
                # Check tags
                if any([self.vars.get(tag, False) for tag in position["tags"]]):
                    self.file.write(r"\cventry")
                    self.file.write("\n")
                    self.file.write(r"{" + position["position"] + r"}")
                    self.file.write("\n")
                    self.file.write(r"{" + company + r"}")
                    self.file.write("\n")
                    self.file.write(r"{" + location + r"}")
                    self.file.write("\n")
                    self.file.write(r"{" + position["dates"] + r"}{")
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
    
    def parse_projects(self):
        if len(self.data["projects"]) == 0:
            return
        
        self.file.write("\n")
        self.file.write(r"\cvsection{Projects}")
        self.file.write("\n")
        self.file.write(r"\begin{cventries}")
        self.file.write("\n")

        for entry in self.data["projects"]:
            if any([self.vars.get(tag, False) for tag in entry["tags"]]):
                self.file.write(r"\cventry")
                self.file.write("\n")
                self.file.write(r"{" + ", ".join(entry["skills"]) + r"}")
                self.file.write("\n")
                self.file.write(r"{" + entry["title"] + r"}")
                self.file.write("\n")

                links = [rf"\href{{{link['url']}}}{{{link['display']}}}" for link in entry["links"]]
                self.file.write(r"{" + ", ".join(links) + r"}")
                self.file.write("\n")
                self.file.write(r"{" + entry["dates"] + r"}{")
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
            self.file.write(r"{" + entry["date"] + r"}")
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
            self.file.write(r"{" + entry["date"] + r"}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvhonors}")
        self.file.write("\n")
    
    def parse_publications(self):
        # Not currently supported by Awesome CV
        pass

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
                self.file.write(r"{" + entry["date"] + r"}")
            else:
                self.file.write("{}")
            self.file.write("\n")
        
        self.file.write(r"\end{cvhonors}")
        self.file.write("\n")
