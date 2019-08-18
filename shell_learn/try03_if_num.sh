read -p "please input a number:" num

if [[ ! $num =~ ^[0-9]+$ ]];then
	echo "it is not a num"
	exit;
fi

echo "you number is $num"
