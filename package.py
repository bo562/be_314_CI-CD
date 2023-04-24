"""
py script that is used to package the current py src code for CodeBuild.
Used to update all AWS Lambdas on pushes to dev or main branch
"""
import os
import zipfile

# static variables
source = './src/py'
package_name = 'src_build.zip'
dir_excludes = ['.idea', 'venv', 'example', 'test']  # what directories should not be zipped
file_excludes = ['requirements.txt']  # what files should not be zipped

# define function to zip files
def package_src(src_path, filename):
    with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # walk through os and add files to zip
        for root, dirs, files in os.walk(src_path):
            # if the dir is a in the list of excluded directories remove it's subdirectories and skip
            if os.path.basename(root) in dir_excludes:
                dirs = [i for i in dirs if i not in dir_excludes]
                continue
            
            # prepare list of files that are not in the exclusion list
            files_to_zip = [i for i in files if i not in file_excludes]

            # write files to zip
            for file in files:
                zipf.write(os.path.join(root, file), os.path.join(os.path.relpath(root, os.path.commonprefix([src_path, root])), file))



if __name__ == '__main__':
    src_path = os.path.abspath(source)  # create absolute path

    # package defined src
    package_src(src_path, package_name)
    