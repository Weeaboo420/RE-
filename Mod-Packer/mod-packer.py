try:
    import patoolib
    import datetime
    from os import walk, remove as deleteFile, name as osName
    from os.path import join as parsePath, exists as fileExists
except Exception as importError:
    print("Import error:\n")
    print(f"{importError}\n\n")
    input("Press RETURN to exit... ")
    exit()

SOFTWARE_VERSION = "1.0 (September 21 2023)"
MOD_ARCHIVE_EXTENSION = ".rar"

SAFE_MODE = True
SUPPRESS_OUTPUT = True
PAUSE_MODE = True
USER_IGNORED_EXTENSIONS = [".py", ".rar", ".txt", "blend", "blend1", ".fbx", ".tga", ".dds", ".png", ".obj", ".mtl"]
USER_IGNORED_FILES = ["source.mdf2.32", "help_ALBD.tex.143221013", "NullATOS.tex.143221013"] #Will replace ANY files that have matching filenames
USER_IGNORED_DIRECTORIES = ["natives/stm/_Chainsaw/Character/ch/cha1/Blender"] #Ignores specified directories and their subdirectories
MOD_ARCHIVE_NAME = "../../Mods/FFX Rikku over Ashley.rar" #The local path and filename of the mod archive. Must be .rar
OS_PATH_STANDARD = "/" #Do not modify unless you are having issues.

def MakeSafeCopy(fileName):
    #Get file extension part
    ext = ""
    for char in reversed(fileName):
        ext += char
        if char == ".":
            break
            
    #Reverse the extension part
    ext = f"{ext}"[::-1]
    
    #Get the current time and make it into a string the OS can accept in a filename
    dateString = datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    
    #Remove the extension part from MOD_ARCHIVE_NAME using slice
    newFileName = fileName[0:len(fileName)-1 - (len(ext)-1)]
    newFileName += f"_{dateString}{ext}"
    return newFileName

def ShowParameterUsedYesNo(parameter):
    if type(parameter) == bool:
        return "YES" if parameter else "NO"

