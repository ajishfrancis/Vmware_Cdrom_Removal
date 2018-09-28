
nol=$(cat "/home/Ajish/orchestration/orchestration_inventory_phase/sonal.csv" | wc -l)
 x=1
 while  [ $x -le "$nol" ]
 do
     line=($(sed -n "$x"p "/home/Ajish/orchestration/orchestration_inventory_phase/sonal.csv)
     echo ""${line[1]}" "${line[3]}""  >> out.txt
     x=$(( $x + 1 ))
 done
