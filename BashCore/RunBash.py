import os
import subprocess

def run_bash(script):
    script_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "Commands",
        script
    )

    script_path = os.path.abspath(script_path)

    result = subprocess.run(
        [script_path],
        capture_output=True,
        text=True
    )

    return result.stdout


