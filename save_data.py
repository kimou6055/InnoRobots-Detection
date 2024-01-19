import cv2

import cv2.aruco as aruco
import numpy as np 



mapx=2000
mapy=3000

def Calculate_homography(corners,ids,img, mapx=mapx/1000 , mapy=mapy/1000,homography_matrix_path = r"E:\esprit_4eme_annee\robotics\homography_matrix.npz"):
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    homography_matrix = None
    

    if ids is not None:
        print("Detected ArUco IDs:", ids.flatten())
        aruco.drawDetectedMarkers(img, corners, ids)
    else:
        print("No ArUco markers detected")
    
# Define marker locations in 3D space (assuming they lie on the z=0 plane)
    marker_length = cv2.getTrackbarPos("Marker Length", "Trackbars") / 100.0  # Scaling back to meters
    x_aruco = cv2.getTrackbarPos("X Aruco", "Trackbars") / 1000.0  # Adjust scale as needed
    y_aruco = cv2.getTrackbarPos("Y Aruco", "Trackbars") / 1000.0  # Adjust scale as needed
    marker_locations_3d = {
    21: np.array([(x_aruco-marker_length, y_aruco-marker_length, 0), (x_aruco+marker_length, y_aruco-marker_length, 0), (x_aruco+marker_length, y_aruco+marker_length, 0), (x_aruco-marker_length, y_aruco+marker_length, 0)]),
    23: np.array([(mapx-x_aruco-marker_length, y_aruco-marker_length, 0), (mapx-x_aruco+marker_length, y_aruco-marker_length, 0), (mapx-x_aruco+marker_length, y_aruco+marker_length, 0), (mapx-x_aruco-marker_length, y_aruco+marker_length, 0)]),
    20: np.array([(x_aruco-marker_length, mapy-y_aruco-marker_length, 0), (x_aruco+marker_length, mapy-y_aruco-marker_length, 0), (x_aruco+marker_length, mapy-y_aruco+marker_length, 0), (x_aruco, mapy-y_aruco+marker_length, 0)]),
    22: np.array([(mapx-x_aruco-marker_length, mapy-y_aruco-marker_length, 0), (mapx-x_aruco+marker_length, mapy-y_aruco-marker_length, 0), (mapx-x_aruco+marker_length, mapy-y_aruco+marker_length, 0), (mapx-x_aruco-marker_length, mapy-y_aruco+marker_length, 0)])
    }   
# Assume all markers are on the same flat surface (z=0)
    image_points = []
    object_points = []
    
    if ids is not None:
        for i, marker_id in enumerate(ids.flatten()):
            if marker_id in marker_locations_3d:
                image_points.append(corners[i][0])
                object_points.append(marker_locations_3d[marker_id])
# Flatten the arrays for homography
    image_points = np.array(image_points).reshape(-1, 2)
    
    object_points = np.array(object_points).reshape(-1, 3)
# Compute the homography matrix if we have enough correspondences
    if len(image_points) >= 4:
    # Calculate homography
        homography_matrix, _ = cv2.findHomography(object_points[:, :2], image_points)
    # Define the 3D coordinates of the map corners assuming z=0
        np.savez(homography_matrix_path, homography_matrix=homography_matrix)

    return homography_matrix 
    

