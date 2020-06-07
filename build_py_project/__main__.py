import os
import pathlib
import sys
from subprocess import PIPE, Popen
from typing import Tuple

import click

CWD = pathlib.Path(__file__).parent.absolute()


def run_command(command: str) -> Tuple[str, str, int]:
    click.echo(f"\tcmd: {command}")
    handle = Popen(command.split(), stdout=PIPE, stderr=PIPE, close_fds=True)
    stdout, stderr = handle.communicate()
    return (
        stdout.decode("utf8").strip(),
        stderr.decode("utf8").strip(),
        handle.returncode,
    )


class ProjectBuilder:
    def __init__(self, name: str, username: str, email: str, path: str, helm: bool):
        self.name = self.sanitize_input(name)
        self.username = self.sanitize_input(username)
        self.email = self.sanitize_input(email)
        self.path = self.sanitize_input(path, is_path=True)
        self.helm = helm
        self.project_path = f"{self.path}/{self.name}"
        self.template_to_new_str = {
            "PROJECT_NAME": self.name,
            "USERNAME": self.username,
            "EMAIL": self.email,
        }

    def sanitize_input(self, arg: str, is_path: bool = False) -> str:
        if arg.endswith("/") and is_path:
            arg = arg[:-1]

        return arg.strip()

    def set_new_path(self, path: str):
        self.path = path
        self.project_path = f"{path}/{self.name}"

    def reprompt_on_bad_path(self):
        path_exists = os.path.isdir(self.path)
        project_exists = os.path.isdir(self.project_path)
        while not path_exists or project_exists:
            if not path_exists:
                click.echo(f"Path does not exist: {self.path}. Please try again.", err=True)
            elif project_exists:
                click.echo(
                    f"Project already exists at: {self.project_path}. Please try again.", err=True,
                )

            new_path = input("Project Path [e to exit]: ")
            if new_path == "e":
                sys.exit()

            self.set_new_path(self.sanitize_input(new_path, is_path=True))

    def echo_params(self):
        click.echo("Running with params:")
        click.echo(f"\t{'Project Name:':<14} {self.name}")
        click.echo(f"\t{'Username':<14} {self.username}")
        click.echo(f"\t{'Email:':<14} {self.email}")
        click.echo(f"\t{'Path:':<14} {self.path}")
        click.echo(f"\t{'Helm:':<14} {self.helm}")

    def move_template(self):
        click.echo("\nMoving template...")
        run_command(f"mkdir {self.project_path}")
        run_command(f"cp -r {CWD}/project_template/ {self.project_path}")
        if not self.helm:
            click.echo("\nRemoving Helm charts...")
            run_command(f"rm -rf {self.project_path}/{self.name}/charts")

    def update_dir_names(self):
        click.echo("\nUpdating dir names...")
        run_command(f"mv {self.project_path}/PROJECT_NAME {self.project_path}/{self.name}")
        if self.helm:
            run_command(
                f"mv {self.project_path}/charts/PROJECT_NAME {self.project_path}/charts/{self.name}"
            )

    def replace_template_strs(self):
        click.echo("\nReplacing template strings...")
        new_project_files, *_ = run_command(f"find {self.project_path} -type f")
        for file in new_project_files.split("\n"):
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
                click.echo(f"\t{file}")
                for replacement in replacements_made:
                    click.echo(f"\t\t{replacement[0]} -> {replacement[1]}")

                with open(file, "w") as f:
                    f.write("".join(new_data))

                click.echo("")

    def echo_completion(self):
        click.echo("\nDone!")
        click.echo(f"New project created at {self.project_path}")


@click.command()
@click.option("--name", type=str, prompt="Project Name", help="The project name.")
@click.option("--username", type=str, prompt="Your Name", help="Your name.")
@click.option("--email", type=str, prompt="Your Email", help="Your email.")
@click.option("--path", type=str, prompt="Project Path", help="Path to new project.")
@click.option("--helm", is_flag=True, prompt="Include Helm charts", help="Include helm charts.")
def cli(name: str, username: str, email: str, path: str, helm: bool):
    builder = ProjectBuilder(name, username, email, path, helm)
    builder.reprompt_on_bad_path()

    builder.echo_params()

    builder.move_template()
    builder.update_dir_names()
    builder.replace_template_strs()

    builder.echo_completion()


if __name__ == "__main__":
    cli()
