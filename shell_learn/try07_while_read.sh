
while read line
do
	let line=$line*100
	echo $line
done < num.txt
