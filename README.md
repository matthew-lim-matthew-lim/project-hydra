# project-hydra
Automation at it's finest

# hardcore_headless_hydra_autonomous_participate -> `hydra_hardcore_v1.py`

**Requires OpenAI API Key**

Truly autonomous chat participation. Automatically read and reply to mutliple people/chats on a schedule.

The program will autonomously message targets in cycles, only within restricted hours (eg. sending messages only before 2am and after 6am).

#### On running the program: 
- You are prompted to enter the time between each hydra cycle in hours (decimals accepted). At each cycle, the bot checks for messages and either sends or will wait until a following hydra cycle to double text (See: `Optional Arguments` section).
- Then, you are prompted to insert the target chats, whether partial chat names is allowed, and for topics you would like the chat to involve. Each of these is seperated by `\`. You can insert as many targets as you would like.
    - Example: `Kimi Räikkönen\N\Monaco GP, Pickleball, Baccarat`

### Optional Arguments:

- Argument 1: 
    - `dt` double-text: If you got seenzoned or sentzoned (rip), the bot can generate a message anyway. By default the bot does not double-text.
        - Example: `python3 hydra_v3.py dt` (the bot will double text 🥶).
    - `[integer accepted no-replies]`: The number of cycles where you have recieved no-reply before you will double text.
        - Example: `python3 hydra_v3.py 3` (the bot will wait 3 cycles with no reply, before double texting 😭😿).

### Running the scripts truly autonomously

To run the scripts autonomously, you can either:
- Use a Cloud-based VM
- Leave it running on your device, or a Raspberry Pi (and etc)

If you are using a Cloud-based VM or plan to close your terminal, you will need to use something like `tmux`, which allows the process to continue in the background.

Usage:

- Start a new `tmux` session:
```
tmux new -s mysession
```
- Detach from the `tmux` session by pressing `Ctrl + B` followed by `D`.
- Reattach to a `tmux` session:
```
tmux attach -t mysession
```
- View active `tmux` sessions:
```
tmux ls
```

### Future Work:

Maybe work on a version that uses `cron` to schedule running the program, helping reducing system load?

# hydra_autonomous_participate_in_chat -> `hydra_v3.py` (and etc versions)

**Requires OpenAI API Key**

Reads a messenger chat and generates a response. 
Upon generating a message, the user may select from the options:
- 'Y' to send
- 'R' to regenerate response (uses feedback provided by user in earlier 'F' inputs for this chat message)
- 'M' to manually modify response
- 'F' to provide feedback and regenerate response
- 'N' to exit program

Takes in a Chat name.

### Example Usage:

`python3 hydra_v3.py`

### Optional Arguments:

- `dt` double-text: If you got seenzoned or sentzoned (rip), the bot can generate a message anyway. By default the bot does not double-text.
    - Example: `python3 hydra_v3.py dt`

# hydra_group_chat_dm_all -> `hydra_group_chat_dm_all.py` 

**Does not require OpenAI API Key**

Automatically DMs a particular message to all members in a specific group chat.

Takes in the Chat Name, and the message to send to all members in that chat.

### Example Usage:

`python3 hydra_group_chat_dm_all.py`