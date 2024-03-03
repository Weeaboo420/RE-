//The C++17 standard is required (mainly because of <filesystem>)
//Compile with -std=c++17

#include <filesystem>
#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

//mINI provided by metayeti on Github, https://github.com/metayeti/mINI
#define MINI_CASE_SENSITIVE
#include "include/ini.h"

//Internal settings and defaults
#define VERSION               "v1.0 March 3rd 2024"
#define SETTINGS_INI_FILENAME "settings.ini"

#define INI_MAIN              "main"
#define INI_EXTS              "ignored_extensions"
#define INI_FILES             "ignored_files"
#define INI_DIRS              "ignored_folders"

#define INI_ROOT              "root_directory"
#define INI_ROOT_DIR          "./"
#define INI_OUTPUT            "output_directory"
#define INI_OUTPUT_DIR        "../RE_ENGINE_MOD_ASSEMBLER_TOOL_OUTPUT"

namespace fs = std::filesystem;

bool file_exists(const std::string& path)
{
	return fs::exists(path);
}

bool is_whitespace(const std::string& str)
{
	if(str.size() == 0)
	{
		return true;
	}

	return std::all_of(str.begin(), str.end(), isspace);
}

std::string remove_leading_dot(const std::string& str)
{
	std::string new_str;
	bool add_char = false;

	for(int i = 0; i < str.size(); i++)
	{
		if(add_char)
		{
			new_str += str[i];
		}
		
		else
		{
			//The first dot has been found, all following characters may be added.
			if(str[i] == '.')
			{
				add_char = true;
			}
		}
	}

	return new_str;
}

std::vector<fs::directory_entry> get_files_and_subdirectories(const std::string& path)
{
	std::vector<fs::directory_entry> fs_entries;

	//Iterate over all file system entries specified in "path" recursively
	for(const auto& entry : fs::recursive_directory_iterator(path))
	{
		fs_entries.push_back(entry);
	}

	return fs_entries;
}

std::vector<fs::directory_entry> filter_files(const std::vector<fs::directory_entry>& fs_entries, const mINI::INIStructure& ini_settings)
{
	std::vector<fs::directory_entry> filtered_entries;
	std::vector<std::string> ignored_files;

	//Extract filenames from the ini file that will be ignored, specified under [ignored_files]
	//First the file itself has to be iterated through, each iterator contains a section
	//and the corresponding data inside the section, first and second respectively.
	for(const auto& it : ini_settings)
	{
		const auto& section = it.first;
		const auto& data = it.second;

		//Make sure the right section is being read, "ignored_files"
		if(section == INI_FILES)
		{
			for(const auto& row : data)
			{
				ignored_files.push_back(row.first);
			}
		}
	}

	//Iterate through the filesystem entries, filtering out the unwanted files.
	for(const auto& entry : fs_entries)
	{
		//Make sure a file is being looked at, and not a directory
		if(!entry.is_directory())
		{
			bool add_file = true;

			for(const auto& ignored_file : ignored_files)
			{
				if(ignored_file == entry.path().generic_string())
				{
					add_file = false;
					break;
				}
			}

			if(add_file)
			{
				filtered_entries.push_back(entry);
			}
		}

		//Add all directories, the only concern of this function is filtering
		//out specific unwanted files.
		else
		{
			filtered_entries.push_back(entry);
		}
	}

	return filtered_entries;
}

std::vector<fs::directory_entry> filter_directories(const std::vector<fs::directory_entry>& fs_entries, const mINI::INIStructure& ini_settings)
{
	std::vector<fs::directory_entry> filtered_entries;
	std::vector<std::string> ignored_folders;

	//Extract folders from the ini file under the header [ignored_folders]
	//First the file itself has to be iterated through, each iterator contains a section
	//and the corresponding data inside the section, first and second respectively.
	for(const auto& it : ini_settings)
	{
		const auto& section = it.first;
		const auto& data = it.second;

		//Make sure the right section is being read, "ignored_folders"
		if(section == INI_DIRS)
		{
			//Iterate over each key-value pair, in this case only extract
			//the key since that contains the actual directory address.
			for(const auto& row : data)
			{
				ignored_folders.push_back(row.first);
			}
		}
	}

	//Filter out directories based on the specifications in the ini file.
	for(const auto& entry : fs_entries)
	{
		//Make sure the current file system entry being looked at is
		//a directory and not a file.
		if(entry.is_directory())
		{
			bool add_directory = true;

			for(const auto& ignored_folder : ignored_folders)
			{
				if(entry.path().generic_string() == ignored_folder)
				{
					add_directory = false;
					break;
				}
			}

			if(add_directory)
			{
				filtered_entries.push_back(entry);
			}
		}

		//Add any files since this function is only concerned with
		//filtering out unwanted directories.
		else
		{
			filtered_entries.push_back(entry);
		}
	}


	return filtered_entries;
}

