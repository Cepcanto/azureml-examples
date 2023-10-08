This is a dummy pipeline job with anonymous reference for flow as component. 

Note that you will need to install a private version of cli and make sure that the compute cluster has the permission to access connections before you try to use this feature.

## for usage in office

When using in office, there are some more constraints:
1. office use `shrike` to do component prepare and register;
2. office need to sign components based on their snapshots;
3. office already has some requirements in their repository.

To meet the requirement, please install below private version packages and extensions:
```bash
python -m pip install shrike[build]==2.0.0dev9

# install this after shrike as shrike depends on a stable version
python -m pip install azure-ai-ml

python -m pip install mldesigner==0.0.105430780 --extra-index-url https://azuremlsdktestpypi.azureedge.net/test-sdk-cli-v2

# the private promptflow is to allow pandas >= 2.0.0
python -m pip install promptflow promptflow-tools

# note that all referred python scripts will be loaded during compile. Please use local package import instead of global import
python -m pip install bs4

# remove existed ml extension if you haven't installed the private version
az extension remove -n ml
az extension add ml
```

For global import issue, suppose below tool is referred in `flow.dag.yaml`:

```python
import bs4
from promptflow import tool

@tool
def prettify_string(response_text: str):
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    soup.prettify()
    return soup.get_text()[:2000]
```

As `bs4` has been imported globally, you'll need to install `bs4` to run `shrike.build.commands.prepare` or `mldesigner compile` on this flow.
If you don't want to install `bs4`, you can switch to use local import:

```python
from promptflow import tool

@tool
def prettify_string(response_text: str):
    import bs4
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    soup.prettify()
    return soup.get_text()[:2000]
```

Besides, `shrike` used a component_specification_glob to detect component specifications. For flow, you'll also need to detect `flow.dag.yaml`
so the glob must be updated. For example, you can use `**/*[sf][pl][eo][cw]*.yaml` instead of `**/*spec*.yaml`.