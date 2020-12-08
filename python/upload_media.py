import drive
import cli

def main(filepath):
    d = drive.Drive()
    picture_name = d.uploadPicture(filepath)
    print(f'Uploaded {filepath} to Google Drive as {picture_name}.')

cli.argsFromCLI(main)
