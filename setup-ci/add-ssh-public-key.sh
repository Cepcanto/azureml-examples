
#!/bin/bash
set -e
# This script can be used to add a SSH public key to compute instance. This script can be used to add multiple SSH keys to compute instance.
# It can also be used to enable SSH from within virtual network using private IP for create on behalf of compute instances. 
# It takes the SSH public key as a parameter
sshkeystr="ssh-rsa ${1}"
cd /home/azureuser
echo "${sshkeystr}" >> temp.txt
cat temp.txt >> .ssh/authorized_keys2
