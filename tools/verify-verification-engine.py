from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "core" / "verification-engine.md"
ROADMAP = ROOT / "docs" / "ROADMAP.md"


def require(text, needle, label):
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def main():
    engine = ENGINE.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")

    for phrase, label in [
        ("## Verification levels", "verification levels"),
        ("## Evidence model", "evidence model"),
        ("## Detecting applicable checks", "applicable-check detection"),
        ("## Execution and delegation", "execution/delegation"),
        ("### VERIFIED", "VERIFIED semantics"),
        ("### PARTIAL", "PARTIAL semantics"),
        ("### UNVERIFIED", "UNVERIFIED semantics"),
        ("### FAILED", "FAILED semantics"),
        ("## Claim-prevention rules", "unsupported-claim prevention"),
        ("## Verification report", "verification report contract"),
        ("Authorization ≠ Verification", "authorization boundary"),
        ("No evidence, no VERIFIED claim.", "evidence gate"),
        ("Production smoke tests, migrations, destructive tests, paid external services, or data-affecting verification require the applicable authorization gate.", "protected verification gate"),
    ]:
        require(engine, phrase, label)

    for phrase, label in [
        ("VERIFIED / PARTIAL / UNVERIFIED / FAILED", "status vocabulary"),
        ("Define verification levels and evidence model", "roadmap verification-level item"),
        ("Detect applicable tests/checks", "roadmap applicability item"),
        ("Execute or delegate supported checks", "roadmap execution item"),
        ("Honest VERIFIED / PARTIAL / UNVERIFIED / FAILED reporting", "roadmap reporting item"),
        ("Prevent unsupported correctness claims", "roadmap claim-prevention item"),
    ]:
        require(roadmap, phrase, label)

    print("Verification Engine contract checks passed.")


if __name__ == "__main__":
    main()
