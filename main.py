import asyncio
import math

from pyscript import document, window
from pyodide.ffi import create_proxy


# ============================================================
# STATE
# ============================================================

algorithm = "linear"
category = "searching"

array = []

target = 42
speed = 300

running = False

comparisons = 0
current_index = None


# ============================================================
# DOM HELPER
# ============================================================

def el(selector):
    return document.querySelector(selector)


array_element = el("#array")

input_slider = el("#input-slider")
speed_slider = el("#speed-slider")

target_input = el("#target-input")
target_group = el("#target-group")
target_chip = el("#target-chip")

input_value = el("#input-value")
speed_value = el("#speed-value")

target_display = el("#target-display")

comparison_value = el("#comparison-value")
index_value = el("#index-value")
metric_input_value = el("#metric-input-value")
metric_complexity = el("#metric-complexity")

status_element = el("#status")

algorithm_title = el("#algorithm-title")
algorithm_small = el("#algorithm-name-small")
algorithm_description = el("#algorithm-description")
algorithm_type = el("#algorithm-type")

complexity = el("#complexity")

lesson_title = el("#lesson-title")
lesson_text = el("#lesson-text")

lesson_complexity_title = el(
    "#lesson-complexity-title"
)

lesson_complexity_text = el(
    "#lesson-complexity-text"
)

code_element = el("#code")

back_topic = el("#back-topic")


# ============================================================
# ALGORITHM DATA
# ============================================================

