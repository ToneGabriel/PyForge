import zipfile
import os


class ProjectStructureError(Exception):
    """Exception raised for invalid folder structure at project path"""

    def __init__(self: object, message: str):
        super().__init__(message)


def _check_folder(folder_path: str) -> bool:
    if any(os.scandir(folder_path)):
        raise ProjectStructureError(f"Folder not empty: {folder_path}")


def setup_project(zip_structure_path: str, project_root_path: str) -> None:
    _check_folder(project_root_path)

    with zipfile.ZipFile(zip_structure_path, 'r') as zip_ref:
        zip_ref.extractall(project_root_path)
