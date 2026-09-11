from pyscript import document, window

import asyncio
import math
import io
import contextlib


# ============================================================
# DOM HELPERS
# ============================================================

def get_area():
    return document.getElementById("animation-area")


def get_code_editor():
    return document.getElementById("lesson-code")


def get_output():
    return document.getElementById("lesson-output")


def clear_area():
    area = get_area()

    if area:
        area.innerHTML = ""


def set_output(text):
    output = get_output()

    if output:
        output.innerText = str(text)


# ============================================================
# PYTHON CODE EDITOR
# ============================================================

def handle_editor_keydown(event):
    """
    Make the Tab key insert four spaces
    instead of moving focus away from the editor.
    """

    if event.key != "Tab":
        return

    event.preventDefault()

    editor = event.currentTarget

    start = editor.selectionStart
    end = editor.selectionEnd

    editor.value = (
        editor.value[:start]
        + "    "
        + editor.value[end:]
    )

    editor.selectionStart = start + 4
    editor.selectionEnd = start + 4


# ============================================================
# PYTHON CODE EXECUTION
# ============================================================

async def execute_python():
    """
    Execute the Python code currently inside
    the lesson-code textarea.
    """

    editor = get_code_editor()

    if editor is None:
        set_output("Code editor not found.")
        return

    code = editor.value

    if not code.strip():
        set_output("Write some Python code erertert first.")
        return

    set_output("Running...")

    await asyncio.sleep(0.05)

    output = io.StringIO()

    try:
        execution_globals = {
            "__name__": "__main__"
        }

        with contextlib.redirect_stdout(output):
            exec(
                code,
                execution_globals
            )

        result = output.getvalue()

        if result.strip():
            set_output(
                result.rstrip()
            )
        else:
            set_output(
                "Code ran successfully with no printed output."
            )

    except Exception as error:
        set_output(
            f"{type(error).__name__}: {error}"
        )


def run_code():
    """
    Start Python execution asynchronously.
    """

    asyncio.ensure_future(
        execute_python()
    )


# ============================================================
# JAVASCRIPT → PYTHON BRIDGE
# ============================================================

# Allows app.js to call:
#
# window.runPythonCode()
#
window.runPythonCode = run_code


# ============================================================
# ANIMATION HELPERS
# ============================================================

def make_message(text):
    message = document.createElement("div")

    message.className = "animation-message"
    message.innerText = text

    return message


def make_panel():
    panel = document.createElement("div")

    panel.style.padding = "18px"
    panel.style.border = "1px solid #dce5df"
    panel.style.borderRadius = "12px"
    panel.style.background = "#ffffff"
    panel.style.marginTop = "15px"

    return panel


def make_title(text):
    title = document.createElement("h3")

    title.innerText = text
    title.style.margin = "0 0 15px"
    title.style.color = "#163f32"

    return title


# ============================================================
# LIST ANIMATION
# ============================================================

async def animate_list():
    clear_area()

    area = get_area()

    if area is None:
        return

    panel = make_panel()

    panel.appendChild(
        make_title(
            "List animation"
        )
    )

    values = [
        72,
        85,
        91,
        68,
        88
    ]

    wrapper = document.createElement("div")

    wrapper.style.display = "flex"
    wrapper.style.flexWrap = "wrap"
    wrapper.style.gap = "10px"

    elements = []

    for value in values:
        item = document.createElement("div")

        item.innerText = str(value)

        item.style.padding = "13px 18px"
        item.style.borderRadius = "10px"
        item.style.background = "#e8f0e9"
        item.style.color = "#163f32"
        item.style.fontFamily = "monospace"
        item.style.fontWeight = "700"
        item.style.transition = ".3s ease"
        item.style.opacity = "0"

        wrapper.appendChild(item)

        elements.append(item)

    panel.appendChild(wrapper)

    message = make_message(
        "The loop visits each item."
    )

    panel.appendChild(message)

    area.appendChild(panel)

    for element in elements:

        element.style.opacity = "1"
        element.style.transform = "translateY(-4px)"
        element.style.background = "#28664f"
        element.style.color = "white"

        await asyncio.sleep(0.55)

        element.style.transform = "translateY(0)"
        element.style.background = "#e8f0e9"
        element.style.color = "#163f32"


# ============================================================
# MEAN ANIMATION
# ============================================================

async def animate_mean():
    clear_area()

    area = get_area()

    if area is None:
        return

    panel = make_panel()

    panel.appendChild(
        make_title(
            "Mean animation"
        )
    )

    values = [
        10,
        20,
        30,
        40,
        50
    ]

    mean = sum(values) / len(values)

    wrapper = document.createElement("div")

    wrapper.style.display = "flex"
    wrapper.style.flexWrap = "wrap"
    wrapper.style.gap = "10px"

    elements = []

    for value in values:

        item = document.createElement("div")

        item.innerText = str(value)

        item.style.padding = "13px 18px"
        item.style.borderRadius = "10px"
        item.style.background = "#e8f0e9"
        item.style.color = "#163f32"
        item.style.fontWeight = "700"
        item.style.fontFamily = "monospace"
        item.style.transition = ".3s ease"

        wrapper.appendChild(item)

        elements.append(item)

    panel.appendChild(wrapper)

    message = make_message(
        f"Mean = {mean:.2f}"
    )

    panel.appendChild(message)

    area.appendChild(panel)

    for element in elements:

        element.style.background = "#28664f"
        element.style.color = "white"
        element.style.transform = "translateY(-5px)"

        await asyncio.sleep(0.3)

        element.style.background = "#e8f0e9"
        element.style.color = "#163f32"
        element.style.transform = "translateY(0)"


# ============================================================
# VARIANCE ANIMATION
# ============================================================

