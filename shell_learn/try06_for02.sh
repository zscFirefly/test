read -p "please input username & password & num:" user pwd num

printf "=====================
username: $user
password: $pwd
num: $num
=====================
"

read -p "Are you sure?[y/n]" action
if [ $action != y  ];then
	echo "create user"
fi

for i in `seq -w $num`
do
	echo "username:$user$i"
	echo "password:$pwd"
	echo "$user created!"
done
