#!/bin/bash

# <az_ml_sdk_install>
pip install --pre azure-ai-ml
# </az_ml_sdk_install>

# <mldesigner_install>
pip install mldesigner
# </mldesigner_install>

# <mltable_install>
pip install mltable
# </mltable_install>


# <az_ml_sdk_test_install>
#pip install azure-ai-ml==0.1.0.b5
pip install azure-ai-ml==0.0.68331024 --extra-index-url=https://azuremlsdktestpypi.azureedge.net/azureml-v2-cli-e2e-test/68331024
# </az_ml_sdk_test_install>

pip list