async def animate_variance():
    clear_area()

    area = get_area()

    if area is None:
        return

    values = [
        10,
        20,
        30,
        40,
        50
    ]

    mean = sum(values) / len(values)

    variance = sum(
        (x - mean) ** 2
        for x in values
    ) / len(values)

    panel = make_panel()

    panel.appendChild(
        make_title(
            "Variance animation"
        )
    )

    message = make_message(
        f"Mean = {mean:.2f}"
    )

    panel.appendChild(message)

    area.appendChild(panel)

    for value in values:

        difference = value - mean
        squared = difference ** 2

        message.innerText = (
            f"{value} − {mean:g} = "
            f"{difference:g} → "
            f"{squared:g}"
        )

        await asyncio.sleep(0.7)

    message.innerText = (
        f"Variance = {variance:.2f}"
    )


# ============================================================
# CORRELATION
# ============================================================

def calculate_correlation(
    x_values,
    y_values
):
    n = min(
        len(x_values),
        len(y_values)
    )

    if n < 2:
        return 0

    x_values = x_values[:n]
    y_values = y_values[:n]

    mean_x = sum(x_values) / n
    mean_y = sum(y_values) / n

    numerator = sum(
        (x - mean_x) * (y - mean_y)
        for x, y in zip(
            x_values,
            y_values
        )
    )

    denominator_x = math.sqrt(
        sum(
            (x - mean_x) ** 2
            for x in x_values
        )
    )

    denominator_y = math.sqrt(
        sum(
            (y - mean_y) ** 2
            for y in y_values
        )
    )

    denominator = (
        denominator_x
        * denominator_y
    )

    if denominator == 0:
        return 0

    return numerator / denominator


async def animate_correlation():
    clear_area()

    area = get_area()

    if area is None:
        return

    panel = make_panel()

    panel.appendChild(
        make_title(
            "Correlation"
        )
    )

    message = make_message(
        "Points are displayed from left to right."
    )

    panel.appendChild(message)

    area.appendChild(panel)

    x_values = [
        1,
        2,
        3,
        4,
        5
    ]

    y_values = [
        50,
        60,
        70,
        80,
        90
    ]

    correlation = calculate_correlation(
        x_values,
        y_values
    )

    for x, y in zip(
        x_values,
        y_values
    ):

        message.innerText = (
            f"Point: ({x}, {y})"
        )

        await asyncio.sleep(0.45)

    message.innerText = (
        f"Correlation = {correlation:.3f}"
    )


# ============================================================
# SIMPLE REGRESSION
# ============================================================

async def animate_regression():
    clear_area()

    area = get_area()

    if area is None:
        return

    panel = make_panel()

    panel.appendChild(
        make_title(
            "Simple regression"
        )
    )

    x_values = [
        1,
        2,
        3,
        4,
        5
    ]

    y_values = [
        2,
        4,
        6,
        8,
        10
    ]

    mean_x = (
        sum(x_values)
        / len(x_values)
    )

    mean_y = (
        sum(y_values)
        / len(y_values)
    )

    numerator = sum(
        (x - mean_x) * (y - mean_y)
        for x, y in zip(
            x_values,
            y_values
        )
    )

    denominator = sum(
        (x - mean_x) ** 2
        for x in x_values
    )

    slope = numerator / denominator

    intercept = (
        mean_y
        - slope * mean_x
    )

    message = make_message(
        "Finding the best-fitting line..."
    )

    panel.appendChild(message)

    area.appendChild(panel)

    for x, y in zip(
        x_values,
        y_values
    ):

        message.innerText = (
            f"Adding point ({x}, {y})"
        )

        await asyncio.sleep(0.4)

    message.innerText = (
        f"y = {slope:.2f}x + "
        f"{intercept:.2f}"
    )


# ============================================================
# ANIMATION CONTROLLER
# ============================================================

async def run_animation():
    title_element = document.getElementById(
        "lesson-title"
    )

    category_element = document.getElementById(
        "lesson-category"
    )

    if (
        not title_element
        or not category_element
    ):
        return

    title = title_element.innerText
    category = category_element.innerText

    # --------------------------------------------------------
    # PYTHON BASICS
    # --------------------------------------------------------

    if category == "PYTHON BASICS":

        if title == "Lists":
            await animate_list()

    # --------------------------------------------------------
    # NUMPY
    # --------------------------------------------------------

    elif category == "NUMPY":

        if title == "Mean, Min and Max":
            await animate_mean()

    # --------------------------------------------------------
    # PANDAS
    # --------------------------------------------------------

    elif category == "PANDAS":

        if title == "Describe":
            await animate_variance()

    # --------------------------------------------------------
    # STATISTICAL LEARNING
    # --------------------------------------------------------

    elif category == "STATISTICAL LEARNING":

        if title == "Mean":
            await animate_mean()

        elif title == "Variance":
            await animate_variance()

        elif title == "Correlation":
            await animate_correlation()

        elif title == "Simple Regression":
            await animate_regression()


# ============================================================
# JAVASCRIPT → PYTHON ANIMATION BRIDGE
# ============================================================

def python_animate(
    topic=None,
    lesson_title=None
):
    """
    JavaScript passes two values:

        topic
        lesson_title

    They are accepted here so the JavaScript
    bridge does not produce an argument error.
    """

    asyncio.ensure_future(
        run_animation()
    )


window.pythonAnimate = python_animate


# ============================================================
# INITIALIZATION
# ============================================================

async def initialize():
    """
    Initialize the existing textarea.

    We do NOT replace the textarea.
    """

    await asyncio.sleep(0.5)

    editor = get_code_editor()

    if editor is not None:

        editor.addEventListener(
            "keydown",
            handle_editor_keydown
        )


asyncio.ensure_future(
    initialize()
)