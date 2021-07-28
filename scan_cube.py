import cv2
import color_detector

cam = cv2.VideoCapture(0)

detector_stickers = [[200, 120], [300, 120], [400, 120],
                     [200, 220], [300, 220], [400, 220],
                     [200, 320], [300, 320], [400, 320]]

current_stickers = [[20, 20], [54, 20], [88, 20],
                    [20, 54], [54, 54], [88, 54],
                    [20, 88], [54, 88], [88, 88]]

recorded_stickers = [[20, 130], [54, 130], [88, 130],
                     [20, 164], [54, 164], [88, 164],
                     [20, 198], [54, 198], [88, 198]]


def draw_detector_stickers(frame):
    for index, (x, y) in enumerate(detector_stickers):
        cv2.rectangle(frame, (x, y), (x + 32, y + 32), (255, 255, 255), -1)


def draw_current_stickers(frame, state):
    for index, (x, y) in enumerate(current_stickers):
        cv2.rectangle(frame, (x, y), (x + 32, y + 32), color_detector.name_to_rgb(state[index]), -1)


def draw_recorded_stickers(frame, state):
    for index, (x, y) in enumerate(recorded_stickers):
        cv2.rectangle(frame, (x, y), (x + 32, y + 32), color_detector.name_to_rgb(state[index]), -1)


def color_to_notation(color):
    """
    Helper function for converting colors to notation
    used by solver.
    """
    notation = {
        'green': 'F',
        'white': 'U',
        'blue': 'B',
        'red': 'R',
        'orange': 'L',
        'yellow': 'D'
    }
    return notation[color]


def empty_callback(_):
    """
    Empty function for callback when slider positions change. Need input x (_), this is the value
    the slider has changed to. You don't need to do anything in this function.
    """
    pass


def scan():
    """
    Open up the webcam and scans the 9 regions in the center
    and show a preview.

    After hitting the space bar to confirm, the block below the
    current stickers shows the current state that you have.
    This is show every user can see what the computer took as input.

    :returns: dictionary
    """

    sides = {}  # collection of scanned sides
    preview = ['white', 'white', 'white',  # default starting preview sticker colors
               'white', 'white', 'white',
               'white', 'white', 'white']
    state = [0, 0, 0,  # current sticker colors
             0, 0, 0,
             0, 0, 0]

    default_cal = {  # default color calibration
        'white': [[179, 30, 255], [0, 0, 0]],
        'green': [[102, 255, 184], [52, 85, 39]],
        'red': [[172, 255, 147], [13, 165, 86]],
        'orange': [[172, 255, 255], [7, 136, 148]],
        'yellow': [[179, 255, 255], [27, 210, 140]],
        'blue': [[120, 255, 255], [100, 141, 90]]
    }
    color_cal = default_cal

    space_bar_pressed = False
    color_index = 0
    color = ['white', 'green', 'red', 'orange', 'blue', 'yellow']
    top = ['blue', 'white', 'white', 'white', 'white', 'green']

    cv2.namedWindow('default')
    cv2.resizeWindow('default', 800, 600)

    while True:
        _, frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        key = cv2.waitKey(10)

        # init certain stickers.
        draw_detector_stickers(frame)
        draw_recorded_stickers(frame, preview)

        if key == ord('r'):
            if color_index >= 1:
                color_index -= 1

        current_face = color[color_index]

        for index, (x, y) in enumerate(detector_stickers):
            roi = hsv[y:y + 32, x:x + 32]  # extracts hsv values within sticker
            avg_hsv = color_detector.median_hsv(roi)  # filters the hsv values into one hsv
            color_name = color_detector.get_color_name(avg_hsv, color_cal)  # extracts the color based on hsv
            state[index] = color_name  # stores the color

            # update when space bar is pressed.
            if key == 32:
                preview = list(state)
                if current_face == state[4]:
                    space_bar_pressed = True
                    # convert the color to notation of the middle sticker and label this as the face
                    face = color_to_notation(state[4])
                    draw_recorded_stickers(frame, state)  # draw the saved colors on the preview
                    notation = [color_to_notation(color) for color in state]  # convert all colors to notation
                    sides[face] = notation  # update the face in the sides dictionary

        # show the new stickers
        draw_current_stickers(frame, state)  # draw live sampling of face colors

        if space_bar_pressed:
            space_bar_pressed = False
            color_index += 1
            print(sides)

        if color_index == len(color):
            color_index = 0

        # append amount of scanned sides
        text = 'scanned sides: {}/6'.format(len(sides))
        cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        text = 'Press space to record / \'r\' to re-scan'
        cv2.putText(frame, text, (250, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        text = 'Show face with {} center and top {}'.format(current_face.upper(), top[color_index].upper())
        cv2.putText(frame, text, (200, 70), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 0), 1, cv2.LINE_AA)

        if len(sides) == 6:
            break

        # quit on escape.
        if key == 27:
            break

        # show result
        cv2.imshow("default", frame)

    cam.release()
    cv2.destroyAllWindows()
    return sides if len(sides) == 6 else {}
