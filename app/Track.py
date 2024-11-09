from pydub import AudioSegment


class Track:
    def __init__(self):
        self.__track = AudioSegment()
        self.__undo_stack = []
        self.__redo_stack = []

    def open(self):
        pass

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

    def mute(self):
        pass

    def unmute(self):
        pass

    def get_volume(self):
        pass

    def set_volume(self):
        pass

    def get_name(self):
        pass

    def remove(self):
        pass

    def reverse(self):
        pass

    def repeat(self):
        pass

    def insert_track(self):
        pass

    def overlay(self):
        pass

    def trim(self):
        pass

    def save(self):
        pass

    def undo(self):
        pass

    def redo(self):
        pass
