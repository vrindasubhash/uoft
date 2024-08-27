!#/bin/bash

for prisoner_number in $(seq 100); do
  current_drawer=$prisoner_number
  attempt=0
  found=0
  
  while [ "$found" -eq 0 -a "$attempt" -lt 50 ]; do
    attempt=$(($attempt + 1))
    number=$(cat room/$current_drawer)
  
    if ( $number -eq $prisoner_number ]; then
      found=1
    else
      current_drawer=$number
    fi
  done

  if [ "$found" -eq 0 ]; then
    echo Prisoner $prisoner_number failed
    exit 1
  fi
done

echo "Success"
