import time
import cv2
import os


def __get_current_time():
    return time.strftime("%Y%m%d%H%M%S", time.localtime())


def capture_image(path):
    image_path = os.path.join(path, "bonbon-{}.png".format(__get_current_time()))

    capture = cv2.VideoCapture(0)

    ret, frame = capture.read()

    if ret:
        cv2.imwrite(image_path, frame)

    capture.release()
    cv2.destroyAllWindows()

    return image_path


def capture_video(path, length):
    video_path = os.path.join(path, "bonbon-{}.avi".format(__get_current_time()))

    capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) <= length:
        ret, frame = capture.read()

        if ret:
            out.write(frame)
        else:
            break

    capture.release()
    out.release()
    cv2.destroyAllWindows()

    return video_path
