import subprocess, sys
commands = [
    ['python3','tools/stage_step10_corrections.py','--check'],
    ['python3','tools/review_step10_delivery.py','--check'],
    ['python3','tools/finalize_step10_corrections.py','--check'],
    ['python3','tools/build_navigation.py','--check'],
    ['python3','tools/verify_step10_content.py','reader'],
    ['python3','tools/verify_step10_content.py','baseline'],
    ['python3','-m','unittest','discover','-s','tools','-p','test_*.py'],
]
for command in commands:
    print('COMMAND', command, flush=True)
    result = subprocess.run(command)
    if result.returncode: sys.exit(result.returncode)
