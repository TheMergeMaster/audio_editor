import tkinter as tk
from Sound import Sound
from Components import Window, Section, Button, Slider, Label, Input
from helpers.create_tmp_dir import create_tmp_dir

from constants import \
    COLORS, \
    FONT_FAMILY, \
    ICONS, \
    PLAY_ICON, \
    PAUSE_ICON, \
    STOP_ICON, \
    TEMP_DIR_PATH, \
    VOLUME_MUTED_ICON, \
    VOLUME_FULL_ICON


class AudioEditor:
    __PLAY_ICON = ICONS[PLAY_ICON]
    __PAUSE_ICON = ICONS[PAUSE_ICON]
    __STOP_ICON = ICONS[STOP_ICON]
    __VOLUME_FULL_ICON = ICONS[VOLUME_FULL_ICON]
    __MUTED_ICON = ICONS[VOLUME_MUTED_ICON]
    __FONT_FAMILY = FONT_FAMILY
    __MUTE_UNMUTE_ICONS = tk.StringVar()
    __PLAY_PAUSE_ICONS = tk.StringVar()
    __track = tk.StringVar()
    __status = tk.StringVar()
    __task_status = tk.StringVar()
    __current_pos = tk.StringVar()
    __current_pos.set("?s/?s")
    __tr = None

    def __init__(self):
        create_tmp_dir(TEMP_DIR_PATH)

        self.root = Window("Audio Editor", "600x705+500+75")

        '''******************** Song Track Frame ********************'''
        trackframe = Section(self.root, "Song Track")
        trackframe.place(x=0, y=0, width=600, height=100)

        songtrack = Label(trackframe, textvariable=__track)
        songtrack.grid(row=0, column=0, padx=10, pady=5)

        current_pos_lbl = Label(trackframe, textvariable=self.current_pos)
        current_pos_lbl.grid(row=0, column=10, padx=5, pady=5)

        '''******************** Control Panel Frame ********************'''
        buttonframe = Section(self.root, "Control Panel")
        buttonframe.place(x=0, y=100, width=600, height=100)

        playbtn = Button(buttonframe, self.playpause,
                         textvariable=self.playpauseicons)
        playbtn.grid(row=0, column=0, padx=10, pady=5)
        self.playpauseicons.set(self.play_icon)

        stopbtn = Button(buttonframe, self.stopsong, text=self.stop_icon)
        stopbtn.grid(row=0, column=3, padx=10, pady=5)

        openbtn = Button(buttonframe, self.open_helper, text="Open")
        openbtn.grid(row=0, column=8, padx=10, pady=5)
        volumelbl = Button(buttonframe, self.muteunmute,
                           textvariable=self.muteunmuteicons)
        volumelbl.grid(row=0, column=6, padx=10, pady=5)
        self.muteunmuteicons.set(self.volume_full_icon)

        volumesldr = Slider(
            buttonframe,
            from_=0,
            to=100,
            variable=self.volume,
            command=lambda new_vol: self.changevolume(new_vol.split(".")[0]),
            orient=tk.HORIZONTAL,
        )
        volumesldr.set(14)
        volumesldr.grid(row=0, column=7, padx=0, pady=5)

        '''******************** Task Status Frame ********************'''
        self.task_status_frm = tk.Frame(
            self.root,
            bg="black",
            bd=2,
            relief=tk.GROOVE,
        )

        self.task_status_frm.place(x=0, y=200, width=600, height=100)

        self.task_status_lbl = Label(
            self.task_status_frm, textvariable=self.task_status)
        self.task_status_lbl.pack(expand=True)

        '''******************** Editor Panel Frame ********************'''
        self.edtr_panel_frm = Section(self.root, "Editor Panel")
        self.edtr_panel_frm.place(x=0, y=300, width=600, height=700)

        self.action_bar_frm = Section(self.edtr_panel_frm, "Action bar")
        self.action_bar_frm.place(
            x=8,
            y=5,
            width=580,
            height=80,
        )

        self.saveButton = Button(
            self.action_bar_frm, self.save_helper, text="Save")
        self.saveButton.grid(row=0, column=0, padx=10, pady=5)

        self.clearButton = Button(
            self.action_bar_frm, self.clear_helper, text="Clear")
        self.clearButton.grid(row=0, column=1, padx=10, pady=5)

        self.undoButton = Button(
            self.action_bar_frm, self.undo_helper, text="Undo")
        self.undoButton.grid(row=0, column=2, padx=10, pady=5)

        self.redoButton = Button(
            self.action_bar_frm, self.redo_helper, text="Redo")
        self.redoButton.grid(row=0, column=3, padx=10, pady=5)

        '''******************** Fun Tools Frame ********************'''
        self.rev_rep_frm = Section(self.edtr_panel_frm, "Fun Tools")
        self.rev_rep_frm.place(x=8, y=85, width=580, height=85)

        self.rev_audio_btn = Button(
            self.rev_rep_frm, self.rev_helper, text="Reverse")
        self.rev_audio_btn.grid(row=0, column=0, padx=10, pady=10)

        self.repeat_btn = Button(
            self.rev_rep_frm, self.repeat_helper, text="Repeat")
        self.repeat_btn.grid(row=0, column=1, padx=10, pady=10)

        self.overlay_btn = Button(
            self.rev_rep_frm, self.overlay_helper, text="Overlay")
        self.overlay_btn.grid(row=0, column=2, padx=10, pady=10)

        '''******************** Cut Audio Frame ********************'''
        self.cut_audio_frm = Section(self.edtr_panel_frm, "Cut")
        self.cut_audio_frm.place(x=8, y=170, width=290, height=200)

        self.trim_start_lbl = Label(self.cut_audio_frm, text="Cut from (sec)")
        self.trim_start_lbl.grid(row=0, column=0, padx=10, pady=10)

        self.trim_start_input = Input(self.cut_audio_frm)
        self.trim_start_input.grid(row=0, column=1, padx=10, pady=10)

        self.trim_end_lbl = Label(self.cut_audio_frm, text="Cut till (sec)")
        self.trim_end_lbl.grid(row=1, column=0, padx=10, pady=10)

        self.trim_end_input = Input(self.cut_audio_frm)
        self.trim_end_input.grid(row=1, column=1, padx=10, pady=10)

        self.cut_audio_btn = Button(
            self.cut_audio_frm, self.cut_initiater, text="Cut")
        self.cut_audio_btn.grid(
            row=2, column=0, padx=10, pady=10, columnspan=2)

        ''' Merge Audios Frame '''
        self.merge_frm = Section(self.edtr_panel_frm, "Merge")
        self.merge_frm.place(x=298, y=170, width=290, height=200)

        self.merge_from_lbl = Label(self.merge_frm, text="Merge from (sec)")
        self.merge_from_lbl.grid(row=0, column=0, padx=10, pady=5)
        self.merge_from = Input(self.merge_frm)
        self.merge_from.grid(row=0, column=2, padx=10, pady=5)

        self.merge_gap_lbl = Label(self.merge_frm, text="Gap b/w merge (sec)")
        self.merge_gap_lbl.grid(row=1, column=0, padx=10, pady=5)

        self.merge_gap = Input(self.merge_frm)
        self.merge_gap.grid(row=1, column=2, padx=10, pady=5)

        self.merge_for_lbl = Label(self.merge_frm, text="Merge for (sec)")
        self.merge_for_lbl.grid(row=2, column=0, padx=10, pady=5)

        self.merge_for = Input(self.merge_frm)
        self.merge_for.grid(row=2, column=2, padx=10, pady=5)

        self.merge_btn = Button(
            self.merge_frm, self.merge_helper, text="Merge")
        self.merge_btn.grid(row=3, column=0, columnspan=3, padx=5, pady=10)

        self.root.mainloop()

    """******************** Core Functions ********************"""

    def playsong(self):
        if not self.is_audio_none():
            # self.active_audio_path = self.tr.get_file_path()
            self.tr = self.get_audio()
            extra = ""
            # pygame.mixer.music.load(
            #     f"./temp/{extra}temp_{self.active_audio_name}")
            self.playpauseicons.set(self.pause_icon)
            if self.tr.track.duration_seconds:
                pygame.mixer.music.play()

            else:
                stat = "Audio too short. Audio length is 0. Can't play that"
                self.task_completion_status(stat)

    def stopsong(self):
        if not self.is_audio_none():
            self.playpauseicons.set(self.play_icon)
            # pygame.mixer.music.stop()
            self.current_pos.set(
                f"?s/{round(float(self.tr.checkLength()),3)}s")

    def pausesong(self):
        self.playpauseicons.set(self.play_icon)
        # pygame.mixer.music.pause()

    def unpausesong(self):
        self.playpauseicons.set(self.pause_icon)
        # pygame.mixer.music.unpause()

    def changevolume(self, new_volume):
        # pygame.mixer.music.set_volume(int(new_volume) / 100)
        self.volume.set(int(new_volume))

    def muteunmute(self):
        # if mute case
        if int(self.volume.get()) == 0:
            self.changevolume(self.current_volume)
            self.muteunmuteicons.set(self.volume_full_icon)
        else:
            self.current_volume = self.volume.get()
            self.changevolume(0)
            self.muteunmuteicons.set(self.muted_icon)

    """******************** Helper Functions ********************"""

    def set_playing_status(self, status):
        self.status.set(status)

    def task_completion_status(self, status):
        self.task_status.set(status)

    def open(self):
        self.tr = Sound()

    def is_audio_none(self):
        return True if not self.tr else False

    def get_audio(self):
        return self.tr

    def ask_to_close(self):
        if messagebox.askokcancel("Quit?", "Do you really want to exit?"):
            self.root.destroy()

    def reduce_name(self, text, max_allowed=25):
        if not self.is_audio_none():
            if len(text) - 4 > max_allowed:
                text = text[: max_allowed - 3] + "..."
            return text

    def open_helper(self):
        self.task_completion_status("Opening...")
        print("\nopen_helper...before open()...")
        self.open()
        print("\nopen_helper...after open()...")

        self.tr = self.get_audio()
        if self.tr.get_file_name() != "":
            self.stopsong()
            self.tr.temp_save()
            self.active_audio_name = self.tr.get_file_name()
            self.track.set(self.reduce_name(self.active_audio_name))
            # print(self.active_audio_name)
            stat = "Opened! Ready to play."

            self.task_completion_status(stat)
            self.current_pos.set(
                f"?s/{round(float(self.tr.checkLength()),3)}s")
        else:
            self.task_completion_status("")

    def cut_initiater(self):
        if not self.is_audio_none():
            self.task_completion_status("Triming...")
            self.trimStart = self.trim_start_input.get()
            self.trimEnd = self.trim_end_input.get()
            try:
                self.trimStart = float(self.trimStart)
                self.trimEnd = float(self.trimEnd)
            except ValueError:
                pass
            self.stopsong()
            Sound.trim(self.tr, self.trimStart, self.trimEnd)
            stat = f"{self.track.get()} was successfully trimed."
            self.task_completion_status(stat)
            self.current_pos.set(
                f"?s/{round(float(self.tr.checkLength()),3)}s")

    def rev_helper(self):
        if not self.is_audio_none():
            self.task_completion_status("Reversing...")
            self.stopsong()
            Sound.reverse(self.tr)
            stat = f"{self.track.get()} was successfully reversed."
            self.task_completion_status(stat)

    def repeat_helper(self):
        if not self.is_audio_none():
            self.task_completion_status("Repeating Audio...")
            self.stopsong()
            Sound.repeat(self.tr)
            stat = f"{self.track.get()} was successfully repeated."
            self.task_completion_status(stat)
            self.current_pos.set(
                f"?s/{round(float(self.tr.checkLength()),3)}s")

    def overlay_helper(self):
        if not self.is_audio_none():
            self.task_completion_status("Overlaying Audios...")
            self.stopsong()
            second_audio_name = Sound.overlay(self.tr)
            if second_audio_name:
                stat = f"{self.reduce_name(second_audio_name)} overlayed on {self.track.get()}."
                self.task_completion_status(stat)
                self.current_pos.set(
                    f"?s/{round(float(self.tr.checkLength()),3)}s")
            else:
                self.task_completion_status("")

    def save_helper(self):
        if not self.is_audio_none():
            self.task_completion_status("Saving your awesome track...")
            new_name = Sound.save(self.tr)
            if not new_name:
                stat = f"Save UNSUCCESSFUL."
                self.task_completion_status(stat)
            else:
                self.track.set(self.reduce_name(new_name))
                stat = f"{self.reduce_name(new_name)} is successfully saved."
                self.task_completion_status(stat)

    def clear_helper(self):
        if not self.is_audio_none():
            self.task_completion_status("Clearing track and data...")
            self.stopsong()
            pygame.mixer.music.unload()
            self.tr = Sound.clearTrack(self.tr)
            self.track.set("")
            self.current_pos.set("?s/?s")
            stat = "Audio track along with undo redo data is now cleared."
            self.task_completion_status(stat)

    def undo_helper(self):
        if not self.is_audio_none():
            self.stopsong()
            successful = Sound.undo(self.tr)
            if successful:
                self.task_completion_status("Successful undo.")
                self.current_pos.set(
                    f"?s/{round(float(self.tr.checkLength()),3)}s")

    def redo_helper(self):
        if not self.is_audio_none():
            self.stopsong()
            successful = Sound.redo(self.tr)
            if successful:
                self.task_completion_status("Successful redo.")
                self.current_pos.set(
                    f"?s/{round(float(self.tr.checkLength()),3)}s")

    def merge_helper(self):
        if not self.is_audio_none():
            self.task_completion_status("Merging...")
            gap = self.merge_gap.get()
            merge_from = self.merge_from.get()
            merge_for = self.merge_for.get()
            if not gap:
                gap = 0
            if merge_for != "":
                merge_for = float(merge_for)
            if not merge_from:
                merge_from = self.tr.checkLength()
            self.stopsong()
            other_audio = Sound.gapMerge(self.tr, merge_from, merge_for, gap)
            if other_audio:
                self.task_completion_status(
                    f"{self.track.get()} merged with {other_audio}."
                )
                self.current_pos.set(
                    f"?s/{round(float(self.tr.checkLength()),3)}s")
            else:
                self.task_completion_status("")

    def playpause(self):
        if not self.is_audio_none():
            pass
            # if pygame.mixer.music.get_pos() == -1:
            #     self.playsong()
            # elif pygame.mixer.music.get_busy():
            #     self.pausesong()
            #     self.current_pos.set(
            #         f"{(pygame.mixer.music.get_pos() / 1000)}s/{round(float(self.tr.checkLength()),3)}s"
            #     )
            # else:
            #     self.unpausesong()


if __name__ == "__main__":
    AudioEditor()
