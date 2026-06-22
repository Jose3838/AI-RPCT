import json
from pathlib import Path


SENSITIVE_FILES = [Path(".env")]
EXAMPLE_FILE = Path(".env.example")


def build_secret_hygiene_check():
    gitignore = Path(".gitignore").read_text() if Path(".gitignore").exists() else ""
    env_ignored = ".env" in {line.strip() for line in gitignore.splitlines()}
    example_has_values = False
    example_keys = []

    if EXAMPLE_FILE.exists():
        for line in EXAMPLE_FILE.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            example_keys.append(key)
            if value.strip():
                example_has_values = True

    return {
        "product": "AI-RPCT",
        "env_ignored": env_ignored,
        "env_file_exists_locally": any(path.exists() for path in SENSITIVE_FILES),
        "env_example_keys": example_keys,
        "env_example_has_secret_values": example_has_values,
        "status": "ok" if env_ignored and not example_has_values else "needs_attention",
    }


def main():
    print(json.dumps(build_secret_hygiene_check(), indent=2))


if __name__ == "__main__":
    main()
