import os
import json

class DataParser:
    def __init__(self, file, vars):
        self.file = file
        self.vars = vars

        if not os.path.exists("data.json"):
            raise RuntimeError("data.json not found")

        with open("data.json", "r") as f:
            self.data = json.load(f)

    def parse_education(self):
        if len(self.data["education"]) == 0:
            return
        
        self.file.write("\\section{Education}\n")
        self.file.write("\\resumeSubHeadingListStart\n")

        for entry in self.data["education"]:
            school = entry["institution"]
            location = entry["location"]
            degree = entry["degree"]
            dates = entry["dates"]

            self.file.write(r"\resumeSubheading{" + school + "}{" + location + "}{" + degree + "}{" + dates + "}\n")
        
        self.file.write("\\resumeSubHeadingListEnd\n")
    
    def parse_employment(self):
        if len(self.data["employment"]) == 0:
            return
        
        self.file.write("\\section{Employment}\n")
        self.file.write("\\resumeSubHeadingListStart\n")

        for entry in self.data["employment"]:
            company = entry["organization"]
            location = entry["location"]
            positions = entry["positions"]
        
        self.file.write("\\resumeSubHeadingListEnd\n")
