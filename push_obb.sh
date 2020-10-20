#!/bin/sh

usage(){
	echo "push_obb <版本号> <资源路径>"
}

curdir=$(dirname "$0")
version=$1

if [ -z "$version" ];then
	echo "请输入版本号"
	usage
	exit -1
fi

xfmain=$2
if [ -z $xfmain]; then
	echo "请输入资源路径"
	usage
	exit -1
fi

command -v adb >/dev/null 2>&1 || { echo >&2 "找不到adb命令，请把Android SDK中的adb命令加入到PATH中"; exit 1; }

# local_file="$curdir/build/outputs/expansion/xfmain.zip"
local_file=$xfmain
external_storage=$(adb "shell" "echo" "\$EXTERNAL_STORAGE")
obb_file="main.$version.com.ministone.game.risingsuperchef2.obb"
src_file="$external_storage/$obb_file"
dest_dir="$external_storage/Android/obb/com.ministone.game.risingsuperchef2/"

#echo "local_file = $local_file"
#echo "obb_file = $obb_file"
#echo "src_file = $src_file"
#echo "dest_dir = $dest_dir"

adb push $local_file $src_file
adb shell mkdir -p $dest_dir
adb shell mv $src_file $dest_dir
