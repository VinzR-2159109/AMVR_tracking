import cv2
import numpy as np

class FeatureBasedAROverlay:
    def __init__(self, video_source=0, src_img_path='edm_image.png'):
        self.video_source = video_source
        self.src_img = cv2.imread(src_img_path)
        self.cap = cv2.VideoCapture(video_source)

        # Initialize SIFT detector
        self.sift = cv2.SIFT_create()
        self.bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)  # For SIFT, NORM_L2 is better suited

        # Detect keypoints and descriptors in source image
        self.src_keypoints, self.src_descriptors = self.sift.detectAndCompute(self.src_img, None)

    def overlay_image(self, frame, homography):
        src_h, src_w = self.src_img.shape[:2]
        dst_pts = np.float32([[0, 0], [src_w, 0], [src_w, src_h], [0, src_h]]).reshape(-1, 1, 2)
        dst_pts = cv2.perspectiveTransform(dst_pts, homography)
        
        # Warp source image to the frame based on the homography
        warped_img = cv2.warpPerspective(self.src_img, homography, (frame.shape[1], frame.shape[0]))

        # Create mask for blending
        mask = np.zeros_like(frame, dtype=np.uint8)
        cv2.fillConvexPoly(mask, np.int32(dst_pts), (255, 255, 255))

        # Blend the warped image with the frame
        frame_mask = cv2.bitwise_not(mask)
        frame_roi = cv2.bitwise_and(frame, frame_mask)
        augmented_frame = cv2.add(frame_roi, warped_img)

        return augmented_frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Detect keypoints and descriptors in the frame
            frame_keypoints, frame_descriptors = self.sift.detectAndCompute(frame, None)

            # Match descriptors between the source image and the frame
            matches = self.bf.match(self.src_descriptors, frame_descriptors)

            # Sort matches based on distance (quality of the match)
            matches = sorted(matches, key=lambda x: x.distance)

            if len(matches) > 10:  # Ensure there are enough good matches
                # Extract location of the keypoints
                src_pts = np.float32([self.src_keypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
                dst_pts = np.float32([frame_keypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

                # Compute homography matrix
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                if M is not None:
                    frame = self.overlay_image(frame, M)

            # Display the augmented frame
            cv2.imshow('Augmented Reality Output', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


use_webcam = False

if use_webcam:
    overlay = FeatureBasedAROverlay(video_source=0, src_img_path='source_image.jpg')
else:
    overlay = FeatureBasedAROverlay(video_source='input_video_features.mp4', src_img_path='edm_image.png')

overlay.run()
