import os


def analyze_project(folder_path):
    total_files = 0
    total_folders = 0

    languages = set()

    framework = "Unknown"

    database = "Unknown"

    entry_file = None

    for root, dirs, files in os.walk(folder_path):

        total_folders += len(dirs)

        for file in files:

            total_files += 1

            # -------- Languages --------

            if file.endswith(".py"):
                languages.add("Python")

            elif file.endswith(".js"):
                languages.add("JavaScript")

            elif file.endswith(".html"):
                languages.add("HTML")

            elif file.endswith(".css"):
                languages.add("CSS")

            elif file.endswith(".java"):
                languages.add("Java")

            elif file.endswith(".cpp"):
                languages.add("C++")

            # -------- Entry Files --------

            if file == "app.py":
                entry_file = "app.py"

            elif file == "main.py":
                entry_file = "main.py"

            elif file == "server.js":
                entry_file = "server.js"

            # -------- Framework Detection --------

            if file == "requirements.txt":

                path = os.path.join(root, file)

                with open(path, "r", errors="ignore") as f:

                    data = f.read().lower()

                    if "flask" in data:
                        framework = "Flask"

                    elif "fastapi" in data:
                        framework = "FastAPI"

            if file == "package.json":

                framework = "Node.js"

            # -------- Database --------

            if file.endswith(".db"):
                database = "SQLite"

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "languages": sorted(list(languages)),
        "framework": framework,
        "database": database,
        "entry_file": entry_file
    }