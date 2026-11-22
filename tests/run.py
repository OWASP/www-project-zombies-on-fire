"""Run offline game and template checks, with an optional local portal exercise."""

import argparse
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "templates" / "games"
BASELINE = ROOT / "tests" / "fixtures" / "tabletop.json"
QUESTIONS = ("overview", "challenges", "twists", "conclusion")
DOCUMENT_TYPES = (
    "scenario_brief",
    "facilitator_guide",
    "participant_handbook",
    "inject_cards",
    "assessment_rubric",
    "after_action_template",
)


def template_files(suffixes):
    return sorted(
        path for path in TEMPLATES.rglob("*")
        if path.is_file() and path.suffix.lower() in suffixes
    )


def load_fixture(path):
    fixture = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(fixture, dict):
        raise ValueError(f"{path}: expected a JSON object")
    for field in ("title", *QUESTIONS):
        minimum = 3 if field == "title" else 10
        value = fixture.get(field)
        if not isinstance(value, str) or len(value.strip()) < minimum:
            raise ValueError(f"{path}: {field} needs at least {minimum} characters")
        if field == "title" and len(value) > 255:
            raise ValueError(f"{path}: title exceeds 255 characters")
    return fixture


class OfflineChecks(unittest.TestCase):
    def test_game(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Install Node.js 18+ to run the game checks")
        subprocess.run([node, str(ROOT / "tests" / "game.cjs")], check=True, timeout=15)

    def test_text_templates(self):
        paths = template_files({".md", ".txt"})
        self.assertTrue(paths, f"No text templates found in {TEMPLATES}")
        for path in paths:
            with self.subTest(template=path.relative_to(ROOT)):
                self.assertTrue(path.read_text(encoding="utf-8").strip(), "Template is empty")

    def test_portal_fixture_format(self):
        for path in [BASELINE, *template_files({".json"})]:
            with self.subTest(fixture=path.relative_to(ROOT)):
                load_fixture(path)


class PortalChecks(unittest.TestCase):
    def test_local_portal(self):
        try:
            from fastapi.testclient import TestClient
        except ImportError as exc:
            self.fail(f"Install portal/requirements.txt before using --portal ({exc})")

        sys.path.insert(0, str(ROOT / "portal"))
        previous_bytecode_setting = sys.dont_write_bytecode
        sys.dont_write_bytecode = True
        with tempfile.TemporaryDirectory(prefix="zof-tests-") as directory:
            workspace = Path(directory)
            env = {
                "DATABASE_URL": f"sqlite:///{workspace / 'tabletop.db'}",
                "UPLOAD_DIR": str(workspace / "uploads"),
                "PDF_OUTPUT_DIR": str(workspace / "pdfs"),
                "LLM_PROVIDER": "mock",
                "OPENAI_API_KEY": "",
                "ANTHROPIC_API_KEY": "",
                "SECRET_KEY": secrets.token_urlsafe(32),
            }
            previous_directory = Path.cwd()
            try:
                os.chdir(workspace)
                with patch.dict(os.environ, env):
                    from app.database import engine
                    from app.main import app

                    try:
                        with TestClient(app) as client:
                            self.exercise_portal(client)
                    finally:
                        engine.dispose()
            finally:
                os.chdir(previous_directory)
                sys.dont_write_bytecode = previous_bytecode_setting
                sys.path.pop(0)

    def check_status(self, response, expected=200):
        self.assertEqual(
            response.status_code, expected,
            f"{response.request.method} {response.request.url.path}: {response.text[:400]}",
        )

    def exercise_portal(self, client):
        self.check_status(client.get("/health"))
        username = "tabletop-harness"
        password = secrets.token_urlsafe(16)
        created = client.post("/api/auth/register", json={
            "username": username, "password": password, "email": "harness@example.com",
        })
        self.check_status(created, 201)
        login = client.post("/api/auth/login", data={"username": username, "password": password})
        self.check_status(login)
        client.headers["Authorization"] = f"Bearer {login.json()['access_token']}"

        for path in [BASELINE, *template_files({".json"})]:
            with self.subTest(fixture=path.relative_to(ROOT)):
                self.exercise_fixture(client, load_fixture(path))

    def exercise_fixture(self, client, fixture):
        created = client.post("/api/tabletops/", json={"title": fixture["title"]})
        self.check_status(created, 201)
        tabletop_id = created.json()["id"]
        for question in QUESTIONS:
            response = client.put(f"/api/tabletops/{tabletop_id}/questions/{question}", json={
                "question_type": question,
                "answer": fixture[question],
            })
            self.check_status(response)
            self.assertEqual(response.json()["answer"], fixture[question])

        generated = client.post(f"/api/documents/tabletop/{tabletop_id}/generate", json={
            "document_types": DOCUMENT_TYPES,
        })
        self.check_status(generated)
        documents = generated.json()
        self.assertCountEqual([doc["document_type"] for doc in documents], DOCUMENT_TYPES)
        for doc in documents:
            with self.subTest(document=doc["document_type"]):
                self.assertEqual(doc["status"], "completed", doc["error_message"])
                self.assertTrue(doc["content"])
                pdf = client.get(f"/api/documents/{doc['id']}/download")
                self.check_status(pdf)
                self.assertEqual(pdf.headers["content-type"], "application/pdf")
                self.assertTrue(pdf.content.startswith(b"%PDF-"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--portal", action="store_true", help="also run portal API and PDF smoke tests")
    args = parser.parse_args()
    loader = unittest.defaultTestLoader
    suite = loader.loadTestsFromTestCase(OfflineChecks)
    if args.portal:
        suite.addTests(loader.loadTestsFromTestCase(PortalChecks))
    return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
