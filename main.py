import math
from pyscript import window


canvas = window.document.getElementById("canvas")
ctx = canvas.getContext("2d")


t = 0


def animate(timestamp):

    global t

    # Clear the canvas
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

    # Move animation forward
    t += 0.03

    # Request next frame
    window.requestAnimationFrame(animate)


window.requestAnimationFrame(animate)
