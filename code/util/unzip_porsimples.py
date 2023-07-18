from zipfile import ZipFile
import os

########################################################################
#
#   Unzips PorSimples which is in the format:
#       - PorSimples/
#           - zh.zip
#           - folha.zip
#
#   "path" should point to the PorSimples directory as specified above
#   The PorSimples directory should already be unzipped manually prior
#
########################################################################

path = "/Users/ANONYMOUS/Downloads/Brazilian Portuguese/PorSimples"

def unzip_porsimples_dir(pathname, dirname):
    new_dir = os.path.join(pathname, dirname)
    zip_path = os.path.join(pathname, dirname + '.zip')
    if os.path.exists(pathname):
        os.makedirs(new_dir)
    with ZipFile(zip_path, 'r') as zipObject:
        zipObject.extractall(new_dir)
    dir_names = os.listdir(new_dir)[:]
    for filename in dir_names:
        new_sub_dir = os.path.join(new_dir, filename[:-4])
        new_zip_path = os.path.join(new_dir, filename)
        os.makedirs(new_sub_dir)
        with ZipFile(new_zip_path, 'r') as zipObject2:
            zipObject2.extractall(new_sub_dir)
        os.remove(new_zip_path)
    os.remove(zip_path)
        


unzip_porsimples_dir(path, 'zh')
unzip_porsimples_dir(path, 'folha')