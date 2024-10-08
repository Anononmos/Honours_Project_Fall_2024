from django.core.files.storage import FileSystemStorage
import subprocess as sh

def validate_size(file) -> bool:
    LIMIT = 50  # Max filesize of 50MB
    filesize: int = file.size // (1024 * 1024)

    return filesize < LIMIT

def validate_type(file) -> bool:
    file_type = file.content_type.split('/')[0]

    return file_type == 'video'


def validate_duration(file) -> bool:
    # Created temporary file to run duration check on
    # Duration got through ffprobe
    
    folder: str = '../tmp/'        
    fs = FileSystemStorage(location=folder)

    filename: str = fs.save(file.name, file)
    url: str = fs.url(filename)

    command: str = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {filename}'

    result = sh.run(command.split(' '), stdout=sh.PIPE, stderr=sh.STDOUT)
    duration: int = int(result.stdout)
