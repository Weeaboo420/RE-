from pathlib import PurePath as parsePath
from os import getcwd as getCwd
from os import walk as exploreReursive
from os import scandir as scanDirectory
from os.path import isfile as fileExists
from os import remove as deleteFile
from shutil import copyfile as copyFile

SOFTWARE_VERSION = "1.0 (September 21 2023)"
SOURCE_FILENAME = "source.mdf2.32"
EXPORT_LIST_FILENAME = "export.list"
RECURSIVE = False

#---Special Functions------------------------------------------------------------------------------------------------------------------------------------------------
def RewriteOrCreateExportFiles():
    print("")
    with open(EXPORT_LIST_FILENAME) as exportList:
        
        filePaths = []
        filesToModify = []
        exportFilenames = []
        
        if RECURSIVE:            
            rootSubDirectories = GetSubdirectories(getCwd())        
            for rootSubDirectory in rootSubDirectories:
                for path, subdirectories, filenames in exploreReursive(rootSubDirectory):
                    for filenameEntry in filenames:        
                        filePaths.append(str(parsePath(path, filenameEntry)).strip())                                              
                        
        for filename in exportList.readlines():
            exportFilenames.append(filename.strip())
        
        if RECURSIVE:
            for f in filePaths:
                for e in exportFilenames:
                    if e in f:
                        filesToModify.append(f)
                
        else:
            for entry in exportFilenames:
                filesToModify.append(entry)                
    
    for entry in filesToModify:
        rewritten = False
        if FileExists(entry):
            deleteFile(entry)
            rewritten = True

        copyFile(SOURCE_FILENAME, entry)

        msg = ""
        if rewritten:
            msg = f"Rewrote file \"{entry}\""                        
        else:
            msg = f"Created file \"{entry}\""

        print(msg)
            
    print("\n...Done")    
    input("Press [RETURN] to exit: ")
    exit()

#---IO Functions-----------------------------------------------------------------------------------------------------------------------------------------------------
def GetSubdirectories(path):
    subdirectories = []
    
    with scanDirectory(path) as scan:
        for entry in scan:
            if entry.name[0] != "." and entry.is_dir():
                subdirectories.append(entry.name)
    
    return subdirectories

def FileExists(filename, recursive=False):
    if not recursive:
        return fileExists(filename)
    else:
        #List all files in every subdirectory recursively, excluding the directory where this file is located
        rootSubDirectories = GetSubdirectories(getCwd())
        
        for rootSubDirectory in rootSubDirectories:
            for path, subdirectories, filenames in exploreReursive(rootSubDirectory):
                for filenameEntry in filenames:
                    if filenameEntry == filename:
                        return fileExists(parsePath(path, filenameEntry))

def ValidateFile(filename, description=""):
    if not FileExists(filename):
        print(f"\nERROR: The {description}file \"{filename}\" does not exist or is not named correctly.\n")
        input("Press RETURN to exit... ")
        exit()

#---Main Function----------------------------------------------------------------------------------------------------------------------------------------------------
def Run():
    print(f"\n---[RE-Engine MDF-Exporter | written by SpaceDoggo/Weeaboo420Fgt v{SOFTWARE_VERSION}]---")
    
    recursive_display = "ON" if RECURSIVE else "OFF"
    print(f"   Recursive mode: {recursive_display}")

    ValidateFile(SOURCE_FILENAME, "source ")
    ValidateFile(EXPORT_LIST_FILENAME, "export ")
    print(f"   Using input file \"{SOURCE_FILENAME}\"\n")

    overwritePrompt = True
    while(overwritePrompt):
        print(f"This will overwrite any existing files specified inside \"{EXPORT_LIST_FILENAME}\" with the contents of the file \"{SOURCE_FILENAME}\"")
        choice = input("Is this ok (y/n)? ")

        if len(choice) > 0:
            choice = choice.lower()
            if choice == "n" or choice == "no":
                print("See you, Space Cowboy...\n")
                exit()

            elif choice == "y" or choice == "yes":
                RewriteOrCreateExportFiles()
                
#---Program start----------------------------------------------------------------------------------------------------------------------------------------------------
Run()