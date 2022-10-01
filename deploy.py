import os
import subprocess
import urllib.request
import venv
import webbrowser
import zipfile


def find_file(startdir, pattern):
    for root, dirs, files in os.walk(startdir):
        for name in files:
            if name.find(pattern) >= 0:
                return root + os.sep + name


SCRIPT_FOLDER = rf"{os.path.dirname(__file__)}"
PROJECT_FOLDER = rf"{SCRIPT_FOLDER}{os.path.sep}deloitte-main"


if not find_file(SCRIPT_FOLDER, "deloitte.zip"):
    # Baixa o .zip do projeto
    urllib.request.urlretrieve(
        r"https://codeload.github.com/mmanfro/deloitte/zip/refs/heads/main",
        f"{SCRIPT_FOLDER}{os.path.sep}deloitte.zip",
    )

if not find_file(SCRIPT_FOLDER, "requirements.txt"):
    # Extrai o .zip do projeto (pasta deloitte-main)
    with zipfile.ZipFile(f"{SCRIPT_FOLDER}{os.path.sep}deloitte.zip", "r") as zip_ref:
        zip_ref.extractall(SCRIPT_FOLDER)


if find_file(PROJECT_FOLDER, "activate") is None:
    # Ambiente virtual não existe, cria um novo
    print("Criando o ambiente virtual")
    env = venv.EnvBuilder(with_pip=True)
    env.create(rf"{PROJECT_FOLDER}{os.path.sep}.venv")


###############################################################
# Todos os comandos abaixo são executados no ambiente virtual #
###############################################################

VENV_PYTHON = (
    f"{os.path.dirname(find_file(PROJECT_FOLDER, 'activate'))}{os.path.sep}python"
)
VENV_PIP = f"{os.path.dirname(find_file(PROJECT_FOLDER, 'activate'))}{os.path.sep}pip"


# Instala os módulos com pip
subprocess.check_call(
    [
        VENV_PIP,
        "install",
        "-r",
        f"{PROJECT_FOLDER}{os.path.sep}requirements.txt",
    ]
)

# Inicia o Django
subprocess.check_call(
    [
        VENV_PYTHON,
        f"{PROJECT_FOLDER}{os.path.sep}manage.py",
        "makemigrations",
        "--no-input",
    ]
)
subprocess.check_call(
    [VENV_PYTHON, f"{PROJECT_FOLDER}{os.path.sep}manage.py", "migrate"]
)
subprocess.check_call(
    [
        VENV_PYTHON,
        f"{PROJECT_FOLDER}{os.path.sep}manage.py",
        "collectstatic",
        "--no-input",
    ]
)
os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"
subprocess.call(
    [
        VENV_PYTHON,
        f"{PROJECT_FOLDER}{os.path.sep}manage.py",
        "createsuperuser",
        "--no-input",
        "--username=admin",
        "--email=admin@admin.com",
    ]
)
subprocess.check_call([VENV_PYTHON, f"{PROJECT_FOLDER}{os.path.sep}manage.py", "test"])
webbrowser.open("http://127.0.0.1:8000/", new=1)
subprocess.check_call(
    [VENV_PYTHON, f"{PROJECT_FOLDER}{os.path.sep}manage.py", "runserver"]
)
