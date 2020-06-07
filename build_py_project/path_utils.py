import os
import pathlib
from typing import Iterator, List, Set, Tuple


def get_parent(file: str) -> pathlib.Path:
    return pathlib.Path(file).parent.absolute()


def walk(path: str) -> Iterator[Tuple[str, List[str], List[str]]]:
    return os.walk(path)


def get_all_files_in_dir(dir_path: str) -> List[str]:
    files = []
    for path, dirnames, filenames in walk(dir_path):
        for file in filenames:
            files.append(f"{path}/{file}")

    return files


def get_project_types() -> Set[str]:
    top_level_template_dirs = list(walk(f"{get_parent(__file__)}/templates"))[0][1]
    return {x for x in top_level_template_dirs if x not in {"project_root_shared"}}


def dir_exists(path_to_dir: str):
    return os.path.isdir(path_to_dir)


class NewProjectPaths:
    def __init__(self, parent: str, name: str, type: str):
        self.cwd = get_parent(__file__)
        self.parent = parent
        self.project_root = f"{self.parent}/{name}"
        self.src = f"{self.project_root}/PROJECT_NAME"
        self.charts = f"{self.project_root}/charts"
        self.charts_src = f"{self.project_root}/charts/PROJECT_NAME"

        self.templates = f"{self.cwd}/templates"
        self.type_template = f"{self.templates}/{type}"
        self.shared_root = f"{self.templates}/project_shared_root "
