# All imports required
import os
import cv2
import numpy as np


background = None
accumulated_weight = 0.5

# box dimensions
ROI_top = 10
ROI_bottom = 500
ROI_right = 100
ROI_left = 600

# separating the background and foreground image
def cal_accum_avg(frame, accumulated_weight):
    global background

    if background is None:
        background = frame.copy().astype("float")
        return None

    cv2.accumulateWeighted(frame, background, accumulated_weight)
    # cv2.imshow("accumulated weight", frame)


# gesture detection part
def segment_hand(frame, threshold=25):
    global background

    # find the difference between the background and the moving frame in front
    diff = cv2.absdiff(background.astype("uint8"), frame)

    # threshold the diff image so that we get the foreground
    _, thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

    cv2.imshow("Thresholded",thresholded)

    # Grab the external contours for the image
    contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow('After Contouring', thresholded)

    print("Number of Contours found = " + str(len(contours)))

    # cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)
    # cv2.imshow('Contours', frame)
    #
    if len(contours) == 0:
        return None
    else:
        hand_segment_max_cont = max(contours, key=cv2.contourArea)

        return (_, thresholded, hand_segment_max_cont,contours , diff)


cam = cv2.VideoCapture(0)

num_frames = 0
element = 1
num_imgs_taken = 0

while True:
    ret, frame = cam.read()

    # flipping the frame to prevent inverted image of captured frame...
    frame = cv2.flip(frame, 1)

    frame_copy = frame.copy()

    roi = frame[ROI_top:ROI_bottom, ROI_right:ROI_left]

    gray_frame = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # we are converting roi (that rectangle) to gray scale
    gray_frame = cv2.GaussianBlur(gray_frame, (9, 9), 0)  # smoothning and blurring of the gray scale image

    cv2.rectangle(frame_copy, (ROI_left, ROI_top), (ROI_right, ROI_bottom), (255, 255, 0), 3)

    if num_frames < 60:
        cal_accum_avg(gray_frame, accumulated_weight)
        if num_frames <= 59:
            cv2.putText(frame_copy, "FETCHING BACKGROUND ...PLEASE WAIT", (80, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (0, 0, 255), 2)

    elif num_frames <= 300:
        cv2.putText(frame_copy, "Hand gesture can begin for " + str(element), (80, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (255, 0, 255), 2)
        hand = segment_hand(gray_frame)
        # print("hand is " , hand)
        if hand is not None:
        #
             thresholded = hand[0]
             hand_segment = hand[1]
             contours = hand[2]
             print(thresholded)
             print(hand_segment)
             print(len(contours))
        #
        #     # Draw contours around hand segment
        #    print((ROI_right,ROI_top))
             # cont = [hand_segment+(ROI_right,ROI_top)]

             cv2.drawContours(gray_frame, contours, -1, (255, 0, 0),3)
             # cv2.imshow("Contours",frame)
             cv2.drawContours(frame_copy, contours, -1, (255, 255, 0), 3)
             cv2.imshow('Contours', gray_frame)
        #
             cv2.putText(frame_copy, str(num_frames)+"For" + str(element), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        #
        #     # Also display the thresholded image
        #      cv2.imshow("Thresholded Hand Image", thresholded)

    else:
        cv2.putText(frame_copy, "300 frames crossed", (80, 600), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2)
        # Segmenting the hand region...
        hand = segment_hand(gray_frame)


        # find the difference between the background and the moving frame in front
        diff = cv2.absdiff(background.astype("uint8"), gray_frame)
        #
        # # threshold the diff image so that we get the foreground
        _, thresholded_1 = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        #
        cv2.imshow("Thresholded_1", thresholded_1)
        #
        # # Grab the external contours for the image
        # contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # # cv2.imshow('After Contouring', thresholded)
        #
        # print("Number of Contours found = " + str(len(contours)))
        #
        # # cv2.drawContours(frame, contours, -1, (255, 255, 0), 3)
        # # cv2.imshow('Contours', frame)
        # #
        # if len(contours) == 0:
        #     # return None
        #     print("No contours")
        # else:
        #     hand_segment_max_cont = max(contours, key=cv2.contourArea)
        #
        #     # return (_, thresholded, hand_segment_max_cont, contours)

        # Checking if we are able to detect the hand...
        if hand is not None:

            # unpack the thresholded img and the max_contour...
            # thresholded, hand_segment = hand //given code
            thresholded = hand[0]
            hand_segment = hand[1]
            contours = hand[2]
            diff = hand[3]
            # print(thresholded)
            # print(hand_segment)
            # print(len(contours))
            # hand_segment = hand_segment_max_cont

            # Drawing contours around hand segment
            # cv2.drawContours(frame_copy,contours, -1, (255, 0, 0), 1) //given code
            # _, thresholded_1 = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
            # cv2.imshow("Thresholded _1", thresholded_1)

            cv2.drawContours(gray_frame, contours, -1, (255, 0, 0), 3)
            # cv2.imshow("Contours",frame)
            cv2.drawContours(frame_copy, contours, -1, (255, 255, 0), 3)
            cv2.imshow('Contours', gray_frame)

            cv2.putText(frame_copy, str(num_frames), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            # cv2.putText(frame_copy, str(num_frames)+"For" + str(element), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            cv2.putText(frame_copy, str(num_imgs_taken) + 'images' + "For" + str(element), (200, 400),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Displaying the thresholded image
            # cv2.imshow("Thresholded_1", thresholded)
            if num_imgs_taken <= 1500:
                # cv2.imwrite(r"D:\\gesture\\train\\"+str(element)+"\\" + str(num_imgs_taken+300) + '.jpg', thresholded)
                image_path = r'/Users/dhruvishamondhe/PycharmProjects/Mini Project-pycharm/gesture/train/9/dog.jpg'
                directory = r'/Users/dhruvishamondhe/PycharmProjects/Mini Project-pycharm/gesture/train/9'
                img = cv2.imread(image_path)
                os.chdir(directory)
                filename = str(num_imgs_taken) + '.jpg'
                filename_1 = str(num_imgs_taken) + '-copy' + '.jpg'
                cv2.imwrite(filename, thresholded_1)
                cv2.imwrite(filename_1, thresholded_1)

                print("image saved")

            else:
                break
            num_imgs_taken += 1
        else:
            cv2.putText(frame_copy, 'No hand detected...', (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Showing the frames
    cv2.imshow("Sign Detection", frame_copy)
    # cv2.imshow("Gray frame", gray_frame)
    num_frames = num_frames + 1

    # Closing windows with Esc key...(any other key with ord can be used too.)
    k = cv2.waitKey(1) & 0xFF

    if k == 27:
        break

# Releasing camera & destroying all the windows...

cv2.destroyAllWindows()
cam.release()
