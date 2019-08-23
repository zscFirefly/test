
filename='user.txt'
IFS=$'\n'
for line in `cat $filename`
do
	username=`echo "$line" | awk '{print $1}'`
	password=`echo "$line" | awk '{print $2}'`
	echo "username:$username  password:$password"
done
