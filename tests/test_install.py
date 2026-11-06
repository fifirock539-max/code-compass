import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

class InstallTests(unittest.TestCase):
    def test_both_platforms_and_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            for platform, directory in [('codex', '.agents'), ('claude', '.claude')]:
                paths = installer.install(tmp, platform)
                self.assertEqual(len(paths), 7)
                for path in paths:
                    self.assertEqual((path / 'SKILL.md').read_bytes(), (ROOT / 'skills' / path.name / 'SKILL.md').read_bytes())
                    self.assertEqual(path.parent, Path(tmp) / directory / 'skills')
    def test_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            installer.install(tmp, 'codex', True)
            self.assertEqual(list(Path(tmp).iterdir()), [])
    def test_conflict_is_non_mutating(self):
        with tempfile.TemporaryDirectory() as tmp:
            conflict = Path(tmp) / '.agents/skills/cc-term'
            conflict.mkdir(parents=True)
            sentinel = conflict / 'mine.txt'
            sentinel.write_text('keep')
            with self.assertRaises(FileExistsError):
                installer.install(tmp, 'codex')
            self.assertEqual(sentinel.read_text(), 'keep')
            self.assertEqual(list(conflict.parent.iterdir()), [conflict])
    def test_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside:
            (Path(tmp) / '.agents').symlink_to(outside)
            with self.assertRaises(ValueError):
                installer.install(tmp, 'codex')
            self.assertEqual(list(Path(outside).iterdir()), [])

if __name__ == '__main__':
    unittest.main()
