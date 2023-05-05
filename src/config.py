import json
import os


class Config:
    def __init__(self, title: str or None, template: str or None,
                 git: bool or None, author: str or None):

        self._given = {
            'title': title,
            'template': template,
            'git': git,
            'author': author,
            'macros': None,
            'folders': None
        }

        self._config_dir = os.path.join(
            os.path.expanduser('~'), '.config', 'texinit')

        self._config_path = os.path.join(self._config_dir, 'config.json')

        self.validate_files()
        self._config_file = self._load_config()
        self._config = self._process_config()

    def _load_config(self):
        with open(self._config_path, 'r') as f:
            return json.load(f)

    def _generate_default_config(self):
        defaults = {}
        defaults['title'] = 'Project'
        defaults['template'] = 'default'
        defaults['git'] = False
        defaults['author'] = ''
        return {'defaults': defaults}

    def validate_files(self):
        if not os.path.isdir(self._config_dir):
            os.makedirs(self._config_dir)

        if not os.path.isfile(self._config_path):
            config = self._generate_default_config()
            self._save_config(config)

        default_gitignore_path = os.path.join(
            self._config_dir, '.gitignore.default')
        if not os.path.isfile(default_gitignore_path):
            self._generate_default_gitignore()

    def _save_config(self, config):
        with open(self._config_path, 'w') as f:
            json.dump(config, f, indent=4)

    def _generate_default_gitignore(self):
        with open(self._default_gitignore_path, 'w') as f:
            f.write('*.aux \n')
            f.write('*.log \n')
            f.write('*.out \n')
            f.write('*.fdb_latexmk \n')
            f.write('*.fls \n')
            f.write('*.synctex.gz \n')

    def check_template(self, template: str, key: str):
        if template not in self._config_file.keys():
            return None
        return self._config_file[template].get(key, None)

    def get_value(self, key: str, template: str):
        if self._given[key] is not None:
            print(f'Using given {key}: {self._given[key]}')
            return self._given[key]

        if self.check_template(self._given['template'], key) is not None:
            print(f'Using {key} from template: {self._given["template"]}')
            return self.check_template(template, key)

        print(f'Using default {key}: {self._config_file["defaults"][key]}')
        return self._config_file['defaults'][key]

    def get_template(self) -> str:
        if self._given['template'] is not None:
            print(f'Using given template: {self._given["template"]}')
            return self._given['template']
        print(
            f'Using default template: {self._config_file["defaults"]["template"]}')
        return self._config_file['defaults']['template']

    def _process_config(self):
        config = {}
        config['template'] = self.get_template()
        config['title'] = self.get_value('title', config['template'])
        config['git'] = self.get_value('git', config['template'])
        config['author'] = self.get_value('author', config['template'])
        config['macros'] = self.get_value('macros', config['template'])
        config['folders'] = self.get_value('folders', config['template'])
        return config

    @property
    def template(self) -> str:
        return self._config['template']

    @property
    def title(self) -> str:
        return self._config['title']

    @property
    def git(self) -> bool:
        return self._config['git']

    @property
    def author(self) -> str:
        return self._config['author']

    @property
    def macros(self) -> dict:
        return self._config['macros']

    @property
    def folders(self) -> dict:
        return self._config['folders']
