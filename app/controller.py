from Track import Track


def open_track(path: str) -> bool:
    try:
        Track.open(path)
        return True
    except:
        return False


def play_track() -> None:
    Track.play()


def pause_track() -> None:
    Track.pause()


def stop_track() -> None:
    Track.stop()


def mute_track() -> None:
    Track.mute()


def unmute_track() -> None:
    Track.unmute()


def get_volume() -> int:
    return Track.get_volume()


def set_volume(volume: int) -> int:
    Track.set_volume(volume)
    return volume


def reverse_track() -> None:
    Track.reverse()


def get_track_name() -> str:
    return Track.get_name()


def save_track() -> bool:
    try:
        Track.save()
        return True
    except:
        return False


def remove_track() -> None:
    Track.remove()


def repeat_track(n: int) -> None:
    Track.repeat(n)


def overlay_track():
    Track.overlay()


def trim_track(from: Timestamp, to: Timestamp) -> None:
    Track.trim(from , to)


def insert_track(at: Timestamp, from: Timestamp, to: Timestamp) -> Boolean:
    try:
        Track.insert(at, from , to)
        return True
    except:
        return False


def undo():
    pass


def redo():
    pass
