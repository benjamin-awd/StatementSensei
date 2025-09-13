import re
import tomllib
import requests
from pathlib import Path

# Paths
pyproject = Path("pyproject.toml")
readme = Path("README.md")
constants = Path("webapp/constants.py")

# 1. Read monopoly-core version
with pyproject.open("rb") as f:
    data = tomllib.load(f)

version = None
for dep in data["project"]["dependencies"]:
    if dep.startswith("monopoly-core=="):
        version = dep.split("==")[1]
        break

if not version:
    raise RuntimeError("monopoly-core version not found in pyproject.toml")

print(f"Using monopoly-core version: {version}")

# 2. Fetch monopoly-core README from GitHub tag
url = f"https://raw.githubusercontent.com/benjamin-awd/monopoly/v{version}/README.md"
resp = requests.get(url)
resp.raise_for_status()
monopoly_readme = resp.text

# 3. Extract Supported banks block
pattern = re.compile(
    r"(Supported banks:?\n(?:\|.*\n)+)(?=\n#|\Z)",  # stop at next heading or EOF
    re.IGNORECASE,
)
match = pattern.search(monopoly_readme)
if not match:
    raise RuntimeError("Supported banks block not found in monopoly README")

supported_banks_block = match.group(1).strip() + "\n"

# 4. Replace in StatementSensei README
readme_text = readme.read_text()
new_readme = re.sub(
    r"(Supported banks:?\n(?:\|.*\n)+)(?=\n#|\Z)",
    supported_banks_block,
    readme_text,
    flags=re.IGNORECASE,
)
readme.write_text(new_readme)
print("✅ Updated Supported banks in README.md")

# 5. Replace in webapp/constants.py
constants_text = constants.read_text()
new_constants = re.sub(
    r'SUPPORTED_BANKS\s*=\s*""".*?"""',
    f'SUPPORTED_BANKS = """{supported_banks_block}"""',
    constants_text,
    flags=re.DOTALL,
)
constants.write_text(new_constants)
print("✅ Updated SUPPORTED_BANKS in webapp/constants.py")
