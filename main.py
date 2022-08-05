from os import stat_result
import random
from sre_constants import SUCCESS
import cv2
from cv2 import FONT_HERSHEY_PLAIN
from cv2 import IMREAD_UNCHANGED
import cvzone
import timer
import time

# adding library for hand detector
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)  # Adding image from the webcam
cap.set(3, 640)  # set window size
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
score = [0, 0]  # AI, Player

while True:
    imgBG = cv2.imread("Resources/BG.png")
    SUCCESS, img = cap.read()

    # Put webcam size like a size of background window for user
    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Detect hands
    hands, img = detector.findHands(imgScaled)

    if startGame:
        if stateResult is False:
            timer = time.time() - intialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435),
                        cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

        if timer > 3:
            stateResult = True
            timer = 0

            # detecting fingers
            if hands:
                playerMove = None
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0, 0, 0, 0, 0]:
                    playerMove = 1
                if fingers == [1, 1, 1, 1, 1]:
                    playerMove = 2
                if fingers == [0, 1, 1, 0, 0]:
                    playerMove = 3
                # AI step
                randomNuber = random.randint(1, 3)
                imgAI = cv2.imread(
                    f'Resources/{randomNuber}.png', cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                # Search winner
                # Players
                if(playerMove == 1 and randomNuber == 3) or \
                    (playerMove == 2 and randomNuber == 1) or \
                        (playerMove == 3 and randomNuber == 2):
                    score[1] += 1
                # AI
                if(playerMove == 3 and randomNuber == 1) or \
                    (playerMove == 1 and randomNuber == 2) or \
                        (playerMove == 2 and randomNuber == 3):
                    score[0] += 1

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    # Displaying current players score
    cv2.putText(imgBG, str(score[0]), (410, 215),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(score[1]), (1112, 215),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    cv2.imshow("BG", imgBG)

    # Starting game with key press

    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        intialTime = time.time()
        stateResult = False
