# AutoClicker - User Guide

## Overview
AutoClicker is an advanced tool that automates the process of clicking on specified images (like buttons) on your screen. It's perfect for automating repetitive tasks or interacting with elements on a webpage or application.

This guide will walk you through how to install, use, and customize the tool for your needs.

## Installation Instructions

### Download the Application
Ensure that you have downloaded the AutoClicker folder, which contains the Python script and necessary files (including `icon.ico` for the system tray icon).

### Run the Executable (Optional)
You can also run the application directly from the provided executable. The executable is included in a zip folder. Simply extract the zip folder and run the app by launching `AutoClickerGUI.py` without needing to install Python or dependencies.

### Install Dependencies
Make sure Python is installed on your computer. You can download it from [here](https://www.python.org/downloads/).

Install required Python libraries. Open a command prompt or terminal and run the following command:

```bash
pip install pyautogui pystray keyboard customtkinter pillow
```

### Run the Application
Double-click the `AutoClickerGUI.py` file to launch the application.

## User Interface Overview
Upon starting the application, you will see the following sections:

### Control Panel
- **Upload Images:** Click this to upload images (e.g., screenshots of buttons you want to click).
- **Save Profile:** Save your current settings to a JSON profile.
- **Load Profile:** Load a saved profile with your preferences and images.
- **Start (▶️):** Start the automated clicking process.
- **Stop (⏹️):** Stop the automated clicking process.

### Listbox
- Displays the images you've uploaded.
- You can reorder images by dragging them up or down in the list.

### Settings Panel
- **Confidence:** Adjust the image matching confidence (higher values mean more accuracy).
- **Clicks per Image:** Set how many times the tool will click on a found image.
- **Max Loops:** Set the number of times the process will repeat. A value of 0 means infinite loops.
- **Search Delay:** Delay between search attempts when trying to locate images.
- **Cycle Delay:** Delay between each cycle of image searching and clicking.
- **Theme Switch:** Switch between light and dark themes.

### Log Panel
- Displays real-time log information of actions being taken (e.g., which image was clicked, current cycle, errors, etc.).
- **Export Log:** Export the log to a `.txt` file for review.

## How to Use AutoClicker

1. **Upload Images**  
   Click the Upload Images button and select the images of the buttons or areas you want the tool to click.  
   Only PNG, JPG, and JPEG formats are supported.

2. **Configure Settings**  
   - **Confidence:** Adjust the slider to set the confidence level for image matching. A higher value (e.g., 0.9) means more precise matching, while lower values (e.g., 0.5) allow for some flexibility.  
   - **Clicks per Image:** Set how many times you want the tool to click each image when found.  
   - **Max Loops:** If you want the process to stop after a certain number of loops, set a number here. If you want it to run indefinitely, leave it as 0.  
   - **Search Delay:** Set a delay between search attempts if the image is not found initially.  
   - **Cycle Delay:** Set a delay between cycles of image clicks (useful for applications like refreshing a browser tab).

3. **Start the Clicking Process**  
   After uploading images and configuring your settings, click the Start (▶️) button to begin the automated clicking process.  
   The tool will continuously search for and click on the images in the order they were uploaded. The number of clicks per image and confidence settings will guide how the tool interacts with the images.

4. **Stop the Clicking Process**  
   Click the Stop (⏹️) button to stop the automated clicking process. You can also stop it by closing the window or using the system tray icon.

5. **Use Hotkeys**  
   You can use the F3 hotkey to start or stop the automated clicking process at any time.

## System Tray Icon
The tool also minimizes to the system tray (next to the clock on your desktop) for convenience.

The system tray icon allows you to:
- Show the application window.
- Start/Stop the clicking process.
- Exit the application.

## Saving and Loading Profiles
- **Save Profile:** After configuring your settings and uploading images, you can save your profile to a `.json` file. This makes it easy to reload your setup in the future.
- **Load Profile:** You can load previously saved profiles by clicking the Load Profile button. This will restore the images and settings from the saved file.

## Troubleshooting

### Image Not Found Error
If the tool cannot find an image on the screen, it will retry until it's found or the max loops are reached. Ensure the images are clearly visible on your screen and not obstructed by other windows.

### System Tray Icon Missing
If the tray icon doesn't appear, make sure you have the `icon.ico` file in the same directory as the script. If it’s missing, the tool will create a temporary one.

## Exporting Logs
All activities are logged in real-time in the Log Panel.

You can export the log to a `.txt` file by clicking the Export Log button.

For any support, feel free to contact me.

If you need any additional modifications or have questions, feel free to reach out!
