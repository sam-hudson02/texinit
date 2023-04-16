import click
import os
import shutil
import subprocess
from config import Config

template_dir = '~/.config/texinit/templates'
template_dir = os.path.expanduser(template_dir)


@click.command()
@click.argument('title', required=False)
@click.option('--template', help='Template to use', required=False)
@click.option('--git', is_flag=True, help='Initialize Git repository',
              required=False)
def main(template, title, git):
    config = Config()
    if not title:
        title = config.default_title
    if not template:
        template = config.default_template
    if not git:
        git = config.default_git

    click.echo('Template: ' + template)
    click.echo('Title: ' + title)
    click.echo('Git: ' + str(git))

    template_path = find_template(template)
    if not template_path:
        click.echo('Template not found')
        return
    if not create_project(template_path, title):
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


def create_project(template_path, title) -> bool:
    try:
        os.mkdir(title)
    except FileExistsError:
        click.echo('Project already exists')
        return False

    # Copy template files to project directory
    shutil.copy(template_path, f'{title}/{title}.tex')

    # Create figures directory
    os.chdir(title)
    os.mkdir('figures')

    # Build project
    build(title)
    os.chdir('..')
    return True


def build(title):
    subprocess.run(['latexmk', '-pdf', '-silent', f'{title}.tex'])


def init_git(title, config: Config):
    os.chdir(title)
    # initialize git repository, don't output anything
    subprocess.run(['git', 'init', '-q'])
    # make git ignore file
    click.echo('Creating .gitignore')
    shutil.copy(config.default_gitignore_path, '.gitignore')


if __name__ == '__main__':
    main()
