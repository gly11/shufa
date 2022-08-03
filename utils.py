import os


def get_project_path():
    """得到项目路径"""
    # project_path = os.path.join(
    #     os.path.dirname(__file__),
    #     "..",
    # )
    project_path = os.path.dirname(__file__)
    return project_path
