import click
import os
import requests

schema = os.environ.get('FILESTORAGE_SCHEMA', 'http')
host = os.environ.get('FILESTORAGE_HOST', '127.0.0.1')
port = os.environ.get('FILESTORAGE_PORT', 8080)
base_url = '{}://{}:{}/files'.format(schema, host, port)

@click.group()
def main():
    """
    Simple CLI for working with file storage
    """
    pass

@main.command()
@click.argument('filepath')
def upload_file(filepath):
    """This upload file"""
    filename = os.path.basename(filepath)
    try:
        files = { 'file': open(filepath,'rb') }
    except FileNotFoundError as ex:
        click.echo(str(ex))
        return

    resp = requests.post('{}/{}'.format(base_url, filename), files=files)
    if resp.status_code == 201:
        info = resp.json()
        click.echo('File with name \"{}\" and size {} has been uploaded successfully.'.format(info['filename'], info['size']))
    elif resp.status_code == 400:
        click.echo('Failed to upload file. Reason: {}'.format(resp.json()['error']))
    else:
        click.echo('Failed to upload \"{}\" file. Please try again...'.format(filename))

@main.command()
@click.argument('filename')
def delete_file(filename):
    """This delete file by file name"""
    resp = requests.delete('{}/{}'.format(base_url, filename))
    if resp.status_code == 200:
        info = resp.json()
        click.echo('File with name \"{}\" and size {} has been deleted successfully.'.format(info['filename'], info['size']))
    elif resp.status_code == 400:
        click.echo('Failed to delete file. Reason: {}'.format(resp.json()['error']))
    else:
        click.echo('Failed to delete \"{}\" file. Please try again...'.format(filename))

@main.command()
def list_files():
    """This return a list of files"""
    resp = requests.get(base_url)
    if resp.status_code == 200:
        for info in resp.json():
            click.echo('{} ({})'.format(info['filename'], info['size']))
    else:
        click.echo('Failed to retrieve list of files. Please try again...')

if __name__ == "__main__":
    main()