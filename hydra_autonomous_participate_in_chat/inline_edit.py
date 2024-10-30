import readline

# Pre-fill the input buffer with a default string
readline.set_startup_hook(lambda: readline.insert_text('Hello, World!'))

# Get the user to modify the string
modified_string = input("Edit the string: ")

# Read the modified string
print("You modified it to:", modified_string)

# Reset the startup hook after the first input
readline.set_startup_hook()
