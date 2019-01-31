安装配置supervisor

1.安装python自动化工具    
    # yum install python-setuptools

2.安装supervisor
    # easy_install supervisor

3.测试安装是否成功 
    # echo_supervisord_conf

4.创建配置文件：
    (1)创建supervisor配置文件目录/etc/supervisor/  
        # mkdir -p /etc/supervisor/
    (2)创建主配文件supervisord.conf
        # echo_supervisord_conf > /etc/supervisor/supervisord.conf
    (3)创建项目配置文件目录(在/etc/supervisor/目录下)
        # mkdir conf.d

5.在配置文件目录中添加测试配置文件 
    如：/etc/supervisor/conf.d/opps.conf
    --------------------------------------
    eg:
    文本内容：
    [program:opps]
    command=pipenv run gunicorn -w 1 -b 0.0.0.0:5000 wsgi:app
    directory=/usr/local/2opps/
    user=root
    autostart=true
    autorestart=true
    startretries=10
    stopasgroup=true
    killasgroup=true
    redirect_stderr=true		#把stderr重定向到stdout文件，使日志保存在同一个文件里，默认不写为false
    --------------------------------------

    然后在主配置文件 supervisord.conf 里添加
		① 自定义socket文件路径
			[unix_http_server]
			file=/data/logs/supervisor/supervisor.sock
			
        ② supervisord应用配置
            [supervisord]
			logfile=/data/logs/supervisor/supervisord.log			#自定义supervisord日志
			loglevel=debug											#调试用debug，调试完成后用info，other：warn,trace
			pidfile=/data/logs/supervisor/supervisord.pid			#自定义pid文件路径
			childlogdir=/data/logs/supervisor						#自定义子项目日志生成路径
            environment=LC_ALL='en_US.UTF-8',LANG='en_US.UTF-8'		#让Pipenv里的Click可以正确处理编码问题
			
		③ supervisorctl连接配置
			[supervisorctl]
			serverurl=unix:///data/logs/supervisor/supervisor.sock	#指定连接的socket文件路径
		
        ④ #web管理界面登录验证
            [inet_http_server]
            port=0.0.0.0:9001
            username=linan
            password=linan123
        
        ⑤ 引入自定义配置文件
            [include]
            files = conf.d/*.conf

6.启动supervisor -- 手动启动
    # supervisord -c /etc/supervisor/supervisord.conf
    # pstree -p | grep supervisord
    查看supervisord.log发现program convert已启动
    # cat /tmp/supervisord.log

7.进入到supervisor管理界面
    # supervisorctl -c /etc/supervisor/supervisord.conf  
    几个命令：
        status 	查看状态
        stop opps 停止opps
        start opps 启动opps
        tail opps stderr		查看错误日志
        tail opps stdout	查看日志输出
        stop all	停止所有
        reload	重启监控服务（用于修改配置生效）
        help		查看所有可用命令
    注意：
        (1)每次修改配置文件后需进入supervisorctl，执行reload， 改动部分才能生效
        (2)两个命令
            supervisord : supervisor的服务器端部分，用于supervisor启动
            supervisorctl：启动supervisor的命令行窗口，在该命令行中可执行start、stop、status、reload等操作。
    当然也可以直接操作：
        # supervisorctl  reread	#重新读取配置
        # supervisorctl  update	#更新以便配置生效
        # supervisorctl  opps stop	#停止项目
        # supervisorctl  opps start	#启动项目
