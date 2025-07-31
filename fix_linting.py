#!/usr/bin/env python3
import os
import re


def fix_file(filepath):
    """Fix common linting issues in a file"""
    with open(filepath, "r") as f:
        content = f.read()

    original_content = content

    # Remove unused imports (common ones we can safely remove)
    patterns_to_remove = [
        r"^import os\n" if "os" not in content.replace("import os", "") else None,
        (
            r"^from typing import Any\n"
            if "Any" not in content.replace("from typing import Any", "")
            else None
        ),
        (
            r"^from typing import Optional\n"
            if "Optional" not in content.replace("from typing import Optional", "")
            else None
        ),
        (
            r"^from typing import Dict\n"
            if "Dict" not in content.replace("from typing import Dict", "")
            else None
        ),
        (
            r"^from typing import Tuple\n"
            if "Tuple" not in content.replace("from typing import Tuple", "")
            else None
        ),
        (
            r"^import time\n"
            if "time." not in content.replace("import time", "")
            else None
        ),
        (
            r"^import json\n"
            if "json." not in content.replace("import json", "")
            else None
        ),
        (
            r"^from datetime import date\n"
            if "date" not in content.replace("from datetime import date", "")
            else None
        ),
        (
            r"^from datetime import datetime\n"
            if "datetime" not in content.replace("from datetime import datetime", "")
            else None
        ),
        (
            r"^from sqlalchemy import JSON\n"
            if "JSON" not in content.replace("from sqlalchemy import JSON", "")
            else None
        ),
        (
            r"^from fastapi import Response\n"
            if "Response" not in content.replace("from fastapi import Response", "")
            else None
        ),
    ]

    for pattern in patterns_to_remove:
        if pattern:
            content = re.sub(pattern, "", content, flags=re.MULTILINE)

    # Fix long lines by adding line breaks (simple cases)
    lines = content.split("\n")
    fixed_lines = []

    for line in lines:
        if len(line) > 88 and "(" in line and ")" in line:
            # Try to break long function calls
            if line.strip().startswith("raise ") or "logger." in line:
                # Break after opening parenthesis
                parts = line.split("(", 1)
                if len(parts) == 2:
                    indent = len(parts[0]) - len(parts[0].lstrip())
                    line = f"{parts[0]}(\n{' ' * (indent + 4)}{parts[1]}"
        fixed_lines.append(line)

    content = "\n".join(fixed_lines)

    if content != original_content:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Fixed: {filepath}")


# Files to fix
files_to_fix = [
    "scripts/data_quality_monitor.py",
    "scripts/test_data_cleaning_pipeline.py",
    "scripts/test_fallback_adapter.py",
    "scripts/test_polygon_adapter.py",
    "scripts/test_yahoo_adapter.py",
    "src/agents/base.py",
    "src/api/main.py",
    "src/api/routes/strategies.py",
    "src/core/data/models.py",
    "src/core/data/providers/fallback.py",
    "src/core/data/providers/polygon.py",
    "src/core/llm/agents/base.py",
    "src/core/llm/orchestrator.py",
    "src/core/llm/providers/anthropic.py",
    "src/core/llm/providers/openai.py",
    "src/core/llm/utils/cost_tracker.py",
    "src/core/llm/utils/rate_limiter.py",
    "src/core/logging/http_logger.py",
    "src/core/risk/circuit_breaker.py",
    "src/core/risk/exposure_guard.py",
    "src/core/security/middleware.py",
    "src/core/strategies/performance.py",
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        fix_file(filepath)
    else:
        print(f"Not found: {filepath}")

print("Bulk fixes complete!")
