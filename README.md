# project-hydra
Automation at it's finest

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