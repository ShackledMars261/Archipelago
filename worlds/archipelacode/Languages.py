from .Types import Language


def get_all_supported_languages() -> list[Language]:
    return [
        Language("Python3", ["python3"]),
        Language("Javascript", ["javascript"]),
        Language("Typescript", ["typescript"]),
        Language("Golang", ["golang"]),
    ]
