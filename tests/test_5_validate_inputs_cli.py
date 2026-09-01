# SPDX-FileCopyrightText: 2025 German Aerospace Center, Gabriel Möring-Martínez
# SPDX-License-Identifier: MIT

import subprocess
import sys


def test_validate_inputs_cli():
    """
    Test that input validation can be executed through the command-line interface.

    The test runs ZEVAMPY with the --validate-inputs option and verifies that:
    - The command exits successfully.
    - A successful validation message is printed.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "zevampy.cli",
            "--config",
            "config.yaml",
            "--validate-inputs",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"CLI input validation failed:\n{result.stderr}"
    )

    combined_output = result.stdout + result.stderr

    assert "Input validation successful." in combined_output