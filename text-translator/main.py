"""
This file builds the text translator app as seen on the GitHub repo at
https://github.com/Mrinank-Bhowmick/python-beginner-projects/tree/main/projects/text-translate

I will try to use as much latest packages as possible and if not, then
fallback to old versions.

This file is run on my Mac so no need to install `tkinter` via pip or uv.
macOS and Linux come installed with tkinter. so install tkinter if on Windows.
"""

# The idea is to build a gui that is similar to google translate.
# tkinter is like Java's Swing framework which lets you build GUIs using
# Programmable and Composable Elements

import asyncio
import threading
import tkinter as tk
import tkinter.ttk as ttk

import googletrans as gt

LANGUAGES = sorted([
    "en",
    "es",
    "pt",
    "zh",
    "fr",
    "de",
    "it",
    "ja",
    "ko",
    "ru",
    "ar",
    "nl",
    "el",
    "hi",
    "tr",
    "sv",
    "pl",
    "vi",
    "th",
    "he",
])


async def translate(text, from_lang, to_lang):
    if from_lang not in LANGUAGES or to_lang not in LANGUAGES:
        # Instead of raising an error, fallback to safety
        from_lang = "en"
        to_lang = "en"

    translator = gt.Translator()

    result = await translator.translate(text, dest=to_lang, src=from_lang)

    return result.text



async def create_app():
    # Create Window of the app
    app = tk.Tk()
    app.title("Text Translator")
    app.geometry("400x300")
    app.resizable(True, True)
    app.configure(background='light blue')

    input_label = ttk.Label(app, text="Enter the text:", background="light blue")
    input_entry = ttk.Entry(app, width=30)

    from_lang_label = ttk.Label(app, text="From language:", background="light blue")
    from_lang_var = tk.StringVar(value="en")
    from_lang_dropdown = ttk.Combobox(app, textvariable=from_lang_var, values=LANGUAGES, state="readonly")

    to_lang_label = ttk.Label(app, text="To language:", background="light blue")
    to_lang_var = tk.StringVar(value="es")
    to_lang_dropdown = ttk.Combobox(app, textvariable=to_lang_var, values=LANGUAGES, state="readonly")

    result_label = ttk.Label(
        app, text="Translation will appear here", wraplength=350,
        background="light blue"
    )

    def on_translate():
        text = input_entry.get()
        from_lang = from_lang_var.get()
        to_lang = to_lang_var.get()
        result_label.config(text="Translating...")

        def run_in_thread():
            # Run in a separate thread so we can create a fresh event loop —
            # the outer asyncio loop is blocked by mainloop() but still
            # considered "running", so run_until_complete() would raise
            # RuntimeError if called on the same thread.
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                translated = loop.run_until_complete(translate(text, from_lang, to_lang))
            except Exception as e:
                translated = f"Error: {e}"
            finally:
                loop.close()
            app.after(0, lambda: result_label.config(text=translated))

        threading.Thread(target=run_in_thread, daemon=True).start()

    translate_button = ttk.Button(app, text="Translate", command=on_translate)

    # Arrange widgets in the grid
    input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    input_entry.grid(row=0, column=1, padx=10, pady=10)
    from_lang_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    from_lang_dropdown.grid(row=1, column=1, padx=10, pady=10)
    to_lang_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    to_lang_dropdown.grid(row=2, column=1, padx=10, pady=10)
    translate_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    # Start the app
    app.mainloop()


asyncio.run(create_app())
