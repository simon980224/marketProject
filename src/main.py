import subprocess
import sys
import os

def run_script(script_name):
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    scripts = ['005requests.py', '027requests.py']
    script_dir = '/Users/chenyaoxuan/Desktop/myproject/marketProject/src/'
    for script in scripts:
        script_path = os.path.join(script_dir, script)
        print(f"Running {script_path}...")
        output = run_script(script_path)
        print(f"Output from {script_path}:\n{output}")