import urllib.request
import zipfile
import subprocess
import os
import webbrowser
import venv


def find_file(startdir, pattern):
    for root, dirs, files in os.walk(startdir):
        for name in files:
            if name.find(pattern) >= 0:
                return root + os.sep + name


SCRIPT_FOLDER = rf"{os.path.dirname(__file__)}"
PROJECT_FOLDER = rf"{SCRIPT_FOLDER}\deloitte-main"


# Baixa o .zip do projeto
if not find_file(SCRIPT_FOLDER, "deloitte.zip"):
    urllib.request.urlretrieve(
        "https://codeload.github.com/mmanfro/deloitte/zip/refs/heads/main",
        f"{SCRIPT_FOLDER}\deloitte.zip",
    )

# Extrai o .zip do projeto (pasta deloitte-main)
if not find_file(SCRIPT_FOLDER, "requirements.txt"):
    with zipfile.ZipFile(f"{SCRIPT_FOLDER}\deloitte.zip", "r") as zip_ref:
        zip_ref.extractall(SCRIPT_FOLDER)


if find_file(PROJECT_FOLDER, "activate") is None:
    # Ambiente virtual não existe, cria um novo
    print("Criando o ambiente virtual")
    env = venv.EnvBuilder(with_pip=True)
    env.create(rf"{PROJECT_FOLDER}\.venv")

VENV_PYTHON = rf"{os.path.dirname(find_file(PROJECT_FOLDER, 'activate'))}\python"
VENV_PIP = rf"{os.path.dirname(find_file(PROJECT_FOLDER, 'activate'))}\pip"


# Instala os módulos com pip
subprocess.check_call(
    [
        VENV_PIP,
        "install",
        "-r",
        rf"{PROJECT_FOLDER}\requirements.txt",
    ]
)

# Inicia o Django
subprocess.check_call(
    [VENV_PYTHON, rf"{PROJECT_FOLDER}\manage.py", "makemigrations", "--no-input"]
)
subprocess.check_call([VENV_PYTHON, rf"{PROJECT_FOLDER}\manage.py", "migrate"])
subprocess.check_call(
    [VENV_PYTHON, rf"{PROJECT_FOLDER}\manage.py", "collectstatic", "--no-input"]
)
os.environ["DJANGO_SUPERUSER_PASSWORD"] = "admin"
subprocess.call(
    [
        VENV_PYTHON,
        rf"{PROJECT_FOLDER}\manage.py",
        "createsuperuser",
        "--no-input",
        "--username=admin",
        "--email=admin@admin.com",
    ]
)
webbrowser.open("http://127.0.0.1:8000/", new=1)
subprocess.check_call([VENV_PYTHON, rf"{PROJECT_FOLDER}\manage.py", "runserver"])
