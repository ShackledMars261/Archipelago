# Setup Guide for ArchipelaCode

## Required Software and Accounts

- [An updated installation of Visual Studio Code](https://code.visualstudio.com/Download)

- [A LeetCode account](https://leetcode.com/accounts/login/)

## Instructions

1. Install the ArchipelaCode extension for VS Code.
    You can either search for it in the VS Code extensions view (on the left), or you can click [this link](vscode:extension/ShackledMars261.archipelacode). Once on the extension's page, click the "Install" button. There should be an Archipelago icon on the left side of your window now.

2. Create a new workspace for Archipelago. Create a new folder somewhere on your drive, and then open that folder in VS Code by clicking "Open..." on the Welcome screen.

## Connecting to the Archipelago server

1. To connect to the multiworld server, open the Command Palette. (This should be `Ctrl + Shift + P` on Windows / Linux, and `Command + Shift + P` on macOS)

2. Type in `Start ArchipelaCode Session`, and select the `ArchipelaCode: Start ArchipelaCode Session` entry.

3. Enter the connection info for your mutiworld server into the boxes when prompted. If you do not have a password, you can leave that field empty.

4. When prompted to open an external web page, click open, sign into LeetCode (if it requests it), and then click the "Open Visual Studio Code" button.

Now that you have connected once, you should be able to use the `ArchipelaCode: Reconnect to last Archipelago Session` command (also in the Command Palette) to quickly reconnect to both LeetCode and the previous multiworld server.

## Opening a problem in ArchipelaCode

On the left side of your window, there should be an Archipelago icon. Clicking on that (while connected to Archipelago) will open the Problem Explorer, which contains dropdowns for various categories of problems. I would recommend mostly using the "Available" dropdown. Clicking on any of the problems in the Explorer will let you select the language you want to use, and then it will either open your previous work (if it exists) or create a new file, and prefill in the starter code that LeetCode provides.

## Submitting your work to LeetCode

In order to "check" locations, you must submit your code to LeetCode through the extension to verify that it works. Once connected to Archipelago, you can use the `ArchipelaCode: Submit current code to LeetCode` command in the Command Palette to submit the code in the current editor. This will verify that the problem is "Available" to you and that you aren't using any Language Features that you haven't unlocked yet, before sending your code to LeetCode to make sure it works. If all of these checks pass, the location will be marked as done, and you will receive your item.

## The Output Channel

The output channel will be your best friend. It shows all messages received from the Multiworld server, which items you are missing if you fail a problem submission, and more. To access it, open a Terminal in VS Code (after connecting to the Multiworld) and click the Output tab. Then, click the dropdown in the top right of the panel, and select "ArchipelaCode".

## Commands

The ArchipelaCode Extension creates a few commands in the Command Palette for you to use:
- `ArchipelaCode: Start ArchipelaCode Session` - Starts a new session of Archipelago.
- `ArchipelaCode: Reconnect to last Archipelago Session` - Attempts to connect to your last Archipelago session.
- `ArchipelaCode: Disconnect from Archipelago` - Disconnects from Archipelago.
- `ArchipelaCode: Submit current code to LeetCode` - Submits the currently opened problem to LeetCode for verification. This is how you "check" a location.
- `ArchipelaCode: Send Message to Archipelago` - Allows you to send a message to the Multiworld. You can use this to run AP commands like `!status` or `!hint item_name`, as well as send chat messages.
- `ArchipelaCode: List your currently unlocked "Language Features"` - Lists the items you currently have in the output channel.
- `ArchipelaCode: Opens the current Problem on LeetCode` - Opens the LeetCode page for the current problem in your browser.
- `ArchipelaCode: Opens a Problem in the Editor` - Necessary for the Problem Explorer to function. You don't need to use this.