
"""
----------------------------------------------------------------------
Salesforce git file compare/diff tool across two branches
mchinnappan
----------------------------------------------------------------------
"""
import subprocess
import argparse
import traceback
import tempfile

import pyperclip


# Replace these with the commit hashes or branch names you want to compare

# example usage
# ~/treeprj [patch1] >
# python3  ~/.py/git_diff_file_two_branches.py --branch1=master --branch2=patch1 --filepath=docs/9.md


def main(): 
    desc =''' Get given file content in given 2 branches '''

    parser = argparse.ArgumentParser(description="Get content for a file from given 2 branches")
    parser.epilog = desc
    parser.add_argument("--branch1", default="main", help="branch1 (Default: main) ")
    parser.add_argument("--branch2", default="develop", help="branch2 (Default: develop)")
    parser.add_argument("--filepath", default="./README.md", help="File path for the file (Default: README.md)")
    parser.add_argument("--metadataType", default="profile", help="profile or permission set (Default: profile)")


    args = parser.parse_args()

    # Replace these with the commit hashes or branch names you want to compare
    branch1 = args.branch1 
    branch2 = args.branch2 
    file_path = args.filepath
    metadata_type = args.metadataType
    viz_reqd = False
    if metadata_type in ['profile', 'permission', 'package']: viz_reqd = True


    try:
        # checkout branch1
        print (f'=== Checking out {branch1} ===')
        checkout_branch1 = subprocess.check_output(
            ["git", "checkout", branch1 ]
        ).decode("utf-8").splitlines()


        with open(file_path, 'r') as input_file:
            # Create a temporary file and open it for writing
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                # Loop through the lines in the input file
                for line in input_file:
                    # Write the line to the temporary file
                    temp_file.write(line)

                # Print the name of the temporary file
                print('Temporary file name:', temp_file.name)


        if viz_reqd: 
            print ("=== Going to run xml transform...===")

            result = subprocess.run(['sfdx','mohanc:xml:transform', '-i', temp_file.name, '-m', metadata_type ], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))

        with open(temp_file.name, 'r') as f:
            file_content = f.read()
        pyperclip.copy(file_content)


        print(f'=== Contents of {temp_file.name} is copied into your clipboard. Opening the diff app... ===')
        print(f'=== ACTION REQUIRED: Paste the content into the diff app, once it opens up... and press [Enter] ===')
        result = subprocess.run(['open', 'https://mohan-chinnappan-n5.github.io/delta/diff.html'],  stdout=subprocess.PIPE)
        print(result.stdout.decode('utf-8'))
      

        input()
        print("=== Continuing with the program... ===")

        #-------------------------------       

        print (f'=== checking out {branch2} ===')   
        checkout_branch1 = subprocess.check_output(
            ["git", "checkout", branch2 ]
        ).decode("utf-8").splitlines()


        with open(file_path, 'r') as input_file:
            # Create a temporary file and open it for writing
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                # Loop through the lines in the input file
                for line in input_file:
                    # Write the line to the temporary file
                    temp_file.write(line)

                # Print the name of the temporary file
                print('Temporary file name:', temp_file.name)
        
        if viz_reqd:
            print ("going to run xml transform...")
            result = subprocess.run(['sfdx','mohanc:xml:transform', '-i', temp_file.name, '-m', metadata_type  ], stdout=subprocess.PIPE)
            print(result.stdout.decode('utf-8'))


        with open(temp_file.name, 'r') as f:
            file_content = f.read()
        pyperclip.copy(file_content)

        print(f'=== Contents of {temp_file.name} is copied into your clipboard. Goto the diff app... ===')
        print(f'===     ACTION REQUIRED: Paste the content into the diff app right side box ===')


    except:
        traceback.print_exc()

#===========
main()