ALGORITHMS = {

    "linear": {
        "name": "Linear Search",
        "category": "searching",
        "complexity": "O(n)",
        "description":
            "Check each element one at a time until the target is found.",
        "code":
"""def linear_search(array, target):

    for i in range(len(array)):

        if array[i] == target:
            return i

    return -1
""",
        "lesson":
            "The algorithm examines elements sequentially. "
            "It stops as soon as it finds the target.",
        "complexity_text":
            "In the worst case, every element must be checked."
    },

    "binary": {
        "name": "Binary Search",
        "category": "searching",
        "complexity": "O(log n)",
        "description":
            "Repeatedly divide a sorted search space in half.",
        "code":
"""def binary_search(array, target):

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
""",
        "lesson":
            "Binary search checks the middle and eliminates "
            "half of the remaining search space.",
        "complexity_text":
            "Each comparison removes roughly half of the remaining inputs."
    },

    "jump": {
        "name": "Jump Search",
        "category": "searching",
        "complexity": "O(√n)",
        "description":
            "Jump through sorted blocks before performing a linear search.",
        "code":
"""def jump_search(array, target):

    n = len(array)
    step = int(n ** 0.5)

    previous = 0

    while (
        previous < n
        and array[min(step, n) - 1] < target
    ):

        previous = step
        step += int(n ** 0.5)

        if previous >= n:
            return -1

    while (
        previous < min(step, n)
        and array[previous] < target
    ):

        previous += 1

    if (
        previous < n
        and array[previous] == target
    ):

        return previous

    return -1
""",
        "lesson":
            "Jump search skips through blocks and then searches "
            "the candidate block linearly.",
        "complexity_text":
            "The jump size balances block jumps against linear checking."
    },

    "interpolation": {
        "name": "Interpolation Search",
        "category": "searching",
        "complexity": "O(log log n)",
        "description":
            "Estimate where a target should be based on its value.",
        "code":
"""def interpolation_search(array, target):

    low = 0
    high = len(array) - 1

    while (
        low <= high
        and array[low] <= target <= array[high]
    ):

        position = low + (
            (target - array[low])
            * (high - low)
            // (array[high] - array[low])
        )

        if array[position] == target:
            return position

        if array[position] < target:
            low = position + 1

        else:
            high = position - 1

    return -1
""",
        "lesson":
            "Interpolation search estimates the likely position "
            "instead of always checking the middle.",
        "complexity_text":
            "With uniformly distributed values, the search can shrink extremely quickly."
    },

    "bubble": {
        "name": "Bubble Sort",
        "category": "sorting",
        "complexity": "O(n²)",
        "description":
            "Repeatedly compare neighboring elements and swap them when necessary.",
        "code":
"""def bubble_sort(array):

    n = len(array)

    for i in range(n):

        for j in range(0, n - i - 1):

            if array[j] > array[j + 1]:

                array[j], array[j + 1] = (
                    array[j + 1],
                    array[j]
                )
""",
        "lesson":
            "Bubble sort repeatedly compares neighboring boxes. "
            "Larger values gradually move toward the right.",
        "complexity_text":
            "Nested comparisons can require roughly n² operations."
    },

    "selection": {
        "name": "Selection Sort",
        "category": "sorting",
        "complexity": "O(n²)",
        "description":
            "Repeatedly select the smallest remaining element and place it in position.",
        "code":
"""def selection_sort(array):

    n = len(array)

    for i in range(n):

        minimum = i

        for j in range(i + 1, n):

            if array[j] < array[minimum]:
                minimum = j

        array[i], array[minimum] = (
            array[minimum],
            array[i]
        )
""",
        "lesson":
            "Selection sort searches for the smallest remaining "
            "box and moves it into its final position.",
        "complexity_text":
            "Finding the minimum repeatedly requires quadratic comparisons."
    },

    "insertion": {
        "name": "Insertion Sort",
        "category": "sorting",
        "complexity": "O(n²)",
        "description":
            "Build the sorted section one element at a time.",
        "code":
"""def insertion_sort(array):

    for i in range(1, len(array)):

        key = array[i]
        j = i - 1

        while (
            j >= 0
            and array[j] > key
        ):

            array[j + 1] = array[j]
            j -= 1

        array[j + 1] = key
""",
        "lesson":
            "Insertion sort takes the next box and physically "
            "moves it into the correct position.",
        "complexity_text":
            "In the worst case, each new element may move across the sorted section."
    },

    "merge": {
        "name": "Merge Sort",
        "category": "sorting",
        "complexity": "O(n log n)",
        "description":
            "Divide the array, sort the pieces, and merge them together.",
        "code":
"""def merge_sort(array):

    if len(array) <= 1:
        return array

    mid = len(array) // 2

    left = merge_sort(array[:mid])
    right = merge_sort(array[mid:])

    return merge(left, right)
""",
        "lesson":
            "Merge sort divides the array into smaller sections "
            "and then combines sorted sections.",
        "complexity_text":
            "There are logarithmic levels of division with linear work per level."
    },

    "quick": {
        "name": "Quick Sort",
        "category": "sorting",
        "complexity": "O(n log n)",
        "description":
            "Partition data around a pivot and recursively sort each side.",
        "code":
"""def quick_sort(array):

    if len(array) <= 1:
        return array

    pivot = array[-1]

    left = [
        x for x in array[:-1]
        if x <= pivot
    ]

    right = [
        x for x in array[:-1]
        if x > pivot
    ]

    return (
        quick_sort(left)
        + [pivot]
        + quick_sort(right)
    )
""",
        "lesson":
            "Quick sort chooses a pivot and moves values around "
            "that pivot.",
        "complexity_text":
            "Good pivots produce logarithmic levels of partitioning."
    },

    "heap": {
        "name": "Heap Sort",
        "category": "sorting",
        "complexity": "O(n log n)",
        "description":
            "Use a heap structure to repeatedly extract the next element.",
        "code":
"""def heap_sort(array):

    build_max_heap(array)

    for end in range(
        len(array) - 1,
        0,
        -1
    ):

        array[0], array[end] = (
            array[end],
            array[0]
        )

        sift_down(
            array,
            0,
            end
        )
""",
        "lesson":
            "Heap sort repeatedly extracts the next element "
            "from a heap.",
        "complexity_text":
            "Heap operations take logarithmic time and occur across the array."
    }
}


# ============================================================
# URL PARAMETERS
# ============================================================

def read_url_parameters():

    global algorithm
    global category

    search = window.location.search

    if search.startswith("?"):
        search = search[1:]

    parameters = {}

    for item in search.split("&"):

        if "=" not in item:
            continue

        key, value = item.split("=", 1)

        parameters[key] = value

    requested = parameters.get(
        "algorithm",
        "linear"
    )

    if requested in ALGORITHMS:
        algorithm = requested

    category = ALGORITHMS[
        algorithm
    ]["category"]


# ============================================================
# ARRAY CREATION
# ============================================================

def create_array():

    global array

    size = int(
        input_slider.value
    )

    if category == "searching":

        array = [
            (i + 1) * 5
            for i in range(size)
        ]

        if target not in array:
            array[-1] = target

        array.sort()

    else:

        # Deliberately unsorted.
        # This makes the physical movement
        # easy to understand.

        base = [
            4,
            5,
            1,
            8,
            3,
            7,
            2,
            9,
            6,
            10,
            12,
            11,
            15,
            13,
            14,
            18,
            16,
            20,
            17,
            19,
            24,
            21,
            23,
            22,
            27,
            25,
            30,
            26,
            29,
            28,
            35,
            31,
            34,
            32,
            33,
            40,
            37,
            39,
            36,
            38
        ]

        array = base[:size]