def Main():
    global MOD_ARCHIVE_NAME    
    if MOD_ARCHIVE_EXTENSION not in MOD_ARCHIVE_NAME:
        print("ERROR: Invalid Mod archive name (dot not found specifying file extension)\n")
        exit()          
    
    print(f"\n---[RE-Engine Mod-Packer | written by SpaceDoggo/Weeaboo420Fgt v{SOFTWARE_VERSION}]---")
    print(f"   Safe Mode: {ShowParameterUsedYesNo(SAFE_MODE)} | Suppressed output: {ShowParameterUsedYesNo(SUPPRESS_OUTPUT)} | Pause mode: {ShowParameterUsedYesNo(PAUSE_MODE)}\n")

    ignoredExtensions = [] #List will get cleaned up based on USER_IGNORED_EXTENSIONS, leading dots will be removed.
    filesToPack = []
    
    #Remove empty entries in USER_IGNORED_DIRECTORIES
    for index, dir in enumerate(USER_IGNORED_DIRECTORIES):
        if len(str(dir)) <= 0:
            del USER_IGNORED_DIRECTORIES[index]       
            
    for index, ext in enumerate(USER_IGNORED_EXTENSIONS): #Remove any empty extensions inside USER_IGNORED_EXTENSIONS
        if len(str(ext)) <= 0:
            del USER_IGNORED_EXTENSIONS[index]

    if len(USER_IGNORED_EXTENSIONS) <= 0:
        print("   WARNING: No ignored extensions found")
    else:
        for ext in USER_IGNORED_EXTENSIONS:
            if ext[0] == ".": #Remove dot from beginning of extension if it exists
                newExt = ""
                for char in range(1, len(ext)):
                    newExt = newExt+(ext[char])
                ignoredExtensions.append(newExt)
            else:
                ignoredExtensions.append(ext)
                
        #Remove any duplicate extensions
        ignoredExtensions = list(dict.fromkeys(ignoredExtensions))

        #Convert every element in ignoredExtensions to strings, removes the need to do it elsewhere when needed
        for index, ext in enumerate(ignoredExtensions):
            ignoredExtensions[index] = str(ext)

        print("Ignored extensions: ", end="")
        for index, ext in enumerate(ignoredExtensions):
            print(ext, end="")
            if index < len(ignoredExtensions)-1:
                print(", ", end="")
            else:
                print("")

    #Get a list of all files that will be added, starting from the current directory 
    #and listing every file recursively down the file tree inside all subdirectories
    ignoredDirs = []
    for root, subDirs, fileNames in walk("."):
        
        addFile = True
        root = root.strip(f".{OS_PATH_STANDARD}")
        
        #Skip any directories that match USER_IGNORED_DIRECTORIES
        for dir in USER_IGNORED_DIRECTORIES:
            if dir in root:                
                addFile = False
                ignoredDirs.append(dir)
                break
        
        if addFile:
            for fileName in fileNames:            
                    filesToPack.append(parsePath(root, fileName))
    
    #Print text showing no. of ignored directories via USER_IGNORED_DIRECTORIES
    if len(ignoredDirs) > 0:
        ignoredDirs = list(dict.fromkeys(ignoredDirs))
        print(f"Ignored directories: {len(ignoredDirs)}")
    
    #Remove files that have extensions matching the list of extensions to ignore
    tempList = filesToPack.copy() #Transfer the content of filesToPack to a temp list, 
    filesToPack.clear()           #otherwise it gets all fucked when trying to remove files properly
    
    for file in tempList:
        fileNameParts = file.split(".")
        if type(fileNameParts) is list:
            if len(fileNameParts) > 0:
                fileExt = fileNameParts[len(fileNameParts)-1]                
                
                #Compare extension of file to that of the list of extensions to ignore,
                #remove the file if there is a match
                skipFile = False
                for ext in (ignoredExtensions):
                    if fileExt.strip() == ext.strip():                        
                        skipFile = True
                        break
                
                if not skipFile:
                    filesToPack.append(file)
    
    #Remove specific files specified in USER_IGNORED_FILES
    if len(USER_IGNORED_FILES) > 0:
        for index, file in enumerate(USER_IGNORED_FILES): #Remove any surrounding whitespace as a precaution
            USER_IGNORED_FILES[index] = file.strip()
        
        tempList = filesToPack.copy()
        filesToPack.clear()
                
        for file in tempList:
            skipFile = False
            tempFileParts1 = file.split(OS_PATH_STANDARD)
            fileName = tempFileParts1[len(tempFileParts1)-1]
            
            for ignoredFile in USER_IGNORED_FILES:               
                tempFileParts2 = ignoredFile.split(OS_PATH_STANDARD)
                ignoredFile = tempFileParts2[len(tempFileParts2)-1]
                
                if ignoredFile == fileName:                    
                    skipFile = True
                    break
           
            if not skipFile:
                filesToPack.append(file)
    
    deletedFile = False
    if fileExists(MOD_ARCHIVE_NAME):
        if SAFE_MODE:           
            print("")
            while(True):
                choice = input(f"The archive \"{MOD_ARCHIVE_NAME}\" already exists. Delete it (Y/N)? ")
                choice = choice.lower()
                if choice == "y":
                    deleteFile(MOD_ARCHIVE_NAME)
                    deletedFile = True
                    break
                elif choice == "n":                    
                    MOD_ARCHIVE_NAME = MakeSafeCopy(MOD_ARCHIVE_NAME)
                    
                    while(True):
                        if fileExists(MOD_ARCHIVE_NAME):
                            MOD_ARCHIVE_NAME = MakeSafeCopy(MOD_ARCHIVE_NAME)
                        else:
                            break
                    
                    break
        else:
            deleteFile(MOD_ARCHIVE_NAME)
        
    #Fix Windows Path issue when creating rar archive
    if osName == "nt":
        tempList = []
        
        for fileName in filesToPack:
            parts = fileName.split("\\")            
            fixedFile = ""
            for index, char in enumerate(parts):
                fixedFile += char
                if index < len(parts)-1 and index > 0:
                    fixedFile += "/"
            tempList.append(fixedFile)
            
        filesToPack = tempList.copy()
    
    if len(filesToPack) == 0:
        print("\nNo files to pack into archive. Double check the ignored extensions and directories inside this file.")
        input("\nPress RETURN to exit...")
        exit()

    #Create the archive using patoolib
    archiveCreated = False
    try:
        #Set verbosity. -1 = quiet, 0 = normal
        verboseLevel = -1 if SUPPRESS_OUTPUT else 0
        if verboseLevel == 0:
            print("")
        patoolib.create_archive(MOD_ARCHIVE_NAME, filesToPack, verboseLevel)
        archiveCreated = True
    except Exception as error:
        print(f"Something went wrong when trying to create the archive \"{MOD_ARCHIVE_NAME}\".\nPlease ensure that the file format is RAR (.rar) for optimal compatibility.")
        
        if not SUPPRESS_OUTPUT:
            print(f"\n\n{error}")

    if archiveCreated:
        print(f"\n\nRAR archive created successfully - Saved as \"{MOD_ARCHIVE_NAME}\"")
        if SAFE_MODE and not deletedFile:
            print("\nAdded date and time to end of filename because SAFE_MODE is enabled. Disable to allow for deletion of the old mod archive during export.\n")

    if PAUSE_MODE:
        print("Pause mode is enabled. Set it to \"False\" to prevent this window from appearing and just export unless interaction is needed.")
        input("Press RETURN to exit... ")

#---Program start----------------------------------------------------------------------------------------------------------------------------------------------------
Main()