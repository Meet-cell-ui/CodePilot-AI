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


def mask_sensitive_code(line, issue_name):
    """
    Hide sensitive values before returning security findings.
    """

    if issue_name in {
        "Hardcoded Password",
        "Hardcoded API Key",
        "Hardcoded Secret",
        "AWS Access Key"
    }:
        if "=" in line:
            key_part = line.split("=", 1)[0].strip()
            return f"{key_part} = \"[REDACTED]\""

        return "[REDACTED]"

    return line.strip()


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
            "regex": r'api[_-]?key\s*=\s*["\'].*["\']',
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

    # Walk through project
    for root, dirs, files in os.walk(project_path):

        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for file in files:

            # Ignore minified JS
            if file.endswith(".min.js"):
                continue

            # Ignore unsupported files
            if not file.endswith(SUPPORTED_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)

            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                for line_no, line in enumerate(lines, start=1):

                    stripped = line.strip()

                    # Ignore comments
                    if stripped.startswith("#") or stripped.startswith("//"):
                        continue

                    # Pattern-based checks
                    for pattern in patterns:
                        if re.search(pattern["regex"], line, re.IGNORECASE):
                            issues.append({
                                "file": file,
                                "line": line_no,
                                "severity": pattern["severity"],
                                "issue": pattern["name"],
                                "code": stripped
                            })

                    # Bare except
                    if "except:" in line:
                        issues.append({
                            "file": file,
                            "line": line_no,
                            "severity": "Medium",
                            "issue": "Bare except block",
                            "code": stripped
                        })

                    # Dangerous eval
                    if "eval(" in line:
                        issues.append({
                            "file": file,
                            "line": line_no,
                            "severity": "High",
                            "issue": "Use of eval()",
                            "code": stripped
                        })

                    # Dangerous command execution (Node.js)
                    if "child_process.exec(" in line:
                        issues.append({
                            "file": file,
                            "line": line_no,
                            "severity": "High",
                            "issue": "Command Execution",
                            "code": stripped
                        })

                    # Dangerous subprocess in Python
                    if "subprocess.Popen(" in line or "os.system(" in line:
                        issues.append({
                            "file": file,
                            "line": line_no,
                            "severity": "High",
                            "issue": "Command Execution",
                            "code": stripped
                        })

            except Exception:
                pass

    return issues