std::vector<fs::directory_entry> filter_extensions(const std::vector<fs::directory_entry>& fs_entries, const mINI::INIStructure& ini_settings)
{
	std::vector<fs::directory_entry> filtered_entries;
	std::vector<std::string> ignored_extensions;

	//Extract extensions from the ini file under the header [ignored_extensions]
	//First the file itself has to be iterated through, each iterator contains a section
	//and the corresponding data inside the section, first and second respectively.
	for(const auto& it : ini_settings)
	{
		const auto& section = it.first;
		const auto& data = it.second;

		//Make sure the right section is being read, "ignored_extensions"
		if(section == INI_EXTS)
		{
			//Iterate over each key-value pair in the current section,
			//the only information needed in this case is the key or the "extension".
			for(const auto& row : data)
			{
				const std::string key = remove_leading_dot(row.first);
				ignored_extensions.push_back(key);
			}
		}
	}

	//Iterate over all entries in fs_entries, remove any files that have forbidden extensions
	for(const auto& entry : fs_entries)
	{
		//Automatically add all directories since they don't have extensions
		if(!entry.is_directory())
		{
			bool add_file = true;

			//Make sure the given file has a specified extension, and not a blank extension
			if(entry.path().has_extension())
			{
				for(const auto& ext : ignored_extensions)
				{
					//Compare the current file's extension against all forbidden extensions.
					//It is neccessary to use generic_string to remove the quotation marks when
					//comparing to the forbidden extension, and the leading dot needs removal as well,
					//otherwise it would be comparing like this (with quotes): ".png" and png
					if(remove_leading_dot(entry.path().extension().generic_string()) == ext)
					{
						add_file = false;
						break;
					}
				}
			}

			if(add_file)
			{
				filtered_entries.push_back(entry);
			}
		}

		else
		{
			filtered_entries.push_back(entry);
		}
	}

	return filtered_entries;
}

void show_statistics(const std::vector<fs::directory_entry>& fs_entries)
{
	unsigned int directory_count = 0;
	unsigned int file_count = 0;

	for(const auto& entry : fs_entries)
	{
		if(entry.is_directory())
		{
			directory_count += 1;
		}

		else
		{
			file_count += 1;
		}
	}

	std::cout << "[INFO] " << file_count << " files, " << directory_count << " directories ready for mod assembly" << std::endl;
}

void assemble_files_and_directories(const std::vector<fs::directory_entry>& fs_entries, const mINI::INIStructure& ini_settings)
{
	std::cout << "[INFO] Assembling mod to output folder... " << std::endl;

	const std::string output_directory = ini_settings.get(INI_MAIN).get(INI_OUTPUT);
	if(!fs::exists(output_directory))
	{
		fs::create_directory(output_directory);
	}

	const auto copy_options = fs::copy_options::update_existing
							| fs::copy_options::recursive;

	for(const auto& entry : fs_entries)
	{
		fs::path new_path;
		new_path += output_directory;
		new_path += remove_leading_dot(entry.path().generic_string());

		fs::copy(entry.path(), new_path, copy_options);
	}

	std::cout << "[INFO] Mod assembly successful " << std::endl;
}

