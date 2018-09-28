#!/bin/sh
mkdir /home/Inventory/
input="/home/Ajish/orchestration/orchestration_inventory_phase/test.csv"
while IFS=',' read -r f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12
do
 if [[ $f1 == "windows" ]]
 then
   echo "$f2 ansible_ssh_user=$f3 ansible_ssh_pass=$f4 ansible_ssh_port=$f5 ansible_connection=$f6 ansible_winrm_server_cert_validation=$f8 name=$f9 password=$f10" >> /home/Inventory/windows.yml
 elif [[ $f1 == "linux" ]]
 then
  # echo "$f2" >> /home/linux.txt
   echo "$f2 ansible_ssh_user=$f3 ansible_ssh_pass=$f4 ansible_ssh_port=$f5 ansible_connection=$f6 host_key_checking=$f7" >> /home/Inventory/linux.ini
 else
   # echo "$f2" >> /home/otheros.txt
   echo "$f2 ansible_ssh_user=$f3 ansible_ssh_pass=$f4" >> /home/Inventory/otheros.ini
 fi

done < "$input"


