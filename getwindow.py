import pygetwindow as gw

# Get a list of all open windows
windows = gw.getAllTitles()

# Print the titles of all open windows
for window in windows:
    if window:  # Only print non-empty window titles
        print(window)