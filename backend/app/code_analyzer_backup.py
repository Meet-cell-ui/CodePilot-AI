import os


IGNORE_FOLDERS = {
    "node_modules",
    "venv",
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    "dist",
    "build",
}


def analyze_code(project_path):
    result = {
        "languages": {},
        "files_analyzed": 0,
        "functions": 0,
        "classes": 0,
        "issues": []
    }

    for root, dirs, files in os.walk(project_path):

        # Ignore dependency, build and environment folders
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_FOLDERS
        ]

        for file in files:

            if not file.endswith((
                ".py",
                ".java",
                ".js",
                ".html",
                ".css"
            )):
                continue

            result["files_analyzed"] += 1

            extension = file.rsplit(".", 1)[-1].lower()

            language_map = {
                "py": "Python",
                "java": "Java",
                "js": "JavaScript",
                "html": "HTML",
                "css": "CSS",
            }

            language = language_map.get(extension, "Other")

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

                # Basic function detection
                result["functions"] += content.count("def ")
                result["functions"] += content.count("function ")

                # Basic class detection
                result["classes"] += content.count("class ")

                # Basic hardcoded password detection
                if "password=" in content.lower():
                    result["issues"].append({
                        "file": os.path.relpath(
                            file_path,
                            project_path
                        ),
                        "issue": "Possible hardcoded password",
                        "severity": "High"
                    })

            except (OSError, UnicodeDecodeError):
                continue

    return result
