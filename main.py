import cv2
import numpy as np

class ArucoAROverlay:
    def __init__(self, video_source=0, src_img_path='source_image.jpg'):

        self.video_source = video_source
        self.src_img = cv2.imread(src_img_path)
        self.cap = cv2.VideoCapture(video_source)
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        self.parameters = cv2.aruco.DetectorParameters()

    def draw_corners(self, frame, corners):
        for corner in corners:
            for point in corner:
                cv2.circle(frame, tuple(point.astype(int)), 5, (0, 255, 0), -1)

    def overlay_image_across_markers(self, frame, marker_corners):
        src_h, src_w = self.src_img.shape[:2]
        src_pts = np.float32([[0, 0], [src_w, 0], [src_w, src_h], [0, src_h]])
        dst_pts = np.float32(marker_corners)

        M, status = cv2.findHomography(src_pts, dst_pts)
        if M is None:
            print("Homography matrix couldn't be computed.")
            return frame

        warped_img = cv2.warpPerspective(self.src_img, M, (frame.shape[1], frame.shape[0]))
        mask = np.zeros_like(frame, dtype=np.uint8)
        cv2.fillConvexPoly(mask, np.int32(dst_pts), (255, 255, 255))

        frame_mask = cv2.bitwise_not(mask)
        frame_roi = cv2.bitwise_and(frame, frame_mask)
        augmented_frame = cv2.add(frame_roi, warped_img)

        return augmented_frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, corners, ids)
                if len(corners) >= 4:
                    ids = ids.flatten()
                    sorted_indices = [np.where(ids == i)[0][0] for i in [0, 1, 3, 2]]
                    sorted_corners = [corners[i].reshape((4, 2)) for i in sorted_indices]
                    self.draw_corners(frame, sorted_corners)

                    marker_corners = np.array([
                        sorted_corners[0][0],
                        sorted_corners[1][1],
                        sorted_corners[2][2],
                        sorted_corners[3][3],
                    ], dtype="float32")

                    frame = self.overlay_image_across_markers(frame, marker_corners)

            cv2.imshow('Augmented Reality Output', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


use_webcam = False

if use_webcam:
    overlay = ArucoAROverlay(video_source=0, src_img_path='source_image.jpg')
else:
    overlay = ArucoAROverlay(video_source='input_video.mp4', src_img_path='source_image.jpg')

overlay.run()
