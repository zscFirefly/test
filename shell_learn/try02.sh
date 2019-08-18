file_path=/Users/reocar/Desktop/test_file/shell_learn/test_file/2.txt
file_path_bak=/Users/reocar/Desktop/test_file/shell_learn/back

if [ ! -f $file_path ];then
	echo "文件不存在"
	else
	if [ ! -d $file_path_bak ];then
		echo "文件不存在"
	else
		echo "文件存在"
	fi
fi
echo "开始备份..."
cp $file_path $file_path_bak
echo "备份完成"
