import os
import re


IGNORE_DIRS = {
    "node_modules",
    "venv",
    ".venv",
    ".git",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "target"
}


def scan_security(project_path):

    issues = []

    patterns = [
        {
            "name": "Hardcoded Password",
            "regex": r'password\s*=\s*["\'].*["\']',
            "severity": "High"
        },
        {
            "name": "Hardcoded API Key",
            "regex": r'(api[_-]?key|apikey)\s*=\s*["\'].*["\']',
            "severity": "High"
        },
        {
            "name": "Hardcoded Secret",
            "regex": r'secret\s*=\s*["\'].*["\']',
            "severity": "High"
        },
        {
            "name": "AWS Access Key",
            "regex": r'AKIA[0-9A-Z]{16}',
            "severity": "Critical"
        }
    ]

    supported_extensions = (
        ".py",
        ".js",
        ".java",
        ".ts",
        ".jsx",
        ".tsx",
        ".html",
        ".css"
    )

    for root, dirs, files in os.walk(project_path):

        # Prevent scanning dependency/build folders
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:

            if not file.endswith(supported_extensions):
                continue

            file_path = os.path.join(root, file)

            try:

                with open(
                    file_path,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    lines = f.readlines()

                for line_no, line in enumerate(lines, start=1):

                    stripped_line = line.strip()

                    # Ignore comments
                    if stripped_line.startswith(
                        ("#", "//", "/*", "*")
                    ):
                        continue

                    # Security patterns
                    for pattern in patterns:

                        if re.search(
                            pattern["regex"],
                            line,
                            re.IGNORECASE
                        ):

                            issues.append({
                                "file": os.path.relpath(
                                    file_path,
                                    project_path
                                ),
                                "line": line_no,
                                "severity": pattern["severity"],
                                "issue": pattern["name"],
                                "code": stripped_line
                            })

                    # Bare except
                    if re.search(
                        r'^\s*except\s*:',
                        line
                    ):

                        issues.append({
                            "file": os.path.relpath(
                                file_path,
                                project_path
                            ),
                            "line": line_no,
                            "severity": "Medium",
                            "issue": "Bare except block",
                            "code": stripped_line
                        })

                    # eval()
                    if re.search(
                        r'\beval\s*\(',
                        line
                    ):

                        issues.append({
                            "file": os.path.relpath(
                                file_path,
                                project_path
                            ),
                            "line": line_no,
                            "severity": "High",
                            "issue": "Use of eval()",
                            "code": stripped_line
                        })

                    # exec()
                    if re.search(
                        r'\bexec\s*\(',
                        line
                    ):

                        issues.append({
                            "file": os.path.relpath(
                                file_path,
                                project_path
                            ),
                            "line": line_no,
                            "severity": "High",
                            "issue": "Use of exec()",
                            "code": stripped_line
                        })

            except Exception:
                continue

    return issues
