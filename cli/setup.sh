## IMPORTANT: this file and accompanying assets are the source for snippets in https://docs.microsoft.com/azure/machine-learning! 
## Please reach out to the Azure ML docs & samples team before before editing for the first time.

# <az_ml_install>
az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/sdk-cli-v2-public/ml-2.0.1a1-py3-none-any.whl
# </az_ml_install>

# <az_group_create>
az group create -n "azureml-examples-rg" -l "eastus"
# </az_group_create>

# <az_configure_defaults>
az configure --defaults group="azureml-examples-rg" workspace="main"
# </az_configure_defaults>

# <az_ml_workspace_create>
az ml workspace create
# </az_ml_workspace_create>

