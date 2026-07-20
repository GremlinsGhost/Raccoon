import subprocess

def run_bash(script_path: str):
    result = subprocess.run(
        [script_path],
        shell=False,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "ok": False,
            "error": result.stderr.strip() or "unknown error",
        }

    return {
        "ok": True,
        "output": result.stdout,
    }

