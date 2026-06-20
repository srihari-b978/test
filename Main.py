import tkinter as tk
import random

from Movies import movies_by_language, moods


BUTTON_BG = "#4A90E2"
BUTTON_FG = "white"
BUTTON_ACTIVE_BG = "#357ABD"
BUTTON_ACTIVE_FG = "white"
WINDOW_BG = "#F2F6FC"
CARD_BG = "white"
TEXT_COLOR = "#333333"


class StyledButton(tk.Button):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            bg=BUTTON_BG,
            fg=BUTTON_FG,
            activebackground=BUTTON_ACTIVE_BG,
            activeforeground=BUTTON_ACTIVE_FG,
            relief="raised",
            bd=0,
            highlightthickness=0,
            font=("Helvetica", 11, "bold"),
            cursor="hand2",
            **kwargs,
        )


class LanguageFrame(tk.Frame):
    def __init__(self, parent, on_language_selected):
        super().__init__(parent, bg=CARD_BG, bd=0, padx=20, pady=20)
        tk.Label(self, text="Select your language", font=("Helvetica", 17, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(pady=(0, 15))

        languages = [
            ("Malayalam", "malayalam"),
            ("English", "english"),
            ("Hindi", "hindi"),
            ("Japanese", "japanese"),
            ("Tamil", "tamil"),
            ("Korean", "korean"),
        ]

        for display_name, language_key in languages:
            btn = StyledButton(
                self,
                text=display_name,
                width=20,
                command=lambda lang=language_key: on_language_selected(lang),
            )
            btn.pack(pady=6, fill="x")


class MoodFrame(tk.Frame):
    def __init__(self, parent, on_mood_selected, on_back):
        super().__init__(parent, bg=CARD_BG, bd=0, padx=20, pady=20)
        tk.Label(self, text="Select your mood", font=("Helvetica", 17, "bold"), bg=CARD_BG, fg=TEXT_COLOR).pack(pady=(0, 15))

        for mood in moods:
            btn = StyledButton(
                self,
                text=mood,
                width=20,
                command=lambda m=mood: on_mood_selected(m),
            )
            btn.pack(pady=6, fill="x")

        StyledButton(self, text="Back", width=20, command=on_back).pack(pady=(20, 0), fill="x")


class MoodMoviePickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mood Movie Picker")
        self.root.geometry("500x560")
        self.root.configure(bg=WINDOW_BG)
        self.root.resizable(False, False)

        header = tk.Frame(root, bg=WINDOW_BG)
        header.pack(pady=(15, 0))

        tk.Label(
            header,
            text="🎬 Mood Movie Picker",
            font=("Helvetica", 22, "bold"),
            bg=WINDOW_BG,
            fg=TEXT_COLOR,
        ).pack()

        tk.Label(
            header,
            text="Pick a language and a mood to get a movie suggestion.",
            font=("Helvetica", 11),
            bg=WINDOW_BG,
            fg="#555555",
        ).pack(pady=(6, 0))

        self.message_label = tk.Label(
            root,
            text="Choose a language first.",
            font=("Helvetica", 12),
            bg=WINDOW_BG,
            fg="#555555",
        )
        self.message_label.pack(pady=(15, 10))

        self.card = tk.Frame(root, bg=CARD_BG, bd=0, highlightbackground="#DCE4EE", highlightthickness=1)
        self.card.pack(padx=20, pady=(0, 10), fill="both", expand=True)

        self.main_frame = tk.Frame(self.card, bg=CARD_BG)
        self.main_frame.pack(expand=True, fill="both")

        self.language_frame = LanguageFrame(self.main_frame, self.on_language_selected)
        self.mood_frame = MoodFrame(self.main_frame, self.on_mood_selected, self.on_back_to_language)

        self.language_frame.pack(expand=True, fill="both")

        self.result_frame = tk.Frame(root, bg=WINDOW_BG)
        self.result_frame.pack(pady=(0, 10), fill="x")

        self.result_label = tk.Label(
            self.result_frame,
            text="",
            font=("Helvetica", 13, "bold"),
            bg=WINDOW_BG,
            fg="#1E3A8A",
            wraplength=460,
            justify="center",
        )
        self.result_label.pack(pady=10, padx=10)

        self.selected_language = None

    def on_language_selected(self, language_key):
        self.selected_language = language_key
        self.message_label.config(text=f"Language selected: {language_key.title()}. Now pick a mood.")
        self.language_frame.pack_forget()
        self.mood_frame.pack(expand=True, fill="both")
        self.result_label.config(text="")

    def on_mood_selected(self, mood):
        if not self.selected_language:
            self.result_label.config(text="Please select a language first.")
            return

        movie = suggest_movies(self.selected_language, mood)
        if movie:
            self.result_label.config(
                text=f"Suggested {mood} movie in {self.selected_language.title()}:\n{movie}"
            )
        else:
            self.result_label.config(
                text=f"No movie found for {self.selected_language.title()} and mood '{mood}'."
            )

    def on_back_to_language(self):
        self.selected_language = None
        self.message_label.config(text="Choose a language first.")
        self.mood_frame.pack_forget()
        self.language_frame.pack(expand=True, fill="both")
        self.result_label.config(text="")


def suggest_movies(language, mood):
    language = language.lower()
    mood = mood.title()
    language_data = movies_by_language.get(language)
    if not language_data:
        return None
    mood_movies = language_data.get(mood)
    if not mood_movies:
        return None
    return random.choice(mood_movies)


if __name__ == "__main__":
    root = tk.Tk()
    app = MoodMoviePickerApp(root)
    root.mainloop()
