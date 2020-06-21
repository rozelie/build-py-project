from glob import glob

from jinja2 import Template

from . import commands, path_utils
from .printer import print_green, print_info


class ProjectBuilder:
    def __init__(self, name: str, path: str, username: str, email: str, type: str, helm: bool):
        self.name = name
        self.paths = path_utils.NewProjectPaths(path, name, type)
        self.username = username
        self.email = email
        self.type = type
        self.helm = helm

    def build(self):
        self.print_params()
        self.copy_template_files()
        self.rename_dirs()
        self.replace_template_strs()
        self.print_completion()

    def print_params(self):
        print_green("Running with params:")
        for name, value in [
            ("Project Name", self.name),
            ("Path", self.paths.parent),
            ("Username", self.username),
            ("Email", self.email),
            ("Type", self.type),
            ("Helm", self.helm),
        ]:
            print_info(f"\t{name:<14} {value}")

    def copy_template_files(self):
        print_info("\nCopying template files...")
        commands.mkdir(self.paths.project_root)
        commands.cp(self.paths.type_template, self.paths.project_root, unpack=True)
        commands.cp(self.paths.shared_root, self.paths.project_root, unpack=True)
        if not self.helm:
            print("Removing Helm charts...")
            commands.rm_dir(self.paths.charts)

    def rename_dirs(self):
        print_info("Renaming dirs...")
        commands.rename_dir(self.paths.src, self.name)
        if self.helm:
            commands.rename_dir(self.paths.charts_src, self.name)

    def replace_template_strs(self):
        print_info("Replacing template strings...")
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

    def print_completion(self):
        print_green("\nDone!")
        print_green(f"New project created at {self.paths.project_root}")
