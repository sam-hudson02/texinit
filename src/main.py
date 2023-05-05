import click
import os
import shutil
import subprocess
from config import Config
from datetime import date

template_dir = os.path.expanduser('~/.config/texinit/templates')
macros_dir = os.path.expanduser('~/.config/texinit/macros')
templates = os.listdir(template_dir)
templates = [template.split('.')[0] for template in templates]


@click.command()
@click.argument('title', required=False)
@click.option('--template', help='Template to use', required=False,
              type=click.Choice(templates))
@click.option('--git', is_flag=True, help='Initialize Git repository')
@click.option('--author', help='Author of the project', required=False)
def main(template, title, git, author):
    config = Config(title=title, template=template, git=git, author=author)

    click.echo('Template: ' + config.template)
    click.echo('Title: ' + config.title)
    click.echo('Git: ' + str(config.git))
    click.echo('Author: ' + config.author)

    template_path = find_template(config.template)
    if not template_path:
        click.echo('Template not found')
        return
    if not create_project(config):
        return
    if git:
        init_git(title, config)


def find_template(template):
    template_path = os.path.join(template_dir, template)
    template_path = f'{template_path}.tex'
    click.echo(template_path)
    # check if file exists
    if os.path.isfile(template_path):
        return template_path
    return None


def create_project(config: Config) -> bool:
    try:
        os.mkdir(config.title)
    except FileExistsError:
        click.echo('Project already exists')
        return False

    template_path = find_template(config.template)

    os.chdir(config.title)

    copy_files(template_path, config.macros, config.title)
    create_folders(config.folders)
    print('folders', config.folders)
    print('macros', config.macros)

    os.chdir('..')

    fill_template(config.title, config.author)

    return True


def create_folders(folders: list):
    for folder in folders:
        try:
            print(f'Creating folder {folder}')
            os.mkdir(folder)
        except FileExistsError:
            click.echo(f'Folder {folder} already exists')


def copy_files(template_path: str, macros: list, title: str):
    for macro in macros:
        try:
            macro_path = os.path.join(macros_dir, macro)
            shutil.copy(macro_path, f'{macro}')
        except FileNotFoundError:
            click.echo(f'Macro {macro} not found')

    shutil.copy(template_path, f'{title}.tex')


def fill_template(title, author):
    today = date.today().strftime('%d %B %Y')
    month = date.today().strftime('%B')
    year = date.today().strftime('%Y')
    with open(f'{title}/{title}.tex', 'r') as f:
        lines = f.readlines()
    with open(f'{title}/{title}.tex', 'w') as f:
        for line in lines:
            if '!author' in line:
                line = line.replace('!author', author)
            if '!title' in line:
                line = line.replace('!title', title)
            if '!month' in line:
                line = line.replace('!month', month)
            if '!year' in line:
                line = line.replace('!year', year)
            if '!date' in line:
                line = line.replace('!date', today)
            f.write(line)


def init_git(title, config: Config):
    os.chdir(title)
    # initialize git repository, don't output anything
    subprocess.run(['git', 'init', '-q'])
    # make git ignore file
    click.echo('Creating .gitignore')
    shutil.copy(config.default_gitignore_path, '.gitignore')


if __name__ == '__main__':
    main()