# ============================================================
# ARRAY DOM
# ============================================================

def display_array():

    array_element.innerHTML = ""

    for index, value in enumerate(array):

        box = document.createElement("div")

        box.className = "array-box"

        box.innerText = str(value)

        box.setAttribute(
            "data-index",
            str(index)
        )

        array_element.appendChild(box)


def boxes():

    return document.querySelectorAll(
        ".array-box"
    )


def clear_states():

    for box in boxes():

        box.classList.remove(
            "active",
            "found",
            "eliminated",
            "inserting",
            "comparing",
            "insertion-position"
        )


# ============================================================
# STATUS
# ============================================================

def status(message, state=""):

    status_element.className = (
        "visualizer-status "
        + state
    )

    status_element.innerText = message


# ============================================================
# METRICS
# ============================================================

def update_metrics():

    comparison_value.innerText = str(
        comparisons
    )

    if current_index is None:

        index_value.innerText = "—"

    else:

        index_value.innerText = str(
            current_index
        )

    metric_input_value.innerText = str(
        len(array)
    )


# ============================================================
# ALGORITHM UI
# ============================================================

def update_algorithm_ui():

    data = ALGORITHMS[algorithm]

    algorithm_title.innerText = (
        data["name"]
    )

    algorithm_small.innerText = (
        data["name"]
    )

    algorithm_description.innerText = (
        data["description"]
    )

    complexity.innerText = (
        data["complexity"]
    )

    metric_complexity.innerText = (
        data["complexity"]
    )

    algorithm_type.innerText = (
        "SEARCHING ALGORITHM"
        if data["category"] == "searching"
        else "SORTING ALGORITHM"
    )

    lesson_title.innerText = (
        data["name"]
    )

    lesson_text.innerText = (
        data["lesson"]
    )

    lesson_complexity_title.innerText = (
        f"Why {data['complexity']}?"
    )

    lesson_complexity_text.innerText = (
        data["complexity_text"]
    )

    code_element.innerText = (
        data["code"]
    )

    if data["category"] == "searching":

        back_topic.href = "searching.html"

        el("#category-name").innerText = (
            "Searching"
        )

        target_group.style.display = "block"

        target_chip.style.display = "block"

    else:

        back_topic.href = "sorting.html"

        el("#category-name").innerText = (
            "Sorting"
        )

        target_group.style.display = "none"

        target_chip.style.display = "none"


# ============================================================
# RANGE SLIDER
# ============================================================

def update_slider(slider):

    minimum = float(
        slider.min
    )

    maximum = float(
        slider.max
    )

    value = float(
        slider.value
    )

    percentage = (
        (value - minimum)
        /
        (maximum - minimum)
        * 100
    )

    slider.style.setProperty(
        "--progress",
        f"{percentage}%"
    )


def input_changed(event=None):

    if running:
        return

    create_array()

    input_value.innerText = (
        input_slider.value
    )

    display_array()

    update_metrics()

    draw_graph()

    status(
        "Input size changed. Ready to visualize."
    )

    update_slider(
        input_slider
    )


def speed_changed(event=None):

    global speed

    speed = int(
        speed_slider.value
    )

    speed_value.innerText = (
        f"{speed} ms"
    )

    update_slider(
        speed_slider
    )


def target_changed(event=None):

    global target

    if running:
        return

    try:
        target = int(
            target_input.value
        )

    except ValueError:

        target = 42

    target_input.value = str(
        target
    )

    target_display.innerText = str(
        target
    )

    create_array()

    display_array()

    status(
        f"Target updated to {target}."
    )


# ============================================================
# SEARCHING
# ============================================================

async def linear_search():

    global comparisons
    global current_index

    items = boxes()

    for i in range(
        len(array)
    ):

        if not running:
            return

        comparisons += 1
        current_index = i

        clear_states()

        items[i].classList.add(
            "active"
        )

        update_metrics()

        status(
            f"Checking index {i} → {array[i]}",
            "running"
        )

        await asyncio.sleep(
            speed / 1000
        )

        if array[i] == target:

            items[i].classList.remove(
                "active"
            )

            items[i].classList.add(
                "found"
            )

            status(
                f"Found {target} at index {i}.",
                "success"
            )

            return

        items[i].classList.remove(
            "active"
        )

        items[i].classList.add(
            "eliminated"
        )

    status(
        f"{target} was not found.",
        "error"
    )


