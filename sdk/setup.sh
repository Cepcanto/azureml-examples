#!/bin/bash

# <az_ml_sdk_install>
pip install --pre azure-ai-ml
# </az_ml_sdk_install>

# <mldesigner_install>
pip install mldesigner==0.1.0b5 --extra-index-url=https://azuremlsdktestpypi.azureedge.net/test-sdk-cli-v2/
# </mldesigner_install>

# <mltable_install>
pip install mltable
# </mltable_install>


# <az_ml_sdk_test_install>
pip install https://docsupport.blob.core.windows.net/ml-sample-submissions/1836020/azure_ai_ml-0.1.0b7-py3-none-any.whl
# </az_ml_sdk_test_install>

pip list
