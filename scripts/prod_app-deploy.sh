#!/bin/bash
#example: bash /opt/pre-web-CI.sh prod passport 1.0.0

deploy_data="/data/deploy_data"
script_path=$(cd "$(dirname "$0")"; pwd)
project_name=$1
version=$2
host=$3
types=$4
datestamp=$5
ansible_hosts="$script_path/ansible_files/app.hosts"
datestamp=`date +'%s'`
user=root

if [ -z $version ];then
	echo "没有输入版本号,请重新部署"
	exit 1
fi

if [ "$datestamp" = "" ];then
    datestamp=`date +'%s'`
fi


if [[ "$types" == "app" ]];then
        package_source="/data/deploy/upload_file"
        package_tmp=`ls -d ${package_source}/*/*${project_name}*`
        pdir="/data/deploy/upload_file/${version}"
        bagtag=`echo $package_path |awk -F'.' '{print \$2}'`
        package_dir="${pdir}/${bagtag}"
        mkdir -p $package_dir
        mv $package_path $package_dir
        project_path="/opt/app/*${project_name}*"
        code_dir="/data/repos/$version/$project_name/"
        code_path="$code_dir/$project_name"_"$datestamp"
        yaml_file="$script_path/ansible_files/app_${bagtag}.yaml"
elif [[ "$types" == "conf" ]];then
        package_source="/data/deploy/config_file"
        package_path=`ls ${package_source}/${version}/*${project_name}*/*.py`
        if [[ $project_name =~ "srs" ]];then
            project_path="/opt/pro/${project_name}/research/api-server"
            code_dir="/data/repos/$version/$project_name/"
            code_path="$code_dir/$project_name"_"$datestamp"
            yaml_file="$script_path/ansible_files/config.yaml"
fi

echo ""
echo "开始执行部署"
echo ""

ansible_vars="package_name=$package_name project_path=$project_path package_path=$package_path version=$version run_user=$user host=$host code_path=$code_path code_dir=$code_dir"
ansible-playbook -i $ansible_hosts -e "$ansible_vars" $yaml_file
if [ $? != 0 ];then
    echo "部署失败，联系运维"
    exit 1
fi

echo "部署成功"
echo 0
