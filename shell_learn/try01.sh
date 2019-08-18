read -p "Please input number:" num

while true
do
	if [[ $num =~ ^[0-9]+$ ]];then
		break
	else
		read -p "it is not a num,try again:" num
	fi

done


echo "you num is:" $num
