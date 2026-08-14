import os
import json


def analyze_project(folder_path):
    total_files = 0
    total_folders = 0

    languages = set()
    frameworks = []
    database = "Unknown"
    entry_files = set()

    project_type = "Unknown"
    package_manager = "Unknown"
    build_tool = "Unknown"

    readme_found = False
    gitignore_found = False
    requirements_found = False
    package_json_found = False

    IGNORE_FOLDERS = {
        "node_modules",
        "__pycache__",
        ".git",
        "venv",
        ".idea",
        ".vscode"
    }

    for root, dirs, files in os.walk(folder_path):

        # Skip unnecessary folders
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

        total_folders += len(dirs)

        for file in files:

            total_files += 1

            path = os.path.join(root, file)

            # Language Detection
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

            # Entry Files
            if file in ["app.py", "main.py", "server.js", "index.js"]:
                entry_files.add(file)

            # README / Git
            if file.lower() == "readme.md":
                readme_found = True

            if file == ".gitignore":
                gitignore_found = True

            if file == "requirements.txt":
                requirements_found = True

                with open(path, "r", errors="ignore") as f:
                    data = f.read().lower()

                    if "fastapi" in data:
                        frameworks.append("FastAPI")

                    if "flask" in data:
                        frameworks.append("Flask")

                    if "django" in data:
                        frameworks.append("Django")

            # package.json
            if file == "package.json":

                package_json_found = True
                package_manager = "npm"
                build_tool = "Node.js"

                frameworks.append("Node.js")

                try:
                    with open(path, "r", errors="ignore") as f:

                        package = json.load(f)

                        deps = str(package).lower()

                        if "react" in deps:
                            frameworks.append("React")

                        if "express" in deps:
                            frameworks.append("Express")

                except:
                    pass

            # Database
            if file.endswith(".db"):
                database = "SQLite"

    # Project Type
    if "React" in frameworks:
        project_type = "React Web Application"
    elif "Node.js" in frameworks:
        project_type = "Web Application"
    elif "FastAPI" in frameworks:
        project_type = "REST API"
    elif "Flask" in frameworks:
        project_type = "Python Web Application"

    # Health Score
    score = 50

    if readme_found:
        score += 10

    if gitignore_found:
        score += 10

    if requirements_found:
        score += 10

    if package_json_found:
        score += 10

    if entry_files:
        score += 10

    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    else:
        grade = "D"

    # Summary
    summary = (
        f"This is a {project_type} developed using "
        f"{', '.join(sorted(languages))}. "
        f"It contains {total_files} files and "
        f"{total_folders} folders."
    )

    # ----------------------------
    # AI Recommendations
    # ----------------------------

    recommendations = []

    if not readme_found:
        recommendations.append("Add a README.md file to explain the project.")

    if not gitignore_found:
        recommendations.append("Add a .gitignore file to ignore unnecessary files.")

    if database == "Unknown":
        recommendations.append("No database detected.")

    if len(languages) > 3:
        recommendations.append("Project uses multiple languages. Ensure good documentation.")

    if score >= 90:
        recommendations.append("Excellent project structure.")

    return {
        "total_files": total_files,
        "total_folders": total_folders,
        "languages": sorted(list(languages)),
        "frameworks": sorted(list(set(frameworks))),
        "database": database,
        "entry_files": sorted(list(entry_files)),
        "project_type": project_type,
        "package_manager": package_manager,
        "build_tool": build_tool,
        "health_score": score,
        "grade": grade,
        "summary": summary,
        "recommendations": recommendations
    }