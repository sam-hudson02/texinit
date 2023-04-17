import json
import os


class Config:
    def __init__(self):
        self._config_dir = os.path.join(
            os.path.expanduser('~'), '.config', 'texinit')

        if not os.path.isdir(self._config_dir):
            os.makedirs(self._config_dir)

        self._config_path = os.path.join(self._config_dir, 'config.json')

        self._default_gitignore_path = os.path.join(
            self._config_dir, '.gitignore.default')

        self._config = {}
        if not os.path.isfile(self._config_path):
            self._generate_default_config()
        else:
            self._config = self._load_config()

        if not os.path.isfile(self._default_gitignore_path):
            self._generate_default_gitignore()

    def _load_config(self):
        with open(self._config_path, 'r') as f:
            return json.load(f)

    def _generate_default_config(self):
        self._config['default_title'] = 'Project'
        self._config['default_template'] = 'default'
        self._config['default_git'] = False
        self._config['default_author'] = ''
        self._save_config()

    def _save_config(self):
        with open(self._config_path, 'w') as f:
            json.dump(self._config, f, indent=4)

    def _generate_default_gitignore(self):
        with open(self._default_gitignore_path, 'w') as f:
            f.write('*.aux \n')
            f.write('*.log \n')
            f.write('*.out \n')
            f.write('*.fdb_latexmk \n')
            f.write('*.fls \n')
            f.write('*.synctex.gz \n')

    @property
    def default_title(self):
        return self._config.get('default_title', 'Project')

    @property
    def default_template(self):
        return self._config.get('default_template', 'default')

    @property
    def default_git(self):
        return self._config.get('default_git', False)

    @property
    def default_gitignore_path(self):
        return self._default_gitignore_path

    @property
    def default_author(self):
        return self._config.get('default_author', '')
