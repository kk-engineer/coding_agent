from core.orchestrator import generate_suggested_diffs


def test_generate_suggested_diffs_does_not_write_files(monkeypatch):

    calls = {
        "write": 0
    }

    def fake_read_file(file_path):

        return "old\n"

    def fake_generate_updated_file(user_prompt, file_path):

        return "new\n"

    def fake_write_file(file_path, content):

        calls["write"] += 1

    monkeypatch.setattr(
        "core.orchestrator.read_file",
        fake_read_file
    )
    monkeypatch.setattr(
        "core.orchestrator.generate_updated_file",
        fake_generate_updated_file
    )
    monkeypatch.setattr(
        "core.orchestrator.write_file",
        fake_write_file
    )

    diffs = generate_suggested_diffs(
        user_prompt="add greeting",
        files=["example.py"]
    )

    assert calls["write"] == 0
    assert diffs[0]["file"] == "example.py"
    assert "-old" in diffs[0]["diff"]
    assert "+new" in diffs[0]["diff"]


def test_generate_suggested_diffs_respects_limit(monkeypatch):

    seen_files = []

    def fake_read_file(file_path):

        return "old\n"

    def fake_generate_updated_file(user_prompt, file_path):

        seen_files.append(file_path)
        return "new\n"

    monkeypatch.setattr(
        "core.orchestrator.read_file",
        fake_read_file
    )
    monkeypatch.setattr(
        "core.orchestrator.generate_updated_file",
        fake_generate_updated_file
    )

    generate_suggested_diffs(
        user_prompt="update files",
        files=["a.py", "b.py", "c.py"],
        limit=2
    )

    assert seen_files == ["a.py", "b.py"]


def test_generate_suggested_diffs_reports_progress(monkeypatch):

    events = []

    def fake_read_file(file_path):

        return "old\n"

    def fake_generate_updated_file(user_prompt, file_path):

        return "new\n"

    def record_progress(event, file_path, index, total):

        events.append((event, file_path, index, total))

    monkeypatch.setattr(
        "core.orchestrator.read_file",
        fake_read_file
    )
    monkeypatch.setattr(
        "core.orchestrator.generate_updated_file",
        fake_generate_updated_file
    )

    generate_suggested_diffs(
        user_prompt="update files",
        files=["a.js", "b.go"],
        progress_callback=record_progress
    )

    assert events == [
        ("start", "a.js", 1, 2),
        ("end", "a.js", 1, 2),
        ("start", "b.go", 2, 2),
        ("end", "b.go", 2, 2),
    ]


def test_generate_suggested_diffs_skips_generated_files(monkeypatch):

    seen_files = []

    def fake_read_file(file_path):

        seen_files.append(file_path)
        return "old\n"

    monkeypatch.setattr(
        "core.orchestrator.read_file",
        fake_read_file
    )

    diffs = generate_suggested_diffs(
        user_prompt="update deps",
        files=["uv.lock", "package-lock.json"]
    )

    assert diffs == []
    assert seen_files == []
