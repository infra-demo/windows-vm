ip=$(cat vm-output.txt | grep Private_IP | cut -d '=' -f2 | awk '{$1=$1};1')
name=$(cat vm-output.txt | grep VM_Name | cut -d '=' -f2 | awk '{$1=$1};1')

ssh -t 'root@10.228.10.7' 'cd chef-repo && knife bootstrap windows winrm '$ip' -N '$name' -r recipe[WinAgents] -x '$username' -P '$password' -y '

