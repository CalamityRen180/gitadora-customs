import platform
import os
import shutil

def is_wsl():
    return "microsoft" in platform.uname()[3].lower()


def get_windows_path(input):
    return '\\'.join(os.path.normpath(input).split(os.sep))


def getCaseInsensitivePath(path):
    """
    Source: http://code.activestate.com/recipes/576571-case-insensitive-filename-on-nix-systems-return-th/
    Get a case insensitive path on a case sensitive system
    """

    if path == "" or os.path.exists(path):
        return path

    f = os.path.basename(path) # f may be a directory or a file
    d = os.path.dirname(path)

    suffix = ""
    if not f: # dir ends with a slash?
        if len(d) < len(path):
            suffix = path[:len(path)-len(d)]

        f = os.path.basename(d)
        d = os.path.dirname(d)

    if not os.path.exists(d):
        d, found = getCaseInsensitivePath(d, True)

        if not found:
            return path

    # at this point, the directory exists but not the file

    try: # we are expecting 'd' to be a directory, but it could be a file
        files = os.listdir(d)
    except:
        return path

    f_low = f.lower()

    try:
        f_nocase = [fl for fl in files if fl.lower() == f_low][0]
    except:
        f_nocase = None

    if f_nocase:
        return os.path.join(d, f_nocase) + suffix

    else:
        return path # cant find the right one, just return the path as is.

def romanize(text):
    if all(ord(c) < 128 for c in text):
        return text

    import pykakasi
    kakasi = pykakasi.kakasi()
    kakasi.setMode("H","a")
    kakasi.setMode("K","a")
    kakasi.setMode("J","a")
    kakasi.setMode("C", True)
    conv = kakasi.getConverter()
    new_text = conv.do(text)
    return new_text.upper() if text != new_text else text

def _find_tool(candidates):
    for candidate in candidates:
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

        resolved = shutil.which(candidate)
        if resolved:
            return resolved

    return None

def check_ffmpeg():
    ffmpeg_path = _find_tool(["ffmpeg.exe", "ffmpeg"])
    if not ffmpeg_path:
        raise RuntimeError("Couldn't find ffmpeg. Install ffmpeg or add it to PATH.")

    ffprobe_path = _find_tool(["ffprobe.exe", "ffprobe"])
    if not ffprobe_path:
        raise RuntimeError("Couldn't find ffprobe. Install ffmpeg or add it to PATH.")

    import pydub

    pydub.AudioSegment.converter = ffmpeg_path
    pydub.AudioSegment.ffmpeg = ffmpeg_path
    pydub.AudioSegment.ffprobe = ffprobe_path

    return ffmpeg_path
