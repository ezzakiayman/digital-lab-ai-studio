"""Build the Windows x64 setup EXE with an installed Inno Setup compiler."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.request import urlopen
import zipfile


NODE_ARCHIVE = (
    'https://nodejs.org/download/release/v22.23.3/node-v22.23.3-win-x64.zip',
    '2b0ff57b049cda1bbcea2240eec20467018713c1efe1f7360c2681859b90ed71',
)
PYTHON_ARCHIVE = (
    'https://api.nuget.org/v3-flatcontainer/python/3.12.10/python.3.12.10.nupkg',
    '0eb85c2dfccccf1b17352de4c397f69194035b7d37149eacc16f1147d93de3b8',
)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def fetch(path, url, checksum):
    if path.is_file() and digest(path) == checksum:
        return
    download = path.with_suffix('.download')
    with urlopen(url, timeout=60) as response, download.open('wb') as stream:
        shutil.copyfileobj(response, stream)
    if digest(download) != checksum:
        raise ValueError(f'Checksum mismatch for {url}')
    download.replace(path)


def extract_runtime(source, prefix, target):
    with zipfile.ZipFile(source) as archive:
        for item in archive.infolist():
            parts = PurePosixPath(item.filename).parts
            if item.is_dir() or len(parts) < 2 or parts[0] != prefix:
                continue
            destination = target.joinpath(*parts[1:]).resolve()
            if target not in destination.parents:
                raise ValueError(f'Unexpected runtime archive path: {item.filename}')
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(item) as stream, destination.open('wb') as output:
                shutil.copyfileobj(stream, output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iscc', type=Path, required=True, help='Path to ISCC.exe')
    parser.add_argument('--work-dir', type=Path, required=True, help='Build cache outside the project')
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    work = args.work_dir.resolve()
    output = args.output_dir.resolve()
    scripts = Path(__file__).resolve().parents[1]
    if work == scripts.parent or scripts.parent in work.parents:
        parser.error('--work-dir must be outside the project')
    work.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)

    node = work / 'node.zip'
    python = work / 'python.nupkg'
    fetch(node, *NODE_ARCHIVE)
    fetch(python, *PYTHON_ARCHIVE)

    project = work / 'project'
    archive = work / 'project.zip'
    build = [
        sys.executable, scripts / 'build-transfer.py', '--reusable',
        '--destination', project, '--archive', archive,
    ]
    if project.is_dir():
        build.append('--refresh')
    subprocess.run(build, check=True)

    with TemporaryDirectory(prefix='setup-payload-', dir=work) as temp:
        payload = Path(temp)
        shutil.copyfile(archive, payload / 'project.zip')
        extract_runtime(node, 'node-v22.23.3-win-x64', payload / 'runtime/node')
        extract_runtime(python, 'tools', payload / 'runtime/python')
        subprocess.run([
            args.iscc.resolve(), f'/DPayloadDir={payload}', f'/DOutputDir={output}',
            scripts / 'windows/studio.iss',
        ], check=True)

    installer = output / 'Digital-Lab-Studio-Setup-x64.exe'
    checksum = digest(installer)
    installer.with_suffix('.exe.sha256').write_text(f'{checksum}  {installer.name}\n', encoding='ascii')
    print(f'Installer ready: {installer} ({installer.stat().st_size:,} bytes)')


if __name__ == '__main__':
    main()
