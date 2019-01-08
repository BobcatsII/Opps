#!/bin/bash

deploy_data="/data/deploy_data"
script_path=$(cd "$(dirname "$0")"; pwd)
project_name=$1
version=$2
host=$3
types=$4
datestamp=$5
ansible_hosts="$script_path/ansible_files/app.hosts"
#datestamp=`date +'%s'`
user=root

if [ -z $version ];then
	echo "没有输入版本号,请重新部署"
	exit 1
fi

if [ "$datestamp" = "" ];then
    datestamp=`date +'%s'`
fi


if [[ "$types" == "app" ]];then
        package_name=${project_name}
        package_source="/data/deploy/upload_file"
        #package_tmp=`ls -d ${package_source}/*/*${project_name}*`
        package_file=`ls ${package_source}/${version}/*/*${project_name}*`
        bagtag=`echo $package_file |awk -F'.' '{print $NF}'`
        package_path="${package_file}"
	project_path="/opt/app/${project_name}"
        code_dir="/data/repos/$version/$project_name/"
        code_path="$code_dir/$project_name"".${bagtag}_""$datestamp"
        yaml_file="$script_path/ansible_files/app_again_${bagtag}.yaml"
elif [[ "$types" == "conf" ]];then
        package_source="/data/deploy/config_file"
        package_path=`ls ${package_source}/${version}/*${project_name}*/*.py`
        if [[ $project_name =~ "srs" ]];then
            package_name=${project_name}
            filename=`echo $package_path|awk -F'/' '{print $NF}'`
            project_path="/opt/pro/${project_name}/research/api-server"
            project_file="${project_path}/${filename}"
            code_dir="/data/repos/$version/$project_name/"
            code_path="$code_dir/${filename}_${datestamp}"
            yaml_file="$script_path/ansible_files/config_again.yaml"
#        elif [[ $project_name =~ "trans" ]];then
#            package_name=${project_name}
#            filename=`echo $package_path|awk -F'/' '{print $NF}'`
#            project_path="/opt/shell/live_record_task"
#            project_file="$project_path/$filename"
#            project_file_bak="${project_file}_bak"
#            code_dir="/data/repos/$version/$project_name/"
#            #code_path="$code_dir/$project_name"".py_""$datestamp"
#            code_path="$code_dir/${filename}_${datestamp}"
#            yaml_file="$script_path/ansible_files/trans.yaml"
        fi
fi

echo ""
echo "开始执行部署"
echo ""

ansible_vars="package_name=$package_name project_path=$project_path project_file=$project_file package_path=$package_path version=$version run_user=$user host=$host code_path=$code_path code_dir=$code_dir"
ansible-playbook -i $ansible_hosts -e "$ansible_vars" $yaml_file
if [ $? != 0 ];then
    echo "部署失败，联系运维"
    exit 1
fi

echo "部署成功"
exit 0
