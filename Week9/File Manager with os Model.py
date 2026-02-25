import os

def file_manager_demo():

    #display current directory
    current_dir= os.getcwd()
    print(f"Current Directory: {current_dir}\n")

    #create new folder
    folder_name= "lab_files"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print(f"Created Folder: {folder_name}")
    else:
        print(f"Folder '{folder_name}' already exsists")

    
    #create 3 empty text files
    file_names= ["file1.txt", "file2.txt", "file3.txt"]
    for file_name in file_names:
        file_path= os.path.join(folder_name, file_name)
        with open(file_path, 'w') as f:
            f.write(f"This is {file_name}")
        print(f"Created file: {file_name}")

    #list all files in folder
    print(f"\n---> Files in {folder_name} <---")
    files= os.listdir(folder_name)
    for file in files:
        print(f"- {file}")

    #rename file
    old_path= os.path.join(folder_name, "file2.txt")
    new_path= os.path.join(folder_name, "file20.txt")
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"\nRenamed 'file2.txt' to 'file20.txt'")

    #show files after renaming
    print(f"---> Files after renamed <---")
    files= os.listdir(folder_name)
    for file in files:
        print(f"- {file}")

    #cleanup-remove files and folder
    print("f\n---> Cleaning Up <---")
    for file in os.listdir(folder_name):
        file_path= os.path.join(folder_name, file)
        os.remove(file_path)
        print(f"Deleted: {file}")

    os.rmdir(folder_name)
    print(f"Removed Folder; {folder_name}")
    print("\nAll Cleanup Completed Successfully")


#Test Run
file_manager_demo()
