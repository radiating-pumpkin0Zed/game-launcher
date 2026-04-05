import subprocess

def launch_game(wsl_path: str) -> None:
    result = subprocess.run(
            ["wslpath", "-w", wsl_path],
            capture_output=True,
            text=True
    )
    windows_path = result.stdout.strip()
    subprocess.Popen(
            ["cmd.exe", "/c", "start", "", windows_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
    )

