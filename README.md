# texinit

An easy to use cli project initializer for your latex projects.

### Dependencies

- currently only linux is supported
- you'll need to install latexmk as this is used to build the latex document

### Installation

- clone this repo: ```git clone https://github.com/sam-hudson02/texinit.git && cd texinit```
- run install script: ```python3 install.py```


### Config

- templates live at ```~/.config/texinit/templates```
- default template, author and git init can be edited in ```~/.config/texinit/config.json```

### Usage

To create a new project use ```texinit [options] [project title]``` ie ```texinit --git --template mytemplate project1```

## Templates

You the following key words in your templates and they will be replaced with the following values

!title - replaced with project title - eg: ```\title{!title}``` \
!author - replaced with project author - eg: ```\author{!author}``` \
!date - replaced with current date in form (18 April 2023) - eg: ```\date{!date}``` \
!month - replaced with current month in form (April) - eg: ```\date{!month}``` \
!year - replaced with current year in from (2023) - eg: ```\date{!year}``` 
