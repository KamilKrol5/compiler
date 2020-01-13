#!/usr/bin/env bash

input="readme.md"

command="awk /^[^@]/' {print "'$0'"}' "${input}" | grep -o '"'```.*```'"' | grep -o '[^\`]*'"
#echo "${command}"
to_run=$(bash -c "${command}")
#echo "${to_run}"
wynik="wynik"$(date +%m-%d-%Y)".txt"
rm $wynik
while IFS= read -r line
do
    if [[ "$1" = "-all" ]]; then
        echo "___________________________________________________________________"
        echo "${line}"
        bash -c "${line}";
    else
        echo "___________________________________________________________________" >> $wynik
        echo "${line}" >> $wynik
        bash -c "${line}" | grep -o '[^?]*' | awk '
            /liczba rozkazów/ { print "commands count: " $6 }
            /koszt/ { print "total cost: " $4 }
            /Uruchamianie/ { print "results:"}
            />/ { print "> " $2 }
        ' >> $wynik;
    fi
done < <(echo "${to_run}")