async def binary_search():

    global comparisons
    global current_index

    items = boxes()

    left = 0
    right = len(array) - 1

    while left <= right:

        if not running:
            return

        mid = (
            left + right
        ) // 2

        comparisons += 1

        current_index = mid

        clear_states()

        for i in range(
            len(array)
        ):

            if (
                i < left
                or i > right
            ):

                items[i].classList.add(
                    "eliminated"
                )

        items[mid].classList.add(
            "active"
        )

        update_metrics()

        status(
            f"Checking middle index {mid} → {array[mid]}",
            "running"
        )

        await asyncio.sleep(
            speed / 1000
        )

        if array[mid] == target:

            items[mid].classList.remove(
                "active"
            )

            items[mid].classList.add(
                "found"
            )

            status(
                f"Found {target} at index {mid}.",
                "success"
            )

            return

        if array[mid] < target:

            for i in range(
                left,
                mid + 1
            ):

                items[i].classList.add(
                    "eliminated"
                )

            left = mid + 1

        else:

            for i in range(
                mid,
                right + 1
            ):

                items[i].classList.add(
                    "eliminated"
                )

            right = mid - 1

    status(
        f"{target} was not found.",
        "error"
    )


# ============================================================
# PHYSICAL BOX MOVEMENT
# ============================================================

async def animate_insertion(
    source_index,
    destination_index
):

    items = boxes()

    if source_index == destination_index:
        return

    moving_box = items[
        source_index
    ]

    moving_box.classList.add(
        "inserting"
    )

    status(
        f"Moving {array[source_index]} "
        f"in front of {array[destination_index]}.",
        "sorting-message"
    )

    await asyncio.sleep(
        speed / 1000
    )

    distance = (
        destination_index
        - source_index
    )

    box_width = 58

    moving_box.style.transform = (
        f"translateX({distance * box_width}px) "
        f"translateY(-25px)"
    )

    await asyncio.sleep(
        speed / 1000
    )

    moving_box.style.transform = (
        f"translateX({distance * box_width}px) "
        f"translateY(0)"
    )

    await asyncio.sleep(
        speed / 1000
    )

    # Actual array order changes only AFTER
    # the physical movement has completed.

    value = array.pop(
        source_index
    )

    array.insert(
        destination_index,
        value
    )

    display_array()

    await asyncio.sleep(
        80 / 1000
    )


# ============================================================
# INSERTION SORT
# ============================================================

async def insertion_sort():

    global comparisons
    global current_index

    for i in range(
        1,
        len(array)
    ):

        if not running:
            return

        current_index = i

        items = boxes()

        clear_states()

        items[i].classList.add(
            "inserting"
        )

        status(
            f"Take {array[i]} and find "
            f"where it belongs.",
            "sorting-message"
        )

        await asyncio.sleep(
            speed / 1000
        )

        j = i

        while j > 0:

            if not running:
                return

            comparisons += 1

            update_metrics()

            items = boxes()

            clear_states()

            items[j].classList.add(
                "inserting"
            )

            items[j - 1].classList.add(
                "comparing"
            )

            current_value = array[j]
            previous_value = array[j - 1]

            status(
                f"Is {current_value} smaller than "
                f"{previous_value}?",
                "sorting-message"
            )

            await asyncio.sleep(
                speed / 1000
            )

            if current_value >= previous_value:

                status(
                    f"{current_value} belongs after "
                    f"{previous_value}.",
                    "sorting-message"
                )

                await asyncio.sleep(
                    speed / 1000
                )

                break

            destination = j - 1

            items[destination].classList.add(
                "insertion-position"
            )

            status(
                f"{current_value} moves in front "
                f"of {previous_value}.",
                "sorting-message"
            )

            await asyncio.sleep(
                120 / 1000
            )

            await animate_insertion(
                j,
                destination
            )

            j -= 1

            current_index = j

            update_metrics()

            await asyncio.sleep(
                speed / 1000
            )

        clear_states()

    status(
        "Insertion Sort complete — all boxes are sorted.",
        "success"
    )


# ============================================================
# BUBBLE SORT
# ============================================================

