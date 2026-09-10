import math

from pyscript import window
from pyodide.ffi import create_proxy


# Get canvas
canvas = window.document.getElementById("canvas")
ctx = canvas.getContext("2d")

# Animation variable
t = 0


def animate(timestamp):
    global t

    # Clear canvas
    ctx.clearRect(0, 0, 800, 400)

    # Calculate position
    x = 400 + 200 * math.cos(t)
    y = 200 + 100 * math.sin(t)

    # Draw circle
    ctx.beginPath()
    ctx.arc(
        x,
        y,
        20,
        0,
        2 * math.pi
    )

    ctx.fillStyle = "red"
    ctx.fill()

    # Move animation
    t += 0.03

    # Schedule next frame
    window.requestAnimationFrame(animation_proxy)


# Create a persistent JavaScript callback
animation_proxy = create_proxy(animate)

# Start animation
window.requestAnimationFrame(animation_proxy)