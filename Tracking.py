#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2


def main():
    # Define an initial bounding box
    bbox = (150, 130, 60, 100)

    video_feed = cv2.VideoCapture(0)

    tracker = calibrate_webcam(video_feed, bbox)
    while True:
        # Read a new frame
        ok, frame = video_feed.read()
        if not ok:
            break
        # Update tracker
        ok, bbox = tracker.update(frame)

        # Draw bounding box
        if ok:
            draw_rect_from_points(frame, bbox)

        # Display result
        cv2.imshow("Tracking", frame)

        # break out of the loop (exit program)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the web-cam
    video_feed.release()
    cv2.destroyAllWindows()


def calibrate_webcam(video_feed, bbox):
    tracker = cv2.TrackerMIL_create()
    calibrated = False
    while True:
        _, new_frame = video_feed.read()
        new_frame = draw_rect_from_points(new_frame, bbox)
        cv2.putText(new_frame, "Put finger in red rectangle", (80, 80), cv2.FONT_ITALIC, 1, (255, 255, 255), 3)
        cv2.imshow("Webcam", new_frame)
        # break out of the loop (exit program)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or calibrated:
            break
    tracker.init(new_frame, bbox)
    return tracker


def draw_rect_from_points(frame, bbox):
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    cv2.rectangle(frame, p1, p2, (0, 0, 255), 2)
    return frame


if __name__ == "__main__":
    main()
