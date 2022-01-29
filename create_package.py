from pathlib import Path
from zipfile import ZipFile

import typer

app = typer.Typer()


@app.command()
def main():
    with ZipFile("package.zip", "w") as zip_file:
        for filepath in Path("models").glob("**/*"):
            zip_file.write(filepath)
        for filepath in Path("api").glob("**/*"):
            if "__pycache_" in str(filepath):
                continue
            zip_file.write(filepath)
        zip_file.write("aws/cron.yaml", "cron.yaml")
        zip_file.write("aws/Dockerrun.aws.json", "Dockerrun.aws.json")
        zip_file.write("docker/endpoint.sh")
        zip_file.write("Dockerfile")
        zip_file.write("requirements.txt")


if __name__ == "__main__":

    app()
