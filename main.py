import tkinter as tk
from random import randint

radius = 10  # Zmienna globalna dla promienia okręgów
selected_circle = None  # Zmienna globalna dla zaznaczonego okręgu
start_position = {}  # Zmienna globalna dla początkowej pozycji zaznaczonego okręgu
windowWidth = 800
windowHeight = 800
numOfCircles = 2

maxCircles = windowHeight // (radius * 2) * windowWidth // (radius * 2)
print(maxCircles)


def generate_circles(num_circles, radius):
    """
    Funkcja do generowania losowych okręgów i dodawania ich do listy.

    :param num_circles: Liczba okręgów do wygenerowania.
    :param radius: Promień okręgów.
    :return: Lista informacji o wygenerowanych okręgach.
    """
    circles = []
    for _ in range(num_circles):
        x = randint(radius, windowWidth - radius)
        y = randint(radius, windowHeight - radius)
        circle_id = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#222222", outline="white",
                                       width=2)
        circles.append([circle_id, x, y, radius])
    return circles


def move_circle(circle_id, dx, dy):
    """
    Funkcja do przesunięcia danego okręgu o określone przesunięcie w poziomie i pionie.

    :param circle_id: ID okręgu do przesunięcia.
    :param dx: Przesunięcie w poziomie.
    :param dy: Przesunięcie w pionie.
    :return: Stare i nowe współrzędne okręgu.
    """
    circle = [info for info in listOfCircles if info[0] == circle_id][0]
    old_coordinates = (circle[1], circle[2])
    circle[1] += dx
    circle[2] += dy

    # Ograniczenie, aby okręgi nie wyjeżdżały poza okno
    circle[1] = max(radius, min(windowWidth - radius, circle[1]))
    circle[2] = max(radius, min(windowHeight - radius, circle[2]))

    canvas.coords(circle_id, circle[1] - radius, circle[2] - radius, circle[1] + radius, circle[2] + radius)
    new_coordinates = (circle[1], circle[2])
    return old_coordinates, new_coordinates


def select_circle(event):
    """
    Funkcja do zaznaczania okręgu po kliknięciu myszą.

    :param event: Zdarzenie myszy.
    """
    global selected_circle, start_position

    for circle in listOfCircles:
        x1, y1, x2, y2 = canvas.coords(circle[0])
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            if selected_circle:
                canvas.itemconfig(selected_circle, outline="white")
            selected_circle = circle[0]
            start_position[selected_circle] = (event.x, event.y)
            canvas.itemconfig(selected_circle, outline="lime")
            break


def move_selected_circle(event):
    """
    Funkcja do przesuwania zaznaczonego okręgu po kliknięciu myszą.

    :param event: Zdarzenie myszy.
    """
    global selected_circle, start_position
    if selected_circle:
        if start_position.get(selected_circle) is not None:
            circle = [info for info in listOfCircles if info[0] == selected_circle][0]
            dx = event.x - start_position[selected_circle][0]
            dy = event.y - start_position[selected_circle][1]
            old_position, new_position = move_circle(selected_circle, dx, dy)
            start_position[selected_circle] = (event.x, event.y)


def release_mouse(event):
    """
    Funkcja do odznaczania zaznaczonego okręgu po puszczeniu myszy.

    :param event: Zdarzenie myszy.
    """
    global selected_circle
    if selected_circle:
        canvas.itemconfig(selected_circle, outline="white")
        selected_circle = None


def check_collision(circle1, circle2):
    """
    Funkcja do sprawdzania kolizji między okręgami.

    :param circle1: Informacje o pierwszym okręgu.
    :param circle2: Informacje o drugim okręgu.
    :return: True, jeśli występuje kolizja; False w przeciwnym razie.
    """
    x1, y1 = circle1[1], circle1[2]
    x2, y2 = circle2[1], circle2[2]
    r1 = circle1[3]
    r2 = circle2[3]
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return distance < r1 + r2


def check_collisions():
    """
    Funkcja do sprawdzania kolizji między wszystkimi okręgami.
    """
    found_collision = False
    for i, circle1 in enumerate(listOfCircles):
        for circle2 in listOfCircles[i + 1:]:
            collision = check_collision(circle1, circle2)
            if collision:
                print(f"Collision between Circle {circle1[0]} and Circle {circle2[0]}")
                found_collision = True

    if not found_collision:
        print("No collisions found.")


def resolve_collisions():
    """
    Funkcja do rozwiązania kolizji między okręgami.
    """
    max_iterations = 1000
    iteration = 0

    while iteration < max_iterations:
        collisions = []
        for i, circle1 in enumerate(listOfCircles):
            for j, circle2 in enumerate(listOfCircles[i + 1:]):
                j += i + 1
                if check_collision(circle1, circle2):
                    collisions.append((circle1, circle2))

        if not collisions:
            break

        for circle1, circle2 in collisions:
            displacement_vector1 = (circle1[1] - circle2[1], circle1[2] - circle2[2])
            displacement_vector2 = (circle2[1] - circle1[1], circle2[2] - circle1[2])

            move_circle(circle1[0], displacement_vector1[0] / 2, displacement_vector1[1] / 2)
            move_circle(circle2[0], displacement_vector2[0] / 2, displacement_vector2[1] / 2)

        iteration += 1


def display_circle_coordinates():
    """
    Funkcja do wyświetlania danych o obecnych koordynatach okręgów.
    """
    for circle in listOfCircles:
        print(f"Circle ID: {circle[0]}, Coordinates: ({circle[1]}, {circle[2]})")


root = tk.Tk()
root.title("Collision Resolution")

button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

canvas = tk.Canvas(root, width=windowWidth, height=windowHeight, bg="#222222", highlightthickness=0)
canvas.pack()

listOfCircles = generate_circles(numOfCircles, radius)

canvas.bind("<Button-1>", select_circle)
canvas.bind("<B1-Motion>", move_selected_circle)
canvas.bind("<ButtonRelease-1>", release_mouse)

collision_button = tk.Button(button_frame, text="Check Collisions", command=check_collisions)
collision_button.grid(row=0, column=0, padx=10, pady=10)

resolve_collision_button = tk.Button(button_frame, text="Resolve Collisions", command=resolve_collisions)
resolve_collision_button.grid(row=0, column=1, padx=10, pady=10)

display_coordinates_button = tk.Button(button_frame, text="Display Coordinates", command=display_circle_coordinates)
display_coordinates_button.grid(row=0, column=2, padx=10, pady=10)

for circle in listOfCircles:
    print(f"Circle ID: {circle[0]}, Coordinates: ({circle[1]}, {circle[2]})")

root.mainloop()
