import cv2
import numpy as np

def calculate_angle(point1, point2):
    """Calculate the angle between two points."""
    x_diff = point2[0] - point1[0]
    y_diff = point2[1] - point1[1]
    return np.degrees(np.arctan2(y_diff, x_diff))

# Read the image
image = cv2.imread('arrow_1.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply thresholding
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours by area and keep only the largest one
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

# Draw the arrow contour
arrow_contour_image = np.zeros_like(image)
cv2.drawContours(arrow_contour_image, contours, -1, (0, 255, 0), 2)

# Find the centroid of the arrow contour
M = cv2.moments(contours[0])
centroid_x = int(M['m10'] / M['m00'])
centroid_y = int(M['m01'] / M['m00'])
centroid = (centroid_x, centroid_y)

# Draw the centroid
cv2.circle(arrow_contour_image, centroid, 5, (0, 0, 255), -1)

# Calculate distances from each contour point to the centroid
distances = [np.linalg.norm(np.array(centroid) - contour_point[0]) for contour_point in contours[0]]

# Find the indices of the two points with the smallest distances to the centroid
indices = np.argsort(distances)[:2]

# Get the neighboring sharp points
sharp_points = [tuple(contours[0][i][0]) for i in indices]

# Draw the sharp points
for point in sharp_points:
    cv2.circle(arrow_contour_image, point, 5, (255, 0, 0), -1)

# Draw a line joining the two sharp points
cv2.line(arrow_contour_image, sharp_points[0], sharp_points[1], (255, 0, 0), 2)

# Calculate the slope of the line joining the sharp points
if sharp_points[0][0] != sharp_points[1][0]:
    slope = (sharp_points[1][1] - sharp_points[0][1]) / (sharp_points[1][0] - sharp_points[0][0])
else:
    slope = float('inf')

# Find the negative reciprocal to get the slope of the perpendicular line
if slope != 0:
    perpendicular_slope = -1 / slope
else:
    perpendicular_slope = float('inf')

# Calculate the coordinates of the endpoints of the perpendicular line
if perpendicular_slope != float('inf'):
    x1 = centroid_x - 100
    y1 = int(centroid_y - 100 * perpendicular_slope)
    x2 = centroid_x + 100
    y2 = int(centroid_y + 100 * perpendicular_slope)
else:
    # Handle the case when the slope is zero (vertical line)
    x1 = centroid_x
    y1 = centroid_y - 100
    x2 = centroid_x
    y2 = centroid_y + 100

# Draw the perpendicular line
cv2.line(arrow_contour_image, (x1, y1), (x2, y2), (0, 255, 255), 2)

# Calculate the angle between the perpendicular line and the horizontal
angle_with_horizontal = calculate_angle((x1, y1), (x2, y2))

# Display the image with arrow contour, centroid, sharp points, and lines
cv2.imshow('Arrow Contour with Centroid, Sharp Points, and Lines', arrow_contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the angle
print("Angle with horizontal (degrees):", angle_with_horizontal)
