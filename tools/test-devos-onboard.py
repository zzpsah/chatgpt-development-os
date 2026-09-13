#!/usr/bin/env python3
from pathlib import Path
import importlib.util
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools/devos-onboard.py"
spec = importlib.util.spec_from_file_location("devos_onboard", MODULE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def main():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "existing-repo"
        root.mkdir()
        (root / ".git").mkdir()
        (root / ".ai").mkdir()
        existing = root / ".ai/PROJECT.md"
        existing.write_text("KEEP-ME\n", encoding="utf-8")
        (root / "app.py").write_text("print('application')\n", encoding="utf-8")

        first = mod.inventory(root, "My Existing App", "my-existing-app")
        assert first["status"] == "READY", first
        assert any(x["path"] == ".ai/PROJECT.md" and x["action"] == "PRESERVE" for x in first["actions"])
        code, created = mod.apply(root, first)
        assert code == 0, created
        assert existing.read_text(encoding="utf-8") == "KEEP-ME\n"
        assert (root / ".ai/manifest.yaml").exists()
        assert (root / ".github/workflows/context-sync.yml").exists()

        second = mod.inventory(root, "My Existing App", "my-existing-app")
        assert second["status"] == "READY"
        assert all(item["action"] == "PRESERVE" for item in second["actions"]), second
        code2, created2 = mod.apply(root, second)
        assert code2 == 0 and created2 == [], created2

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "new-project"
        root.mkdir()
        plan = mod.inventory(root, None, None)
        assert plan["status"] == "READY"
        assert plan["repository_kind"] == "directory"
        code, created = mod.apply(root, plan)
        assert code == 0
        assert ".github/workflows/context-sync.yml" not in created
        assert (root / ".ai/manifest.yaml").exists()

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "conflict"
        root.mkdir()
        (root / ".ai").mkdir()
        (root / ".ai/manifest.yaml").write_text(
            "managed_by: another-framework\nproject_id: conflict\n", encoding="utf-8"
        )
        report = mod.inventory(root, None, None)
        assert report["status"] == "HOLD", report
        code, created = mod.apply(root, report)
        assert code == 2 and created, (code, created)
        assert not (root / "AGENTS.md").exists()

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "new-git"
        root.mkdir(); (root / ".git").mkdir()
        report = mod.inventory(root, None, None)
        assert any(x["path"] == ".github/workflows/context-sync.yml" and x["action"] == "CREATE" for x in report["actions"])

    print("PASS: universal DevOS onboarding regression corpus")


if __name__ == "__main__":
    main()
