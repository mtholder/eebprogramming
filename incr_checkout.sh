#!/bin/sh

file_to_copy=$2
num_lines=`wc -l $1 | awk '{print $1}'`
curr_line=0


while true
do
	echo "Enter any line of text to proceed to the next checkout."
	read resp

	if test $resp = 'q'
	then
		break
	elif test $resp = 'b'
	then
		if test $curr_line -lt 2
		then
			echo "Can't go back, you are at the beginning!"
			continue
		else
			curr_line=`expr $curr_line - 1`
			echo "Backing up to the commit on line $curr_line"
		fi
	else
		curr_line=`expr $curr_line + 1`
	fi
	if test "${curr_line}" -gt "${num_lines}"
	then
		echo "Done!"
		break
	fi

	next_commit=`head -n${curr_line} $1 | tail -n1`

	git checkout ${next_commit}

	if ! test -z $2
	then
		cp ${file_to_copy} copy_${file_to_copy}
	fi
done

echo "You probably want to checkout master at this point!"
