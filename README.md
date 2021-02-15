# W_H_S-Ship-Data-Collector
Python scripts to pull from the wargaming.net API for particular user's data and organize it in a format to dump into a spreadsheet.

# Overview
The Clan Ship Utility is a designed to help manage team compositions by efficiently outputing the ships at any tier of all members of a clan. Currently, members, their ships, and ship names will be outputed in an indent/newline separated format for copy-paste insertion into spreadsheet software (with the intention of using conditional formatting to then display the data visually).

# Use
Two scripts are currently included. The first is used to collect the data from the Wargaming API. It is cached within ships.json to minimize GET requests. To use it, simply run the script using Python 3.* (Confirmed working on 3.7+, but should work for all), follow the prompts to find the clan you'd like to gather the data of, and let it run. The second script is to export the data. Again, run the script and follow the prompts to select the desired ship class and tier to output. It will then dump your data into a .txt file, from which you can copy the data from.

# Features being considered
- Transfer into a webapp to broaded accessability.
- Rich data visualization and 3D interactive graphics to look deeper into the ships a clan owns.
- Interactive system to draft team compositions. (either customizable constraints or hardcoded and maintained constraints for clan events)
- Automatic single step spreadsheet exporting with included formatting. (either give it a spreadsheet and it modifies or it creates it's own spreadsheet)

## Note
Currently this project is solely developed and maintained by George Johnson ([W_H_S]c0ntrol1144). If you use this code elsewhere, please give appropriate credit.