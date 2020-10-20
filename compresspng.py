import os, sys
import argparse


def compress(format, infile, outfile):
    outdir = os.path.dirname(outfile)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    print('compress %s to %s' % (infile, outfile))
    if format == 'pkm':
        outfile = os.path.dirname(outfile)
        command = "etcpack '%s' '%s' -c etc1 -ext PNG -as" % (infile, outfile)
        os.system(command)

        """
        # 带透明度的文件命名为name.pkm@alpha
        (dirpath, filename) = os.path.split(infile)
        alpha_path = os.path.join(outfile, filename)
        alpha_path = alpha_path.replace('.png', '_alpha.pkm')
        if os.path.isfile(alpha_path):
            new_path = alpha_path.replace('_alpha.pkm', '.pkm@alpha')
            os.rename(alpha_path, new_path)
        """

    elif format == 'pvr':
        command = "TexturePacker --format x2d '%s' --sheet '%s' --opt PVRTC4 --dither-fs-alpha  --premultiply-alpha --disable-rotation --size-constraints NPOT --border-padding 0 --shape-padding 0" % (
            infile, outfile)
        os.system(command)

    elif format == 'pvr.ccz':
        command = "TexturePacker --format x2d '%s' --sheet '%s'  --opt PVRTC4  --content-protection b23d9e45bd414cac37ea0e8a9dd6cf9d  --dither-fs-alpha  --premultiply-alpha --disable-rotation " \
                  "--size-constraints NPOT --border-padding 0 --shape-padding 0" % (
                      infile, outfile)
        os.system(command)


def main():
    parser = argparse.ArgumentParser(description='压缩png资源成各平台压缩纹理')
    parser.add_argument('-f', dest='format', help='输出纹理格式', required=True, choices=['pkm', 'pvr', 'pvr.ccz'])
    parser.add_argument(dest='inFile', help='需要压缩的资源，可以是png文件也可以是目录')
    parser.add_argument('-o', dest='OutFile', help='压缩后的资源路径，如果为空则在同级目录下创建名字相似的目录')
    args = parser.parse_args()

    compressFormat = args.format
    srcAsset = args.inFile
    dstAsset = args.OutFile

    if os.path.isdir(srcAsset):
        if not srcAsset[-1] == os.sep:
            srcAsset += os.sep

        if dstAsset is None:
            dstAsset = srcAsset[:-1] + "_" + compressFormat + os.sep
        else:
            if not dstAsset[-1] == os.sep:
                dstAsset += os.sep

        g = os.walk(srcAsset)
        for path, dir_list, file_list in g:
            for file in file_list:
                file_path = os.path.join(path, file)
                file_ext = os.path.splitext(file_path)[1]

                if file_ext == '.png':
                    dst_file_path = file_path.replace(srcAsset, dstAsset)
                    dst_file_path = dst_file_path.replace('png', compressFormat)

                    compress(compressFormat, file_path, dst_file_path)
    else:
        file_ext = os.path.splitext(srcAsset)[1]
        if file_ext == '.png':
            if dstAsset is None:
                dstAsset = os.path.dirname(srcAsset) + os.sep
            compress(compressFormat, infile=srcAsset, outfile=dstAsset)


if __name__ == '__main__':
    main()
