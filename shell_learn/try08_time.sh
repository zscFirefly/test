start_time=`date +"%s"`
i=1
while [ $i -le 5 ]
do
	let i++
	sleep 1
done
end_time=`date +"%s"`
let time=end_time-start_time
echo "Use time: ${time}s"