async def bubble_sort():

    global comparisons
    global current_index

    n = len(array)

    for end in range(
        n - 1,
        0,
        -1
    ):

        swapped = False

        for j in range(end):

            if not running:
                return

            comparisons += 1
            current_index = j

            items = boxes()

            clear_states()

            items[j].classList.add(
                "comparing"
            )

            items[j + 1].classList.add(
                "comparing"
            )

            update_metrics()

            status(
                f"Compare {array[j]} and "
                f"{array[j + 1]}.",
                "sorting-message"
            )

            await asyncio.sleep(
                speed / 1000
            )

            if array[j] > array[j + 1]:

                status(
                    f"{array[j]} is larger — "
                    f"swap the boxes.",
                    "sorting-message"
                )

                await asyncio.sleep(
                    speed / 1000
                )

                await animate_insertion(
                    j + 1,
                    j
                )

                swapped = True

            else:

                await asyncio.sleep(
                    100 / 1000
                )

        if not swapped:
            break

    clear_states()

    status(
        "Bubble Sort complete.",
        "success"
    )


# ============================================================
# SELECTION SORT
# ============================================================

async def selection_sort():

    global comparisons
    global current_index

    n = len(array)

    for i in range(n):

        minimum = i

        for j in range(
            i + 1,
            n
        ):

            if not running:
                return

            comparisons += 1
            current_index = j

            items = boxes()

            clear_states()

            items[minimum].classList.add(
                "inserting"
            )

            items[j].classList.add(
                "comparing"
            )

            update_metrics()

            status(
                f"Compare {array[j]} with "
                f"current minimum {array[minimum]}.",
                "sorting-message"
            )

            await asyncio.sleep(
                speed / 1000
            )

            if array[j] < array[minimum]:

                minimum = j

        if minimum != i:

            status(
                f"Move minimum {array[minimum]} "
                f"into position {i}.",
                "sorting-message"
            )

            await asyncio.sleep(
                speed / 1000
            )

            value = array.pop(
                minimum
            )

            array.insert(
                i,
                value
            )

            display_array()

            await asyncio.sleep(
                speed / 1000
            )

    clear_states()

    status(
        "Selection Sort complete.",
        "success"
    )


# ============================================================
# GENERIC SORTING VISUALIZATION
# ============================================================

async def simple_sort_visual():

    global comparisons
    global current_index

    # Used as a visual fallback for Merge,
    # Quick and Heap until their dedicated
    # teaching animations are added.

    for i in range(
        len(array)
    ):

        for j in range(
            i + 1,
            len(array)
        ):

            if not running:
                return

            comparisons += 1

            current_index = j

            items = boxes()

            clear_states()

            items[i].classList.add(
                "comparing"
            )

            items[j].classList.add(
                "comparing"
            )

            update_metrics()

            status(
                f"Comparing {array[i]} "
                f"and {array[j]}.",
                "sorting-message"
            )

            await asyncio.sleep(
                speed / 1000
            )

            if array[j] < array[i]:

                await animate_insertion(
                    j,
                    i
                )

            await asyncio.sleep(
                100 / 1000
            )

    clear_states()

    status(
        "Sorting complete.",
        "success"
    )


# ============================================================
# START
# ============================================================

async def run():

    global running
    global comparisons
    global current_index

    if running:
        return

    running = True

    comparisons = 0
    current_index = None

    start = el(
        "#start-button"
    )

    start.disabled = True

    create_array()

    display_array()

    update_metrics()

    try:

        if algorithm == "linear":

            await linear_search()

        elif algorithm == "binary":

            await binary_search()

        elif algorithm == "insertion":

            await insertion_sort()

        elif algorithm == "bubble":

            await bubble_sort()

        elif algorithm == "selection":

            await selection_sort()

        elif algorithm in (
            "merge",
            "quick",
            "heap"
        ):

            await simple_sort_visual()

    finally:

        running = False

        start.disabled = False


# ============================================================
# RESET
# ============================================================

def reset(event=None):

    global running
    global comparisons
    global current_index

    running = False

    comparisons = 0
    current_index = None

    create_array()

    display_array()

    update_metrics()

    draw_graph()

    status(
        "Ready to visualize."
    )

    el(
        "#start-button"
    ).disabled = False


# ============================================================
# GRAPH
# ============================================================

def svg(tag):

    return document.createElementNS(
        "http://www.w3.org/2000/svg",
        tag
    )


