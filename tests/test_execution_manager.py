from core.execution_manager import strip_markdown_code_fence


def test_strip_python_markdown_code_fence():

    content = "```python\nprint('hello')\n```\n"

    assert strip_markdown_code_fence(content) == "print('hello')\n"


def test_strip_plain_markdown_code_fence():

    content = "```\nkey = 'value'\n```\n"

    assert strip_markdown_code_fence(content) == "key = 'value'\n"


def test_preserves_unwrapped_content():

    content = "print('hello')\n"

    assert strip_markdown_code_fence(content) == content


def test_preserves_inner_fences_when_not_wrapping_whole_response():

    content = "before\n```python\nprint('hello')\n```\nafter\n"

    assert strip_markdown_code_fence(content) == content
