"""Runs against real files in a temp directory (no mocks): python -m unittest"""
import os
import tempfile
import unittest
from pathlib import Path

from src.public_record.env_loader import load_env


class LoadEnvTest(unittest.TestCase):
    def setUp(self):
        self.dir = Path(tempfile.mkdtemp())

    def write(self, name, text):
        p = self.dir / name
        p.write_text(text)
        os.chmod(p, 0o600)
        return p

    def test_precedence(self):
        shared = self.write("secrets.env", "A=shared\nB=shared\nC=\n")
        local = self.write(".env", "A=local\nC=local\nD=local\n")
        env = {"B": "process"}
        load_env(shared_file=shared, local_file=local, env=env, quiet=True)
        self.assertEqual((env["A"], env["B"], env["C"], env["D"]), ("shared", "process", "local", "local"))

    def test_project_prefix(self):
        shared = self.write("secrets.env", "PACER_USERNAME=common\nPUBLIC_RECORD__PACER_USERNAME=pr\n")
        env = {}
        load_env(project="public_record", shared_file=shared, local_file=None, env=env, quiet=True)
        self.assertEqual(env["PACER_USERNAME"], "pr")
        self.assertNotIn("PUBLIC_RECORD__PACER_USERNAME", env)

    def test_comment_only_value_is_blank(self):
        shared = self.write("secrets.env", "OPENAI_API_KEY=   # OpenAI key\n")
        local = self.write(".env", "OPENAI_API_KEY=from-local\n")
        env = {}
        load_env(shared_file=shared, local_file=local, env=env, quiet=True)
        self.assertEqual(env["OPENAI_API_KEY"], "from-local")

    def test_missing_shared_file(self):
        local = self.write(".env", "X=1\n")
        env = {}
        r = load_env(shared_file=self.dir / "none.env", local_file=local, env=env, quiet=True)
        self.assertEqual(env["X"], "1")
        self.assertFalse(r["shared_found"])


if __name__ == "__main__":
    unittest.main()
