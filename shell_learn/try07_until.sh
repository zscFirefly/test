
i=1
until [ $i -ge 101 ]
do
	let sum=$sum+$i
	echo $sum
	let i++
done
echo "sum:$sum"
