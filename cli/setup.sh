# <az_ml_install>
#az extension add -n ml -y
# </az_ml_install>

# rc install - uncomment and adjust below to run all tests on a CLI release candidate
az extension remove -n ml

# dev build
az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/azureml-v2-cli-e2e-test/60866320/ml-0.0.60866320-py3-none-any.whl --pip-extra-index-urls https://azuremlsdktestpypi.azureedge.net/azureml-v2-cli-e2e-test/60866320 --yes
# az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/test-sdk-cli-v2/ml-0.0.60488751-py3-none-any.whl --yes
# update when have nightly build for april features
# az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/sdk-cli-v2/ml-0.0.60376978-py3-none-any.whl --yes
# az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/sdk-cli-v2-public/ml-2.2.1-py3-none-any.whl --yes
 
# <set_variables>
GROUP="azureml-examples"
LOCATION="eastus"
WORKSPACE="main"
# </set_variables>

# <az_configure_defaults>
az configure --defaults group=$GROUP workspace=$WORKSPACE location=$LOCATION
# </az_configure_defaults>
