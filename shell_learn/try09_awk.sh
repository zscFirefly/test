
while read line
do
	
	num=`echo $line | awk '{print$2}'`
	let num=$num*10
	echo $num
done < user.txt
