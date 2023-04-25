"""Pytest for easy_gpt/main.py"""
import os
import pytest
import subprocess
import sys

from easy_gpt._gpt_cli import cli

ARGS = [
    "--version",
    "--help",
    "ask --help",
    "ask how are you",
    "ask --doc review.py what does this file do?",
    # "git --help",
    # "git status",
]


@pytest.mark.parametrize("command", ARGS)
@pytest.mark.integration
def test_int_gpt_cli(command):
    """Test gpt commands from installed CLI"""

    command_array = f"gpt {command}".split(" ")
    result = subprocess.run(
        command_array,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert result.returncode == 0


def gpt_cli_test(command):
    os.environ["GPT_ASK_COMMANDS"] = "1"

    sys.argv[1:] = command.split(" ")
    if "--help" in command:
        with pytest.raises(SystemExit):
            cli()
    else:
        exit_code = cli()
        assert exit_code == 0


@pytest.mark.parametrize(
    "command",
    ARGS,
)
def test_gpt_cli(command, mock_openai):
    gpt_cli_test(command)
