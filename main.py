import asyncio

from pyscript import document
from pyodide.ffi import create_proxy


# ==========================================
# DATA
# ==========================================

array = [4, 8, 15, 23, 42, 67, 91]
target = 42

current_algorithm = "linear"


# ==========================================
# GET HTML ELEMENTS
# ==========================================

array_element = document.querySelector("#array")
status_element = document.querySelector("#status")
code_element = document.querySelector("#code")


# ==========================================
# DISPLAY ARRAY
# ==========================================

def display_array():

    array_element.innerHTML = ""

    for value in array:

        box = document.createElement("div")

        box.className = "box"
        box.innerText = str(value)

        array_element.appendChild(box)


# ==========================================
# SHOW LINEAR SEARCH CODE
# ==========================================

def show_linear_code():

    code_element.innerText = """def linear_search(array, target):

    for i in range(len(array)):

        if array[i] == target:
            return i

    return -1
"""


# ==========================================
# SHOW BINARY SEARCH CODE
# ==========================================

def show_binary_code():

    code_element.innerText = """def binary_search(array, target):

    left = 0
    right = len(array) - 1

    while left <= right:

        mid = (left + right) // 2

        if array[mid] == target:
            return mid

        elif array[mid] < target:
            left = mid + 1

        else:
            right = mid - 1

    return -1
"""


# ==========================================
# LINEAR SEARCH
# ==========================================

async def linear_search():

    display_array()

    boxes = document.querySelectorAll(".box")

    comparisons = 0

    for i in range(len(array)):

        comparisons += 1

        boxes[i].style.backgroundColor = "yellow"

        status_element.innerText = (
            f"Checking index {i} → {array[i]} "
            f"| Comparisons: {comparisons}"
        )

        await asyncio.sleep(0.8)

        if array[i] == target:

            boxes[i].style.backgroundColor = "lightgreen"

            status_element.innerText = (
                f"Found {target} at index {i}! "
                f"| Comparisons: {comparisons}"
            )

            return

        boxes[i].style.backgroundColor = "lightgray"


    status_element.innerText = (
        f"{target} not found."
    )


# ==========================================
# BINARY SEARCH
# ==========================================

async def binary_search():

    display_array()

    boxes = document.querySelectorAll(".box")

    left = 0
    right = len(array) - 1

    comparisons = 0

    while left <= right:

        # Reset colors
        for box in boxes:
            box.style.backgroundColor = "white"

        mid = (left + right) // 2

        comparisons += 1

        boxes[mid].style.backgroundColor = "yellow"

        status_element.innerText = (
            f"Checking middle index {mid} → {array[mid]} "
            f"| Comparisons: {comparisons}"
        )

        await asyncio.sleep(1)

        if array[mid] == target:

            boxes[mid].style.backgroundColor = "lightgreen"

            status_element.innerText = (
                f"Found {target} at index {mid}! "
                f"| Comparisons: {comparisons}"
            )

            return

        elif array[mid] < target:

            for i in range(left, mid + 1):
                boxes[i].style.backgroundColor = "lightgray"

            left = mid + 1

        else:

            for i in range(mid, right + 1):
                boxes[i].style.backgroundColor = "lightgray"

            right = mid - 1

        await asyncio.sleep(0.8)


    status_element.innerText = (
        f"{target} not found."
    )


# ==========================================
# BUTTON FUNCTIONS
# ==========================================

def select_linear(event):

    global current_algorithm

    current_algorithm = "linear"

    show_linear_code()

    status_element.innerText = (
        "Linear Search selected. Click Start Animation."
    )


def select_binary(event):

    global current_algorithm

    current_algorithm = "binary"

    show_binary_code()

    status_element.innerText = (
        "Binary Search selected. Click Start Animation."
    )


def start_animation(event):

    if current_algorithm == "linear":

        asyncio.ensure_future(
            linear_search()
        )

    else:

        asyncio.ensure_future(
            binary_search()
        )


# ==========================================
# CREATE JAVASCRIPT CALLBACKS
# ==========================================

linear_proxy = create_proxy(select_linear)

binary_proxy = create_proxy(select_binary)

start_proxy = create_proxy(start_animation)


# ==========================================
# CONNECT BUTTONS
# ==========================================

document.querySelector(
    "#linear-button"
).addEventListener(
    "click",
    linear_proxy
)


document.querySelector(
    "#binary-button"
).addEventListener(
    "click",
    binary_proxy
)


document.querySelector(
    "#start-button"
).addEventListener(
    "click",
    start_proxy
)


# ==========================================
# INITIAL STATE
# ==========================================

display_array()

show_linear_code()

status_element.innerText = (
    "Linear Search selected. Click Start Animation."
)