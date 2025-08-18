# File Organizer for Windows

This project has a Python script that helps organize files on Windows computers. The program searches for image files, videos, and Excel spreadsheets on all drives, except for system and protected folders, and moves them to specific destination folders.

# Why I made this
My parents have an old computer that I wanted to turn into a homelab. They agreed, but only if I saved all the photos they had on it to send to their newer computer. There were about 8,000 photos spread across many messy folders. So, I decided to make a Python script to scan and organize these files automatically.

## Features

- **Automatic search:** Scans all drives on the computer.
- **Smart filtering:** Ignores system folders and files already in the destination folders.
- **Safe moving:** Moves images, videos, and spreadsheets to organized folders.
- **Activity log:** Creates detailed logs of the process, including moved, skipped, and error files.
- **Simple interface:** Asks for user confirmation before starting.

## How to use

1. Make sure you are using Windows.
2. Run the `main.py` script with Python 3.
3. Follow the instructions in the terminal to start organizing your files.

## Notes

- Destination folders are set directly in the code.
- The script may need admin permissions to access all drives and folders.
- You can stop the process anytime by pressing `Ctrl+C`.

---

**Attention:** Before running, check the destination folders set in the code to make sure they
