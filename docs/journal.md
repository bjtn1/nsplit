# 2025-04-18
It's not a good idea to put everything about my programs -- core logic and functions, etc -- all in main.py
I'm refactoring this project to make it more manageable to expand in the future, as well as make it easier to test

# 2025-04-19
I think it makes more sense to have split_file() return the path of the newly created `.split` directory for testing purposes
I don't need to pass both the filename AND the filepath to split_file(). Just passing the filepath and calling os.path.basename(filepath)
should get me the filename, making the functions easier to use and read.
