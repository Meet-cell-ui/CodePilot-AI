import os


def analyze_code(project_path):

    result = {
        "languages": {},
        "files_analyzed": 0,
        "functions": 0,
        "classes": 0,
        "issues": []
    }

    for root, folders, files in os.walk(project_path):

        for file in files:

            if file.endswith((".py", ".java", ".js", ".html", ".css")):

                result["files_analyzed"] += 1

                extension = file.split(".")[-1]

                if extension == "py":
                    language = "Python"

                elif extension == "java":
                    language = "Java"

                elif extension == "js":
                    language = "JavaScript"

                elif extension == "html":
                    language = "HTML"

                elif extension == "css":
                    language = "CSS"

                else:
                    language = "Other"


                result["languages"][language] = (
                    result["languages"].get(language, 0) + 1
                )


                file_path = os.path.join(root, file)

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8",
                        errors="ignore"
                    ) as f:

                        content = f.read()


                    # Count functions

                    result["functions"] += content.count("def ")
                    result["functions"] += content.count("function ")

                    # Count classes

                    result["classes"] += content.count("class ")


                    # Security check

                    if "password=" in content.lower():

                        result["issues"].append(
                            {
                                "file": file,
                                "issue": "Possible hardcoded password",
                                "severity": "High"
                            }
                        )


                except Exception:
                    pass


    return result