from pathlib import Path
from zipfile import ZipFile

import typer

app = typer.Typer()


@app.command()
def main():
    with ZipFile("package.zip", "w") as zip_file:
        for filepath in Path("models").glob("**/*"):
            zip_file.write(filepath)
        zip_file.write("Dockerfile")
        zip_file.write("nginx.conf")
        zip_file.write("aws/cron.yaml", "cron.yaml")
        zip_file.write("aws/Dockerrun.aws.json", "Dockerrun.aws.json")


if __name__ == "__main__":

    app()
