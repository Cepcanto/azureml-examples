# imports
import contextlib
import imp
import os
import json
import glob
import argparse
from pathlib import Path


@contextlib.contextmanager
def change_working_dir(path):
    """Context manager for changing the current working directory"""

    saved_path = os.getcwd()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(saved_path)

@contextlib.contextmanager
def replace_content(file, skip_wait=True):
    wait_str = "ml_client.jobs.stream(pipeline_job.name)"
    replace_holder = "## PLACEHOLDER"

    with open(file) as f:
        original_content = f.read()
    try:
        if skip_wait:
            with open(file, "w") as f:
                f.write(original_content.replace(wait_str, replace_holder))
        yield
    finally:
        if skip_wait:
            with open(file, 'w') as f:
                f.write(original_content)


def main(args):
    
    # get list of notebooks
    notebooks = sorted(glob.glob("**/*.ipynb", recursive=True))

    for notebook in notebooks:
        notebook = Path(notebook)
        folder = notebook.parent
        with change_working_dir(folder), replace_content(notebook.name, args.skip_wait):
            os.system(f"papermill {notebook.name} out.ipynb -k python")


if __name__ == "__main__":
    # setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-wait", type=bool, default=True)
    args = parser.parse_args()

    # call main
    main(args)