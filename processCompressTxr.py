import shutil,os,sys


def moveToOtherDir(root_dir, common_dir_name, commonType, compress_dir_name, compressType, temp_dir_name):
    """
    将通用纹理移动到临时目录，将压缩纹理移动到通用目录
    :param root_dir:            资源总目录
    :param common_dir_name:     通用资源目录名
    :param commonType:          通用资源后缀
    :param compress_dir_name:   压缩资源目录名
    :param compressType:        压缩资源猴嘴
    :param temp_dir_name:       临时资源目录名
    :return:
    """
    compress_dir_path = os.path.join(root_dir, compress_dir_name)
    if os.path.isdir(compress_dir_path):
        g = os.walk(compress_dir_path)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                # 压缩纹理路径
                compress_file_path = os.path.join(path, file_name)
                # 压缩纹理对应的通用纹理路径
                common_file_path = compress_file_path.replace(compress_dir_name, common_dir_name)
                common_file_path = common_file_path.replace(compressType, commonType)

                if os.path.isfile(common_file_path):
                    # 通用纹理的临时存储路径
                    temp_file_path = common_file_path.replace(common_dir_name, temp_dir_name)
                    temp_dir_path = os.path.dirname(temp_file_path)
                    if not os.path.isdir(temp_dir_path):
                        os.makedirs(temp_dir_path)
                    # 将通用资源移动到临时目录
                    print("Move %s to %s" % (common_file_path, temp_dir_path))
                    shutil.move(common_file_path, temp_dir_path)
                    # 将压缩纹理移动到通用路径
                    print("Move %s to %s" % (compress_file_path, os.path.dirname(common_file_path)))
                    shutil.move(compress_file_path, os.path.dirname(common_file_path))


def revertToOriginDir(root_dir, common_dir_name, commonType, compress_dir_name, compressType, temp_dir_name):
    """
        将压缩纹理从通用目录先移动到压缩目录，再将临时目录下的通用资源移动会通用目录
        :param root_dir:            资源总目录
        :param common_dir_name:     通用资源目录名
        :param commonType:          通用资源后缀
        :param compress_dir_name:   压缩资源目录名
        :param compressType:        压缩资源猴嘴
        :param temp_dir_name:       临时资源目录名
        :return:
    """
    temp_dir_path = os.path.join(root_dir, temp_dir_name)
    if os.path.isdir(temp_dir_path):
        is_tempDir_empty = True
        g = os.walk(temp_dir_path)
        for path, dir_list, file_list in g:
            for file_name in file_list:
                # 通用纹理路径当前的路径（tempDir）
                temp_file_path = os.path.join(path, file_name)

                # 压缩纹理当前的路径（sd)
                compress_file_path = temp_file_path.replace(temp_dir_name, common_dir_name)
                compress_file_path = compress_file_path.replace(commonType, compressType)

                if os.path.isfile(compress_file_path):
                    # 压缩纹理本来的位置
                    compress_file_origin_path = compress_file_path.replace(common_dir_name, compress_dir_name)
                    compress_file_origin_dir = os.path.dirname(compress_file_origin_path)
                    if not os.path.isdir(compress_file_origin_dir):
                        os.makedirs(compress_file_origin_dir)
                    # 将通用资源移动到临时目录
                    shutil.move(compress_file_path, compress_file_origin_dir)
                    print("Move %s to %s" % (compress_file_path, compress_file_origin_dir))
                    # 将压缩纹理移动到通用路径
                    shutil.move(temp_file_path, os.path.dirname(compress_file_path))
                    print("Move %s to %s" % (temp_file_path, os.path.dirname(compress_file_path)))
                else:
                    is_tempDir_empty = False

        if is_tempDir_empty:
            # 如果tempDir中没有其它资源，则删除文件夹
            shutil.rmtree(temp_dir_path)


def main():
    if len(sys.argv) == 8:
        action = sys.argv[1]
        rootDir = sys.argv[2]
        commonDir = sys.argv[3]
        commonType = sys.argv[4]
        compressDir = sys.argv[5]
        compressType = sys.argv[6]
        tempDir = sys.argv[7]

        if action == "move":
            moveToOtherDir(rootDir, commonDir, commonType, compressDir, compressType, tempDir)
        elif action == "revert":
            revertToOriginDir(rootDir, commonDir, commonType, compressDir, compressType, tempDir)


if __name__ == '__main__':
    main()

