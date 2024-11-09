from django.core.files.storage import FileSystemStorage
import subprocess as sh

# Limits of file properties

FILE_SIZE = 50  # In MB
DURATION = 60   # In seconds


def extract_id(url: str) -> str:
    """Extracts the v parameter (video id) from "/watch?v={video_id}"."""

    if not url.startswith('/watch?v='):
        return ''
    
    id = url.split('v=')[1]

    return id


def validate_size(file) -> bool:
    """Validates if the filesize is at most 50MB."""

    filesize: int = file.size // (1024 * 1024)

    return filesize <= FILE_SIZE


def validate_type(file) -> bool:
    """Checks if the content-type of the file is video.""" 

    file_type = file.content_type.split('/')[0]

    return file_type == 'video'


def validate_duration(file) -> bool:
    """
    Validates if the duration of the file is at most 60 seconds.
    Creates a new process using the subprocess.run method which runs ffprobe 
    """

    # Created temporary file to run duration check on
    # Upload saved to /tmp
    # Duration got through ffprobe via a new process created by subprocess.run

    folder: str = 'tmp/'
    command: list[str] = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1'.split(' ')

    fs = FileSystemStorage(location=folder)

    filename: str = fs.save(file.name, file)
    result = sh.run(command + [ f'{folder}{filename}' ], stdout=sh.PIPE, stderr=sh.STDOUT)

    # Check if there is an error

    if result.stderr is not None:
        fs.delete(filename)

        raise Exception(result.stderr)

    # Testing on nonsense files generated using fsutil gives no error but the stdout is not convertable to an integer.
    # Error is thrown and caught in this case
    # Deletes temporary storage of file regardless of 

    try:
        duration: int = int( float( result.stdout.decode('utf-8') ) )
    except:
        raise Exception(result.stdout.decode('utf-8'))
    finally:
        fs.delete(filename)

    return duration <= DURATION
