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

## **RE Engine Mod Assembler Tool**
A tool that streamlines the process of creating a finalized mod, without leftover unused assets and files.
This tool can ignore specified file types and directories as well as specific files.

**Usage:**

Download the latest release [here](https://github.com/Weeaboo420/RE-Modding-Tools/releases/tag/mod-assembler)

Open the zip file and put `RE Engine Mod Assembler Tool.exe` in the root of your mod, i.e. the folder that has `natives/`, `mod.jpg` and `modinfo.ini` in it.

Edit the included `settings.ini` file to your liking. "Empty" entries that do not have a traditional ini "value" must have an equals sign after them to be read properly, this is a limitation with the implementation of the ini reader. See the included default `settings.ini` file for examples on how to assign unwanted file extensions, folders and files.
