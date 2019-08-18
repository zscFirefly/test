read -p "Please input a num:" num
case $num in
"2")	
	let k=num*2
	echo $k
;;
"3")	
	let k=$num*3
	echo $k
;;
*)
	echo "error"
esac
echo "End!!"
