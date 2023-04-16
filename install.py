import os
from src.config import Config
import shutil
import time


def main():
    if os.geteuid() == 0:
        print("Don't run this script as root,"
              "it will ask for sudo password when needed.")
        exit(1)
    current_file = os.path.realpath(__file__)
    current_dir = os.path.dirname(current_file)
    main_path = os.path.join(current_dir, 'src', 'main.py')
    executable_path = os.path.join(current_dir, 'texinit')
    config_dir = os.path.join(os.path.expanduser('~'), '.config', 'texinit')
    bin = '/usr/local/bin'

    # Installs dependencies
    install_dependencies(current_dir)

    # Makes a script that just runs the main.py file
    make_executable(main_path, executable_path)

    # Copies the script to bin
    os.system('sudo cp ' + executable_path + ' ' + bin)

    # Initializes the config file
    make_config(config_dir, current_dir)

    print('texinit installed successfully! Run texinit --help for more info. '
          'Go to ~/.config/texinit to edit the config file.')


def make_executable(main_path, executable_path):
    with open(executable_path, 'w') as f:
        file_content = '#!/bin/bash \n'
        file_content += 'python3 ' + main_path + ' $@ \n'
        f.write(file_content)
    os.chmod(executable_path, 0o755)


def install_dependencies(current_dir):
    print('Installing dependencies...')
    requirements_path = os.path.join(current_dir, 'requirements.txt')
    os.system(f'pip install -r {requirements_path} --user')


def make_config(config_dir, repo_dir):
    print('Initializing config file...')
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        os.chdir(config_dir)
        os.mkdir('templates')
        # copy default template to templates folder
        default_path = os.path.join(repo_dir, 'default.tex')
        shutil.copyfile(default_path, 'templates/default.tex')
    Config()


if __name__ == '__main__':
    main()
