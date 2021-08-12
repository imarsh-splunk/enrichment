# Splunk Internal Development Playbooks Repository
This repository for Splunk internal automation playbooks for Phantom and Phantom SaaS products thru 4.x. The `develop` repository branch is for staging to ESCU's security-content were you can find objects in preparation to be included in the QA process, cleared and support migration to ESCU for community consumption.

Splunker's are encouraged to create a fork of the repository and send in pull requests for the content they want to share with the community or use the content here for their use or in conjunction with Splunk Sales or Services activities.

The structure of the folders is defined as below:
| Folder | Purpose |
| --- | --- |
| playbooks | Future location for playbooks within ESCU security-content that will go direct to SOAR. Currently, we are have request to modify the default location of playbooks loading to be within the folder vs in the root location of the repository |
| playbooks/custom_functions | Location for any custom_functions for the playbooks above |
| scripts | Misc scripts from preprocessing, REST scripts, etc |
| stories | Alignment for response plans and providing stories to align with workbooks, phases, tasks and playbooks |
| workbooks | Location of the YAML modular workbooks and workbook exports for manual importing |
| workbooks/phases | Location of YAML modular response phase for ingestion into ESCU and that will be sync'd to Phantom and Phantom SaaS with SSE or PAOS App |
| workbooks/phases/tasks | Location of the YAML modular response tasks and mapped playbooks to tasks |


***
Check out our wiki for some how to's and faqs on Phantom playbooks and going pro with your automation playbooks

[Click here](https://github.com/splunk/ps-playbooks/wiki/Home)
***

Thanks for stopping by,
Splunk SOAR Content Team
@philroyer-phantom @socologize
