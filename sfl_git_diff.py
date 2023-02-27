
"""
-----------------------------------
Salesforce Delta Deployment tool
mchinnappan
-----------------------------------
"""
import subprocess
import argparse
import os
import traceback
import json
import datetime
import getpass

import compTypes
import const
import utils

class PackageUtil:
    def __init__(self, fromId, toId):
        # Instance attributes
        self.fromId = fromId
        self.toId = toId


    def summary(self, file_list):
        delete_count = 0
        modified_count = 0
        added_count = 0
        for filename in file_list:
            if (filename.startswith(".") == False and filename.endswith('.xml')):
                [operation, fname] = filename.split('\t')
                if operation == 'D': delete_count = delete_count + 1 
                if operation == 'M': modified_count = modified_count + 1 
                if operation == 'A': added_count = added_count + 1 
        return (added_count, modified_count, delete_count)

    def find_diff(self):
        try:


              # Get a list of all files that were changed between the two commits
            status_files = subprocess.check_output(
                ["git", "diff", "--name-status", self.fromId, self.toId]
            ).decode("utf-8").splitlines()

            (added_count, modified_count, delete_count) = self.summary(status_files)
            print(f'''
            XML files:
            Additions: {added_count}
            Modifications: {modified_count}
            Deletions: {delete_count}
            ''')

            # list deleted files only
            # git diff  --diff-filter=D --name-status  0d3ceb1..67ad11b


            # Get a list of all files that were changed between the two commits
            changed_files = subprocess.check_output(
                ["git", "diff", "--name-only", self.fromId, self.toId]
            ).decode("utf-8").splitlines()


             # Get a list of all files that were modified between the two commits
            modified_files = subprocess.check_output(
                ["git", "diff", "--diff-filter=M",
                    "--name-only", self.fromId, self.toId]
            ).decode("utf-8").splitlines()


            # Get a list of all files that were added between the two commits
            added_files = subprocess.check_output(
                ["git", "diff", "--diff-filter=A",
                    "--name-only", self.fromId, self.toId]
            ).decode("utf-8").splitlines()

            # Get a list of all files that were deleted between the two commits
            deleted_files = subprocess.check_output(
                ["git", "diff", "--diff-filter=D",
                    "--name-only", self.fromId, self.toId]
            ).decode("utf-8").splitlines()

            # Print the results
            changed = build_type_items(changed_files)
            added = build_type_items(added_files)
            deleted = build_type_items(deleted_files)
            modified = build_type_items(modified_files)

            return (changed, added, modified, deleted, status_files)
        except:
             traceback.print_exc()


def build_type_items(file_list):    
    changed = {}
    for filename in file_list:
        #- select only xml files 
        if (filename.startswith(".") == False and filename.endswith('.xml')):
            (ctype, member, ext, file_path) = find_component_type(filename)
            #print (ctype, member,ext, file_path)
            if (ctype != None and len(ctype.strip()) > 0) :
                if ctype in changed and changed[ctype] is not None:
                    changed[ctype].add(member)
                else:
                    changed.update({ctype : set()})
                    changed[ctype].add(member)
    return changed

 

#--- find the metadata component type for the given metadata file (full_path)
def find_component_type(file_path):
    # ref: https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_dashboard.htm?q=dashboard
    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    folder_item = file_path.split(os.sep)[-2]
    
    ctype = ''
    member = ''
    try:
        for key in compTypes.metadataTypes:
                search_for = '/' + key + '/'
                if (search_for in file_path) : 
                    ctype = compTypes.metadataTypes[key]
                    member = name.split('.')[0] 
                if ctype in compTypes.folder_reqd_items:
                    member =  folder_item + os.sep + name.split('.')[0]  
    except :
        traceback.print_exc()
 
    # return (cmp_type, dir_parts, dir_name, base_name, name, ext)
    return (ctype, member, ext, file_path)


#-- generate package xml
def gen_package_xml(items, fromId, toId):
    output = const.PKG_PREFIX 

    output = output + f'\t<!-- fromCommitId: {fromId} toCommitId: {toId} at {datetime.datetime.now()} by {getpass.getuser()} -->\n'

    for key in items:
        output = output + "\t<types>\n"
        output = output + "\t\t<name>" + key + "</name>\n"
        for member in items[key]:
            output = output + "\t\t<members>" + member + "</members>\n"
        output = output + "\t</types>\n"
    output = output + const.PKG_SUFFIX
    return output


def create_dirs_files(folder_path, file_name, content):
    # create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # create the file inside the folder
    file_path = os.path.join(folder_path, file_name)
    print (f'=== Writing into {file_path}... ====')
    with open(file_path, 'w') as f:
        f.write(content)

# ------------------
def main():

    description ='''
    ===============================
    Finds the changed files and deleted files from the given 
        fromCommit and toCommit and prepare:\n
        1. delta_package/package.xml for deployment\n
        2. delta_package/destructiveChanges/destructiveChanges.xml for destructiveChanges\n

    -------
    You can deploy using:\n
    sfdx force:source:deploy -u username@example.com -x delta_package/package.xml  --predestructivechanges delta_package/destructiveChanges/destructiveChanges.xml --testlevel RunLocalTests   -c --verbose --loglevel TRACE 
    =============================== 
    '''

    parser = argparse.ArgumentParser(description="SFLand git diff based package builder")
    parser.epilog = description
    parser.add_argument("--fromCommit", default="HEAD^", help="FROM CommitId (Default: HEAD^) ")
    parser.add_argument("--toCommit", default="HEAD", help="TO CommitId (Default: HEAD)")

    args = parser.parse_args()

    # Replace these with the commit hashes or branch names you want to compare
    fromId = args.fromCommit
    toId = args.toCommit

    pkgutil = PackageUtil(fromId, toId)
    (changed, added, modified, deleted, status_files) = pkgutil.find_diff()
    create_dirs_files('delta_package', 'package.xml', gen_package_xml(changed, fromId, toId))
    create_dirs_files('delta_package/added', 'package.xml', gen_package_xml(added, fromId, toId))
    create_dirs_files('delta_package/modified', 'package.xml', gen_package_xml(modified, fromId, toId))



    create_dirs_files('delta_package/destructiveChanges', 'destructiveChanges.xml', gen_package_xml(deleted, fromId, toId))
    create_dirs_files('delta_package/destructiveChanges', 'package.xml', const.EMPTY_PACKAGE_xml)

    json_output = json.dumps({"changed": changed, "deleted": deleted, "added": added, "modified": modified}, indent=4, default=utils.set_to_list) 
    create_dirs_files('delta_package', 'delta.json', json_output)

    for i in range(len(status_files)): status_files[i] = status_files[i].replace('\t',':')
    create_dirs_files('delta_package', 'status.json', json.dumps(status_files, indent=4))

    # metadata file
    metadata_ref = compTypes.read_metadata_file(f'https://raw.githubusercontent.com/mohan-chinnappan-n/cli-dx/master/delta/v{const.API_VERSION}.json')
    #print (json.dumps(metadata_ref, indent=4))





# -------------
main()


