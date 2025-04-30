import zipfile
import os


__all__ = ["setup_project"]


def setup_project(zip_structure_path: str, project_root_path: str) -> None:
    if any(os.scandir(project_root_path)):
        raise RuntimeError(f"Folder not empty: {project_root_path}")

    with zipfile.ZipFile(zip_structure_path, 'r') as zip_ref:
        zip_ref.extractall(project_root_path)
