import subprocess
import itertools
import shutil
from pathlib import Path


to_replace = [
    ("request_type", "request_stage"),
    ("Request Type", "Request Stage"),
    ("RequestType", "RequestStage"),
    ("request\ type", "request\ stage"),
    ("requests\ types", "requests\ stages"),
    ("Requests\ Types", "Requests\ Stages"),
]

# to_replace = [
#     ("in (\"Finished\", \"Canceled\")", "== \"Colsed\""),
# ]


ftypes = ("html", "py")

this_script = Path(__file__)
back_up = __file__ + ".back"
shutil.copyfile(this_script, back_up)

for ftype, rep in itertools.product(ftypes, to_replace):
    print(f"replacing {rep[0]} with {rep[1]} in {ftype} files")
    try:
        command = f'find . -type f -name "*.{ftype}" -print0 | xargs -0 sed -i s/"{rep[0]}"/"{rep[1]}"/g'
        completed = subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(e.output)
        print(e.stderr)
        print(e.stdout)

    paths = Path(".").glob(f"**/*.{ftype}")
    for path in paths:
        path_name = path.as_posix()
        if rep[0] in path_name:
            new_fname = path_name.replace(rep[0], rep[1])
            new = path.rename(new_fname)
            print(f"renamed {path_name} to {new_fname}")

    # print(completed.stdout)

shutil.copyfile(back_up, this_script)
Path(back_up).unlink()
