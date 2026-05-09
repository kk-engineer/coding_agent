def test_execution_manager_uses_streaming_llm(monkeypatch):

    calls = {
        "stream": 0
    }

    class Delta:
        content = "updated\n"

    class Choice:
        delta = Delta()

    class Chunk:
        choices = [Choice()]

    def fake_read_file(file_path):

        return "old\n"

    def fake_chat_stream(messages):

        calls["stream"] += 1

        return iter([Chunk()])

    monkeypatch.setattr(
        "core.execution_manager.read_file",
        fake_read_file
    )
    monkeypatch.setattr(
        "core.execution_manager.chat_stream",
        fake_chat_stream
    )

    from core.execution_manager import generate_updated_file

    assert generate_updated_file("update", "example.js") == "updated\n"
    assert calls["stream"] == 1


def test_test_analyzer_uses_streaming_llm(monkeypatch):

    calls = {
        "stream": 0
    }

    class Delta:
        content = "root cause"

    class Choice:
        delta = Delta()

    class Chunk:
        choices = [Choice()]

    def fake_chat_stream(messages):

        calls["stream"] += 1

        return iter([Chunk()])

    monkeypatch.setattr(
        "core.test_analyzer.chat_stream",
        fake_chat_stream
    )

    from core.test_analyzer import analyze_test_failure

    assert analyze_test_failure("fix tests", "boom") == "root cause"
    assert calls["stream"] == 1
