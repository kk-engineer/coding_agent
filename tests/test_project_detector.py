from repo_utils.project_detector import (
    detect_project_type,
    detect_test_command
)


def test_detect_node_project(tmp_path):

    (tmp_path / "package.json").write_text("{}")

    assert detect_project_type(tmp_path) == "frontend/node"
    assert detect_test_command(tmp_path) == "npm test"


def test_detect_go_project(tmp_path):

    (tmp_path / "go.mod").write_text("module example.com/app")

    assert detect_project_type(tmp_path) == "go"
    assert detect_test_command(tmp_path) == "go test ./..."


def test_unknown_project_has_no_default_test_command(tmp_path):

    assert detect_project_type(tmp_path) == "unknown"
    assert detect_test_command(tmp_path) is None


def test_detect_hugo_project(tmp_path):

    (tmp_path / "hugo.toml").write_text("baseURL = 'https://example.com'")

    assert detect_project_type(tmp_path) == "hugo"
    assert detect_test_command(tmp_path) == "hugo --gc --minify"


def test_detect_docsy_project(tmp_path):

    (tmp_path / "hugo.toml").write_text("baseURL = 'https://example.com'")
    (tmp_path / "themes").mkdir()
    (tmp_path / "themes" / "docsy").mkdir()

    assert detect_project_type(tmp_path) == "hugo, docsy"
