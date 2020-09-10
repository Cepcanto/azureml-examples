import json
import glob

prefix='''# Azure ML Examples

[![run-notebooks-badge](https://github.com/Azure/azureml-examples/workflows/run-notebooks/badge.svg)](https://github.com/Azure/azureml-examples/actions?query=workflow%3Arun-notebooks)

Welcome to the Azure ML examples! This repository showcases the Azure Machine Learning (ML) service.

## Getting started

Clone this repository and install a few required packages:

```sh
git clone https://github.com/Azure/azureml-examples
cd azureml-examples
pip install -r requirements.txt
```

## Notebooks

Example notebooks are located in the [notebooks folder](notebooks).

path|scenario|compute|framework(s)|dataset|environment type|distribution|other
-|-|-|-|-|-|-|-
'''

suffix='''
## Contributing

We welcome contributions and suggestions! Please see the [Contributing Guidelines](CONTRIBUTING.md) for details.
'''

def write_workflows(ws='default', rg='azureml-examples', creds='${{secrets.AZ_AE_CREDS}}'):
    nbs = glob.glob('notebooks/**/*.ipynb', recursive=True)

    for nb in nbs:
        print()
        print(nb)

        name = nb.split('/')[-1].split('.')[0]

        workflow = f'''name: {name}
on: [push]
env:
  ml-ws: {ws}
  ml-rg: {rg}
jobs:
  build:
    runs-on: ubuntu-latest 
    steps:
    - name: check out repo
      uses: actions/checkout@v2
    - name: setup python
      uses: actions/setup-python@v2
    - name: pip install
      run: pip install -r requirements.txt
    - name: azure login
      uses: azure/login@v1
      with:
        creds: {creds}
    - name: install azmlcli
      run: az extension add -n azure-cli-ml
    - name: attach to workspace
      run: az ml folder attach -w ${{env.ml-ws}} -g ${{env.ml-rg}}
    - name: run notebook
      run: papermill {nb} out.ipynb -k python
    - name: upload notebook artifact
      uses: actions/upload-artifact@v2
      with:
        path: out.ipynb
'''

        with open(f'.github/workflows/{name}.yml', 'w') as f:
            f.write(workflow)


def write_readme():
    nbs = glob.glob('notebooks/**/*.ipynb', recursive=True)

    for nb in nbs:
        print()
        print(nb)
        with open(nb, 'r') as f:
            data = json.load(f)
        try:
            index_data = data['metadata']['index']
            print(index_data)

            scenario = index_data['scenario']
            compute = index_data['compute']
            frameworks = index_data['frameworks']
            dataset = index_data['dataset']
            environment = index_data['environment']
            distribution = index_data['distribution']
            other = index_data['other']

            row = f'[{nb}]({nb})|{scenario}|{compute}|{frameworks}|{dataset}|{environment}|{distribution}|{other}\n'
            prefix += row 
        except:
            print(f'Notebook: {nb} is missing metadata for building the index.')

    with open('README.md', 'w') as f:
        f.write(prefix+suffix)

#write_readme()
write_workflows()