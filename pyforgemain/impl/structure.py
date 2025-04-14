import zipfile
import os


def _check_folder(folder_path: str) -> bool:
    if any(os.scandir(folder_path)):
        raise RuntimeError(f"Folder not empty: {folder_path}")


def setup_project(zip_structure_path: str, project_root_path: str) -> None:
    _check_folder(project_root_path)

    with zipfile.ZipFile(zip_structure_path, 'r') as zip_ref:
        zip_ref.extractall(project_root_path)
