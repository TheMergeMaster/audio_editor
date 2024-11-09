import pygame
from tkinter import *
from window import Window


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MusicPlayer")
        self.root.geometry("600x900+200+80")

        pygame.init()
        pygame.mixer.init()

        self.track = StringVar()
        self.status = StringVar()
        self.playpauseicons = StringVar()
        self.play, self.pause = ["\u25B6", "\u23F8"]
        self.volume = StringVar()
        self.muteunmuteicons = StringVar()
        self.unmutedicon, self.mutedicon = ["\U0001F50A", "\U0001F507"]
        self.mute = False

        self.tr = None
        trackframe = LabelFrame(
            self.root,
            text="Song Track",
            font=("times new roman", 15, "bold"),
            bg="Navyblue",
            fg="white",
            bd=5,
            relief=GROOVE,
        )
        trackframe.place(x=0, y=0, width=600, height=100)
        songtrack = Label(
            trackframe,
            textvariable=self.track,
            # width=20,
            font=("times new roman", 20, "bold"),
            bg="Orange",
            fg="white",
        ).grid(row=0, column=0, padx=10, pady=5)
        trackstatus = Label(
            trackframe,
            textvariable=self.status,
            font=("times new roman", 20, "bold"),
            bg="orange",
            fg="white",
        ).grid(row=0, column=1, padx=10, pady=5)

        buttonframe = LabelFrame(
            self.root,
            text="Control Panel",
            font=("times new roman", 15, "bold"),
            bg="grey",
            fg="white",
            bd=5,
            relief=GROOVE,
        )
        buttonframe.place(x=0, y=100, width=600, height=100)
        playbtn = Button(
            buttonframe,
            textvariable=self.playpauseicons,
            command=self.playpause,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="navyblue",
            bg="pink",
        )
        self.playpauseicons.set(self.play)
        playbtn.grid(row=0, column=0, padx=10, pady=5)

        stopbtn = Button(
            buttonframe,
            text="\u23F9",
            command=self.stopsong,
            width=10,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="navyblue",
            bg="pink",
        ).grid(row=0, column=3, padx=10, pady=5)
        openbtn = Button(
            buttonframe,
            text="Open",
            command=self.open_helper,
            width=8,
            height=1,
            font=("times new roman", 16, "bold"),
            fg="navyblue",
            bg="pink",
        ).grid(row=0, column=8, padx=10, pady=5)
        volumelbl = Button(
            buttonframe,
            textvariable=self.muteunmuteicons,
            command=self.muteunmute,
            font=("times new roman", 16, "bold"),
            fg="navyblue",
            bg="pink",
        ).grid(row=0, column=6, padx=10, pady=5)
        self.muteunmuteicons.set(self.unmutedicon)

        volumesldr = Scale(
            buttonframe,
            from_=0,
            to=100,
            variable=self.volume,
            command=lambda new_vol: self.changevolume(new_vol),
            orient=HORIZONTAL,
            width=10,
            font=("times new roman", 12, "bold"),
            fg="navyblue",
            bg="pink",
        )
        volumesldr.set(14)
        volumesldr.grid(row=0, column=7, padx=0, pady=5)

    def set_playing_status(self, status):
        self.status.set(status)

    def playpause(self):
        if pygame.mixer.music.get_pos() == -1:
            self.playsong()
        elif pygame.mixer.music.get_busy():
            self.pausesong()
        else:
            self.unpausesong()

    def playsong(self):
        if self.tr is not None:
            # self.active_audio_path = self.tr.get_file_path()
            self.tr = Window.get_audio(Window)
            print(self.tr.track.duration_seconds)
            # self.tr.track.export(
            #     f"temp_{self.active_audio_name}", bitrate="320k", format="mp3"
            # )
            pygame.mixer.music.load(f"temp_{self.active_audio_name}")
            # self.active_audio_name = self.reduce_name(self.tr.get_file_name())
            # self.track.set(self.active_audio_name)
            self.playpauseicons.set(self.pause)
            self.set_playing_status("-Playing")
            if self.tr.track.duration_seconds:
                pygame.mixer.music.play()
            else:
                messagebox.showerror(
                    "Audio too short", "Audio length is 0. Can't play that"
                )

    def stopsong(self):
        self.playpauseicons.set(self.play)
        self.set_playing_status("-Stopped")
        pygame.mixer.music.stop()

    def pausesong(self):
        self.playpauseicons.set(self.play)
        self.set_playing_status("-Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        self.playpauseicons.set(self.pause)
        self.set_playing_status("-Playing")
        pygame.mixer.music.unpause()

    def changevolume(self, new_volume):
        pygame.mixer.music.set_volume(int(new_volume) / 100)
        self.volume.set(int(new_volume))

    def muteunmute(self):
        if self.mute:
            self.changevolume(self.current_volume)
            self.muteunmuteicons.set(self.unmutedicon)
            self.mute = False
        else:
            self.current_volume = self.volume.get()
            self.changevolume(0)
            self.muteunmuteicons.set(self.mutedicon)
            self.mute = True

    def reduce_name(self, audio_name):
        if len(audio_name) - 4 > 25:
            audio_name = audio_name[:23] + "..."
        return audio_name

    def open_helper(self):
        Window.open(Window)
        self.tr = Window.get_audio(Window)
        if self.tr.get_file_name() != "":
            self.stopsong()
            self.active_audio_name = self.tr.get_file_name()
            self.track.set(self.reduce_name(self.active_audio_name))
            # self.tr.track.export(
            #     f"temp_{self.active_audio_name}", bitrate="320k", format="mp3"
            # )
            # pygame.mixer.music.load(f"temp_{self.active_audio_name}")
            # pygame.mixer.music.play()

    def testing(self):
        print("testing testing")


if __name__ == "__main__":
    root = Tk()
    root.resizable(0, 0)
    MusicPlayer(root)
    root.mainloop()