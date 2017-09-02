#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import pyautogui


def main():
    print 'asd'
    video_feed = cv2.VideoCapture(0)

    while True:
        _, screen = video_feed.read()
        cv2.imshow("feed", screen)

        #
        # Detection-logic ??
        #

        #break out of the loop (exit program)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the web-cam
    video_feed.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