def path_from_points(points):

    if not points:
        return ""

    result = (
        f"M {points[0][0]} "
        f"{points[0][1]}"
    )

    for x, y in points[1:]:

        result += (
            f" L {x} {y}"
        )

    return result


def draw_graph():

    grid = el("#graph-grid")
    labels = el("#graph-labels")

    linear_path = el("#linear-path")
    log_path = el("#log-path")

    marker = el("#graph-marker")

    linear_point = el("#linear-point")
    log_point = el("#log-point")

    grid.innerHTML = ""
    labels.innerHTML = ""

    width = 900
    height = 350

    left = 55
    right = 20
    top = 20
    bottom = 40

    plot_width = (
        width - left - right
    )

    plot_height = (
        height - top - bottom
    )

    max_n = 40

    for y_value in [
        0,
        25,
        50,
        75,
        100
    ]:

        y = (
            top
            + plot_height
            - (y_value / 100)
            * plot_height
        )

        line = svg("line")

        line.setAttribute(
            "x1",
            str(left)
        )

        line.setAttribute(
            "x2",
            str(width - right)
        )

        line.setAttribute(
            "y1",
            str(y)
        )

        line.setAttribute(
            "y2",
            str(y)
        )

        line.setAttribute(
            "class",
            "graph-grid-line"
        )

        grid.appendChild(line)


    linear_points = []

    log_points = []

    max_log = math.log2(
        max_n
    )

    for n in range(
        1,
        max_n + 1
    ):

        x = (
            left
            + (n / max_n)
            * plot_width
        )

        linear_y = (
            top
            + plot_height
            - (n / max_n)
            * plot_height
        )

        log_normalized = (
            math.log2(n)
            / max_log
        )

        log_y = (
            top
            + plot_height
            - log_normalized
            * plot_height
        )

        linear_points.append(
            (x, linear_y)
        )

        log_points.append(
            (x, log_y)
        )


    linear_path.setAttribute(
        "d",
        path_from_points(
            linear_points
        )
    )

    log_path.setAttribute(
        "d",
        path_from_points(
            log_points
        )
    )


    n = min(
        len(array),
        max_n
    )

    x = (
        left
        + (n / max_n)
        * plot_width
    )

    linear_y = (
        top
        + plot_height
        - (n / max_n)
        * plot_height
    )

    log_y = (
        top
        + plot_height
        -
        (
            math.log2(
                max(n, 1)
            )
            / max_log
        )
        * plot_height
    )

    marker.setAttribute(
        "x1",
        str(x)
    )

    marker.setAttribute(
        "x2",
        str(x)
    )

    marker.setAttribute(
        "y1",
        str(top)
    )

    marker.setAttribute(
        "y2",
        str(top + plot_height)
    )

    linear_point.setAttribute(
        "cx",
        str(x)
    )

    linear_point.setAttribute(
        "cy",
        str(linear_y)
    )

    log_point.setAttribute(
        "cx",
        str(x)
    )

    log_point.setAttribute(
        "cy",
        str(log_y)
    )


# ============================================================
# EVENTS
# ============================================================

def start_event(event=None):

    asyncio.ensure_future(
        run()
    )


input_proxy = create_proxy(
    input_changed
)

speed_proxy = create_proxy(
    speed_changed
)

target_proxy = create_proxy(
    target_changed
)

start_proxy = create_proxy(
    start_event
)

reset_proxy = create_proxy(
    reset
)


input_slider.addEventListener(
    "input",
    input_proxy
)

speed_slider.addEventListener(
    "input",
    speed_proxy
)

target_input.addEventListener(
    "change",
    target_proxy
)

el(
    "#start-button"
).addEventListener(
    "click",
    start_proxy
)

el(
    "#reset-button"
).addEventListener(
    "click",
    reset_proxy
)


# ============================================================
# INITIALIZATION
# ============================================================

def initialize():

    global speed
    global target

    read_url_parameters()

    speed = int(
        speed_slider.value
    )

    target = int(
        target_input.value
    )

    update_algorithm_ui()

    create_array()

    display_array()

    input_value.innerText = (
        input_slider.value
    )

    speed_value.innerText = (
        f"{speed} ms"
    )

    target_display.innerText = (
        str(target)
    )

    update_slider(
        input_slider
    )

    update_slider(
        speed_slider
    )

    update_metrics()

    draw_graph()

    status(
        "Ready to visualize."
    )


initialize()