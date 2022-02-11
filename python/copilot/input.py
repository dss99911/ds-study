#%%
def get_user_names():
    """ask user to enter the names, one per line"""
    names = []
    while True:
        name = input("Enter a name (blank to quit): ")
        if name == "":
            break
        names.append(name)
    return names