void generate_default_settings_ini()
{
	//Initialize the new INI File and the struct to hold all the data
	mINI::INIFile new_ini_file(SETTINGS_INI_FILENAME);
	mINI::INIStructure ini_settings;

	//Populate the struct with data
	ini_settings[INI_MAIN][INI_ROOT] = INI_ROOT_DIR;
	ini_settings[INI_MAIN][INI_OUTPUT] = INI_OUTPUT_DIR;

	const std::string default_ignored_extensions[] = {
		".jpg", ".jpeg", ".bmp", ".dds", ".tga", ".xcf", ".py",
		".cpp", ".hpp", ".c", ".h", ".rar", ".zip", ".exe", ".blend",
		".blend1", ".out", ".sh", ".swp", ".txt"
	};

	//Loop through the default extensions to ignore and populate "ignored_extensions",
	//assigning indexes as the keys and the extensions as values like so:
	//[ignored_extensions]
	//0=.jpg
	//1=.png
	//And so on...
	for(int i = 0; i < sizeof(default_ignored_extensions) / sizeof(std::string); i++)
	{
		ini_settings[INI_EXTS][default_ignored_extensions[i]];
	}	

	//Add a default ignored file "settings.ini"
	ini_settings[INI_FILES][std::string(INI_ROOT_DIR) + std::string(SETTINGS_INI_FILENAME)];

	//Add by-default ignored directories
	ini_settings[INI_DIRS][std::string(INI_ROOT_DIR) + "include"];
	ini_settings[INI_DIRS][std::string(INI_ROOT_DIR) + "Blender"];

	//Output to a new settings file
	new_ini_file.generate(ini_settings);
}

mINI::INIStructure load_settings_ini()
{
	if(!file_exists(SETTINGS_INI_FILENAME))
	{
		std::cout << "[WARN] \"" << SETTINGS_INI_FILENAME << "\" could not be found, a new settings file with default values will be generated." << std::endl;
		generate_default_settings_ini();
		std::cout << "[INFO] \"" << SETTINGS_INI_FILENAME << "\" generated with default values." << std::endl;
	}

	mINI::INIFile ini_file(SETTINGS_INI_FILENAME);
	mINI::INIStructure ini_settings;

	ini_file.read(ini_settings);
	std::cout << "[INFO] Loading settings..." << std::endl;

	return ini_settings;
}

bool valid_settings_ini(const mINI::INIStructure& ini_settings)
{
	//Check if the required ini headers are present
	if(
	   ini_settings.has(INI_MAIN) && // "main" 
	   ini_settings.has(INI_EXTS) && // "ignored_extensions"
	   ini_settings.has(INI_DIRS) && // "ignored_folders"
	   ini_settings.has(INI_FILES)   // "ignored_files"
	  )
	{
		//Check if the "main" header has the required fields. All other sections are optional and
		//are therefore not crucial to the operation of this software.
		if(ini_settings.get(INI_MAIN).has(INI_ROOT) && ini_settings.get(INI_MAIN).has(INI_OUTPUT))
		{
			return true;
		}
	}

	return false;
}

void return_to_continue_prompt()
{
	std::string temp_input;
	std::cout << "Press RETURN to continue... ";
	std::getline(std::cin, temp_input);
}

int main()
{
	std::cout << "RE Engine Mod Assembler Tool " << VERSION << ", written by Weeaboo420Fgt a.k.a. SpaceDoggo." << std::endl;
	std::cout << "Special thanks to metayeti for their mINI project, https://github.com/metayeti/mINI." << std::endl;
	std::cout << "mINI used in accordance with the MIT License (MIT), Copyright (C) 2018 Danijel Durakovic." << std::endl << std::endl;

	std::vector<std::string> forbidden_extensions;
	mINI::INIStructure ini_settings = load_settings_ini();

	if(!valid_settings_ini(ini_settings))
	{
		std::cout << "[CRIT] \"" << SETTINGS_INI_FILENAME << "\" could not be loaded properly or is malformed." << std::endl;
		std::cout << "[CRIT] The recommended action is to delete \"" << SETTINGS_INI_FILENAME << "\" and have this tool generate a new one upon next use." << std::endl << std::endl;

		return_to_continue_prompt();
		return 0;
	}

	else
	{
		std::cout << "[INFO] Settings loaded successfully." << std::endl;
	}

	std::vector<fs::directory_entry> fs_entries;

	fs_entries = get_files_and_subdirectories(ini_settings.get(INI_MAIN).get(INI_ROOT));

	//Filter out unwanted directories
	if(ini_settings.get(INI_DIRS).size() > 0)
	{
		fs_entries = filter_directories(fs_entries, ini_settings);
	}

	//Filter out files with unwanted extensions if they are specified
	if(ini_settings.get(INI_EXTS).size() > 0)
	{
		fs_entries = filter_extensions(fs_entries, ini_settings);
	}

	//Filter out specificly unwanted files
	if(ini_settings.get(INI_FILES).size() > 0)
	{
		fs_entries = filter_files(fs_entries, ini_settings);
	}

	show_statistics(fs_entries);
	assemble_files_and_directories(fs_entries, ini_settings);

	std::cout << std::endl;
	return_to_continue_prompt();

	return 0;
}
