import click

from . import commands, path_utils


class ProjectBuilder:
    def __init__(self, name: str, path: str, username: str, email: str, type: str, helm: bool):
        self.name = name
        self.paths = path_utils.NewProjectPaths(path, name, type)
        self.username = username
        self.email = email
        self.type = type
        self.helm = helm
        self.template_to_new_str = {
            "PROJECT_NAME": self.name,
            "USERNAME": self.username,
            "EMAIL": self.email,
        }

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
            self.echo("\nRemoving Helm charts...")
            commands.rm_dir(self.paths.charts)

    def rename_dirs(self):
        self.echo("\nRenaming dirs...")
        commands.rename_dir(self.paths.src, self.name)
        if self.helm:
            commands.rename_dir(self.paths.charts_src, self.name)

    def replace_template_strs(self):
        self.echo("\nReplacing template strings...")
        for file in path_utils.get_all_files_in_dir(self.paths.project_root):
            with open(file) as f:
                file_data = f.readlines()

            replacements_made = []
            new_data = []
            for line in file_data:
                for template_str in self.template_to_new_str.keys():
                    if template_str in line:
                        new_str = self.template_to_new_str[template_str]
                        templated_line = line.replace(template_str, new_str)
                        replacements_made.append((line.strip(), templated_line.strip()))
                        line = templated_line

                new_data.append(line)

            if replacements_made:
                self.echo(f"\t{file}")
                for replacement in replacements_made:
                    self.echo(f"\t\t{replacement[0]} -> {replacement[1]}")

                with open(file, "w") as f:
                    f.write("".join(new_data))

                self.echo("")

    def echo_completion(self):
        color = "green"
        self.echo("\nDone!", color=color)
        self.echo(f"New project created at {self.paths.project_root}", color=color)
