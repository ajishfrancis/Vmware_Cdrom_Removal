#!/bin/sh
input="/home/Ajish/orchestration/orchestration_inventory_phase/test.csv"
while IFS=',' read -r f1 f2 f3 f4 f5 f6 f7 f8
do
 if [[ $f1 == "windows" ]]
 then
   echo "$f2 ansible_ssh_user=$f3 ansible_ssh_pass=$f4" >> /home/windows.txt
 elif [[ $f1 == "linux" ]]
 then
  # echo "$f2" >> /home/linux.txt
   echo "$f2 ansible_ssh_user=$f3 ansible_ssh_pass=$f4" >> /home/linux.txt
 else
   # echo "$f2" >> /home/otheros.txt
   echo "$f2 ansible_ssh_user=$f3 ansible_ssh_pass=$f4" >> /home/otheros.txt
 fi

done < "$input"


