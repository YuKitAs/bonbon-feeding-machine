import time
import cv2


def capture_image(path):
    image = "{}bonbon-{}.png".format(path, time.strftime("%Y%m%d%H%M%S", time.localtime()))

    capture = cv2.VideoCapture(0)

    ret, frame = capture.read()

    if ret:
        cv2.imwrite(image, frame)

    capture.release()
    cv2.destroyAllWindows()

    return image


def capture_video(path, length):
    video = "{}bonbon-{}.avi".format(path, time.strftime("%Y%m%d%H%M%S", time.localtime()))

    capture = cv2.VideoCapture(0)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video, fourcc, 20.0, (640, 480))

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

    return video
