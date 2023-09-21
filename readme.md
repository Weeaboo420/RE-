# **RE-Modding-Tools**
A collection of custom-made tools for making mod-making easier when dealing with games developed on Capcom's RE Engine.  

*(This has only been tested on Resident Evil 4 Remake)*

## **MDF-Exporter**
A tool that makes copies of a master MDF file and names those copies based on a user-specified list.  

**Usage:**

Download the latest release [here](https://github.com/Weeaboo420/RE-Modding-Tools/releases/tag/mdf-exporter)

Open the zip file and put `mdf-exporter.py` and `export.list` in the folder where the MDF files you want to replace are located. Example: `natives/stm/_Chainsaw/Character/ch/cha1/cha100/01/`

Copy the MDF file you have edited and would like to be your master MDF file and name it `"source.mdf2.32"`. If you want to use a different name then edit `mdf-exporter.py` and change the variable `SOURCE_FILENAME`.

Edit `export.list` with any text editor and put the names of all the MDF files you want to replace in there, for example:
```
cha100_01.mdf2.32
cha100_01b.mdf2.32
cha100_01c.mdf2.32
cha100_01d.mdf2.32
```

Now simply run `mdf-exporter.py` and it will ask you if you want to replace the files. Type "yes" to overwrite any existing files and you're done.

> [!NOTE]
> Due to how this program functions, you will have to repeat this process for each model's MDF files you want to replace. You could have multiple copies of `mdf-exporter.py` in say the root of the mod folder and use `RECURSIVE = True` and have different .list files for each copy of the .py file.

## **Mod-Packer**
A tool that automates the process of making a RAR file from your mod's files.
This tool can also ignore specified file types and directories which is useful for ignoring helper files and such.

**Requirements:**  

`patool`, a compact python library for managing file archives.
[http://wummel.github.io/patool/](http://wummel.github.io/patool/)

Windows installation:  
`python -m pip install patool` or `pip install patool`  

Windows Subsystem for Linux (WSL):  
`sudo pip install patool` or `sudo python -m pip install patool`  

**Usage:**

Download the latest release [here](https://github.com/Weeaboo420/RE-Modding-Tools/releases/tag/mod-packer)

Open the zip file and put `mod-packer.py` in the root of your mod, i.e. the folder that has `natives/`, `mod.jpg` and `modinfo.ini` in it.

Edit mod-packer.py with a text-editor and edit these parameters to your liking, use the included examples as a guide:  

**`USER_IGNORED_EXTENSIONS`**  
A list of extensions to ignore when making the mod archive.  
The extensions can be specified with or without a leading dot, the program will handle it automatically.

**`USER_IGNORED_FILES`**  
A list of files to ignore when making the mod archive.
> [!IMPORTANT]
> This will exclude **ANY** files that match the specified filenames, no matter what directory they are in.

**`USER_IGNORED_DIRECTORIES`**  
A list of directories to ignore when making the mod archive.  
A full file path is required starting from the folder that this file is located in. Example: `natives/stm/_Chainsaw/Character/ch/cha1/Blender` will ignore the folder `Blender` according to that local file path.

**`MOD_ARCHIVE_NAME`**  
The name and full local path of the output RAR archive.  
Since this is local you could have a file path like "../Mods/mymod.rar" and the archive will appear in that location relative to the root folder.