import os
import cv2

from settings import PDF_IMAGES_DIR, FRAME_THRESH_NOISE, FRAME_THRESH_EMPHASIZE, PDF_UPLOAD_DIR


def process_image(frame, file_name, rotation_result=None, thresh_noise=FRAME_THRESH_NOISE):

    pdf_frame_path = os.path.join(PDF_UPLOAD_DIR, f"{file_name}.jpg")
    updated_frame_path = os.path.join(PDF_IMAGES_DIR, f"updated_{file_name}.jpg")
    if rotation_result == "clockwise":
        rotated_image = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    elif rotation_result == "anti_clockwise":
        rotated_image = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif rotation_result == "reflection":
        rotated_image = cv2.rotate(frame, cv2.ROTATE_180)
    else:
        rotated_image = frame

    cv2.imwrite(pdf_frame_path, cv2.cvtColor(rotated_image, cv2.COLOR_BGR2RGB))
    gray_image = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)
    thresh_frame = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                         FRAME_THRESH_EMPHASIZE, thresh_noise)
    # _, thresh_frame = cv2.threshold(gray_image, 220, 255, cv2.THRESH_BINARY)
    # cv2.imshow("thresh frame", thresh_frame)
    # cv2.waitKey()
    cv2.imwrite(updated_frame_path, thresh_frame)

    return updated_frame_path


if __name__ == '__main__':
    process_image(frame=cv2.imread(""), file_name="")
