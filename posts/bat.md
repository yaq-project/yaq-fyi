---
title: Use BAT Files to Launch yaq
id: bat
date: 2023-05-18
authors: Blaise Thompson
---

Some of our graphical applications are only accessible via the command line.
It can be annoying, on a Windows machine, to open Anaconda Prompt and then type 'yaqc-qtpy'.
Instead, consider using a bat file.
Here's one the Krishna group uses to launch yaqc-qtpy.

    call C:\Users\KrishnaLab\miniconda3\Scripts\activate.bat
    call yaqc-qtpy

Just put that on your desktop and call it "yaqc-qtpy.bat", you've got a clickable launcher for the application.
There are lots of tutorials about bat files on the internet.
You can even run them as administrator!
Useful tool when trying to make your instrument a little bit more user-friendly.