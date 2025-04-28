# import libs
import requests
import re

# set the url
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

# fetch HTML content
html_content = requests.get(url).text

# find all table structure
cells = re.findall(r'<td.*?>(.*?)</td>', html_content, re.DOTALL)

# skip the first 3 header cells (x-coordinate, character, y-coordinate)
cells = cells[3:]

# function to clean HTML and extract text
def clean_html(raw_html):
    return re.sub(r'<.*?>', '', raw_html).strip()

# parse cells into triplets (x, char, y)
points = []
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for i in range(0, len(cells), 3):
    x_raw = clean_html(cells[i])
    char = clean_html(cells[i+1])
    y_raw = clean_html(cells[i+2])

    try:
        x = int(x_raw)
        y = int(y_raw)
    except ValueError:
        continue

    points.append((x, y, char))

    # Keep track of the boundaries
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

# normalize the coordinates
offset_x = -min(0, min_x)
offset_y = -min(0, min_y)

# calculate the grid width and height
width = max_x + offset_x + 1
height = max_y + offset_y + 1

# create the grid with correct dimensions
grid = [[' ' for _ in range(width)] for _ in range(height)]

# place characters on the grid
for x, y, char in points:
    grid[y + offset_y][x + offset_x] = char

# print the grid in the correct orientation
for row in reversed(grid):  # Reverse to correct the upside-down issue
    print(''.join(row))
