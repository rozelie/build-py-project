from glob import glob

import click
from jinja2 import Template

from . import commands, path_utils


class ProjectBuilder:
    def __init__(self, name: str, path: str, username: str, email: str, type: str, helm: bool):
        self.name = name
        self.paths = path_utils.NewProjectPaths(path, name, type)
        self.username = username
        self.email = email
        self.type = type
        self.helm = helm

    def build(self):
        self.echo_params()
        self.copy_template_files()
        self.rename_dirs()
        self.replace_template_strs()
        self.echo_completion()

    def echo(self, text: str, color: str = None):
        if color:
            click.secho(text, fg=color)
        else:
            click.echo(text)

    def echo_params(self):
        self.echo("Running with params:")
        for name, value in [
            ("Project Name", self.name),
            ("Path", self.paths.parent),
            ("Username", self.username),
            ("Email", self.email),
            ("Type", self.type),
            ("Helm", self.helm),
        ]:
            self.echo(f"\t{name:<14} {value}")

    def copy_template_files(self):
        self.echo("\nCopying template files...")
        commands.mkdir(self.paths.project_root)
        commands.cp(self.paths.type_template, self.paths.project_root, unpack=True)
        commands.cp(self.paths.shared_root, self.paths.project_root, unpack=True)
        if not self.helm:
            self.echo("Removing Helm charts...")
            commands.rm_dir(self.paths.charts)

    def rename_dirs(self):
        self.echo("Renaming dirs...")
        commands.rename_dir(self.paths.src, self.name)
        if self.helm:
            commands.rename_dir(self.paths.charts_src, self.name)

    def replace_template_strs(self):
        self.echo("Replacing template strings...")
        helm_templates = glob(f"{self.paths.charts}/*/templates/*")
        for file in path_utils.get_all_files_in_dir(self.paths.project_root):
            # Helm templates should be handled by Helm, not Jinja
            if file not in helm_templates:
                with open(file) as template_file:
                    template_contents = template_file.read()

                template = Template(template_contents)
                rendered_template = template.render(
                    PROJECT_NAME=self.name, USERNAME=self.username, EMAIL=self.email,
                )
                with open(file, "w") as rendered_template_file:
                    rendered_template_file.write(rendered_template)

    def echo_completion(self):
        color = "green"
        self.echo("\nDone!", color=color)
        self.echo(f"New project created at {self.paths.project_root}", color=color)
