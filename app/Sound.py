from pydub import AudioSegment
import tkinter.filedialog as tkFileDialog
from helpers.download_and_extract import download_and_extract
from constants import FFMPEG_REMOTE_PATH, FFMPEG_LOCAL_PATH
# from pygame import mixer

# Required for editing audio
# AudioSegment.converter = "D:\\ffmpeg-4.3.1-win64-static\\bin\\ffmpeg.exe"
# AudioSegment.ffmpeg = "D:\\ffmpeg-4.3.1-win64-static\\bin\\ffmpeg.exe"
# AudioSegment.ffprobe = "D:\\ffmpeg-4.3.1-win64-static\\bin\\ffprobe.exe"

# download_and_extract(
#     FFMPEG_REMOTE_PATH, FFMPEG_LOCAL_PATH, "ffmpeg.7z", FFMPEG_LOCAL_PATH)


class Sound:
    def __init__(self):
        ''' Open a file using Tkinter's built in filedialog. The dialog allows a .mp3 file to be opened. '''

        self.filePath = tkFileDialog.askopenfilename(
            initialdir="/home/",
            title="Which audio track do you want to import?",
            filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")),
        )

        # Using pydub, we create a AudioSegment object from the user-chosen .mp3 file. This object is stored in track.
        if self.filePath:
            print("\n before .from_mp3")
            print("\n filepath:", self.filePath)
            self.track = AudioSegment.from_mp3(self.filePath)
            print("\n after .from_mp3")
        else:
            self.track = None

        self.queue = []
        self.stack = []

    def get_file_path(self):
        return self.filePath

    def get_file_name(self):
        return self.get_file_path()[self.get_file_path().rfind("/") + 1:]

    def temp_save(self):
        extra = ""
        # mixer.music.unload()
        self.track.export(
            f"./temp/{extra}temp_{self.get_file_name()}", bitrate="320k", format="mp3"
        )
        return self.track

    def save(self):
        ''' Using Tkinter to choose a location to save variable track and then exporting
        track to that location using AudioSegment as 320kbps mp3 file. '''
        save_path = tkFileDialog.asksaveasfilename(
            initialdir="/home/",
            title="Where do you want to save the modified audio track?",
            filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")),
        )
        # pyDubs export function allows us to output track to the file path specified by the user.
        if save_path:
            save_path2 = str(save_path)[: save_path.rfind("/") + 1]
            save_name = str(save_path).split("/")[-1].split(".")
            if len(save_name) > 1:
                save_name.pop()
            save_name = "".join(save_name)
            self.track.export(
                str(save_path2) + str(save_name) + ".mp3", bitrate="320k", format="mp3"
            )
            return save_name + ".mp3"

        return False

    def reverse(self):
        """
        reverse allows us to reverse track using pydub. We append the current contents 
        of track to the end of the stack array, this will us to revert back.
        """
        self.stack.append(self.track)
        self.track = self.track.reverse()
        self.temp_save()

    def checkLength(self):
        """
        checkLength is a getter function which returns the current length of track. 
        This is used by the window class to display the length
        in seconds of track. 
        """
        if self.track:
            return self.track.duration_seconds
        return "0"

    def trim(self, start_time, end_time):
        ''' Cut audio from a start point to an end point '''
        if not end_time:
            end_time = self.checkLength()
        if not start_time:
            start_time = 0
        self.stack.append(self.track)
        self.track = self.track[
            int(float(start_time) * 1000): int(float(end_time) * 1000) + 1
        ]
        self.temp_save()

    def gapMerge(self, from_, for_, gap=0):
        """
        Merge allows the user to merge two tracks together with or without gap and
        merges the second audio for a user-specified value
        """
        self.stack.append(self.track)
        self.filePath2 = tkFileDialog.askopenfilename(
            initialdir="/home/",
            title="What file do you want to import?",
            filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")),
        )
        if not self.filePath2:
            return False
        self.mergeTrack = AudioSegment.from_mp3(self.filePath2)
        if for_ == "":
            for_ = self.mergeTrack.duration_seconds

        self.track = (
            self.track[: int(float(from_) * 1000)]
            + AudioSegment.silent(duration=int(float(gap) * 1000))
            + self.mergeTrack[: int(float(for_) * 1000)]
            + self.track[int(float(from_) * 1000):]
        )
        self.temp_save()
        return self.filePath2[self.filePath2.rfind("/") + 1:]

    def repeat(self):
        self.stack.append(self.track)
        self.track = self.track + self.track
        self.temp_save()

    def overlay(self):
        ''' Overlay loads in a new AudioSegment and overlays it with track. Useful for stereo audio.'''
        self.stack.append(self.track)
        self.filePath2 = tkFileDialog.askopenfilename(
            initialdir="/home/",
            title="What file do you want to import?",
            filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")),
        )
        if not self.filePath2:
            return False
        self.overlayTrack = AudioSegment.from_mp3(self.filePath2)
        self.track = self.track.overlay(self.overlayTrack)
        self.temp_save()
        return self.filePath2[self.filePath2.rfind("/") + 1:]

    def clearTrack(self):
        ''' Clear tracks and reset stack and queue '''
        self.track = None
        self.stack = []
        self.queue = []
        return None

    def undo(self):
        if self:
            if self.stack:
                self.queue.insert(0, self.track)
                self.track = self.stack.pop()
                self.temp_save()
                return True
        return False

    def redo(self):
        if self:
            if self.queue:
                self.stack.append(self.track)
                self.track = self.queue.pop(0)
                self.temp_save()
                return True
        return False
