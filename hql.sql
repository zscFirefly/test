use sgg;
create table stu(
id int,
name string
)row format delimited
fields terminated by '\t'


# 导入数据的三种方法
# 方法一：从本地load到表中
load data local inpath '/usr/local/data_temp/stu.txt' into table stu;

# 方法二：直接导入到hdfs中的warehouse中。
hadoop fs -put stu02.txt /user/hive/warehouse/sgg.db/stu

# 方法三：导入到hdfs后，再load到表中
hadoop fs -put stu01.txt /
load data inpath '/stu01.txt' into table stu; 


# JDBC连接hive
# 启动hiveserver 2
/hive/bin/hiveserver 2
# 启动beeline,账号root 无密码
/hive/bin/beeline
!connect jdbc:hive2://192.168.152.150:10000/default -n root 


# mysql -u hive -p hive123
# hive常用交互命令
hive -help # 查看hive用法
hive -e: sql from command line
hive -f: sql from files

hive -e "select * from sgg.stu"
hive -f ./hivef.sql > ./hive_result.txt

# hive 其他交互命令
# client中查看hdfs文件系统
hive> dfs -ls /;
# client中查看本地文件系统
hive> ! ls /;
# 查看hive中输入的所有历史命令
cd /root or cd /home/root
cat .hivehistory


# 其他配置操作

# 该文件夹里面有关于warehouse的配置，可以放到hive-site.xml里面。
cat hive/conf/hive-default.xml.template

# 增加以下配置到hive-site.xml里面可以打印库名跟表明。
<property>
    <name>hive.cli.print.header</name>
    <value>true</value>
</property>

<property>
    <name>hive.cli.print.current.db</name>
    <value>true</value>
</property>

# 日志管理
hive/conf/hive-log4j.properties.template
mv hive-log4j.properties.template hive-log4j.properties
# 修改存放位置
hive.log.dir=/hive/logs

# 参数设置
set mapred.reduce.tasks; # 打印默认值为-1
hive -hiveconf mapred.reduce.tasks=10 # 进入hive客户端，并且设置task值为10
set mapred.reduce.tasks=11 # 设置参数