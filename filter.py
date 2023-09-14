

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.infrared,1, 640, 480, rs.format.y8, 30)
config.enable_stream(rs.stream.infrared,2, 640, 480, rs.format.y8, 30)
#config.enable_stream(rs.stream.color, 640, 480, rs.format.rgba8, 30)

profile = pipeline.start(config)

device = profile.get_device()
depth_sensor = device.first_depth_sensor()
device.hardware_reset()


while True:


    frames = pipeline.wait_for_frames()
    left_ir_frame = frames.get_infrared_frame(1)
    right_ir_frame = frames.get_infrared_frame(2)
 #   color_frame = frames.get_color_frame()
    

   # raw_ir = ir_frame.get_data()
#    blurred_ir = left_image.filter(IF.BLUR)
    left_image = np.asanyarray(left_ir_frame.get_data())
    cv2.imwrite('/home/basit/Realsense/Pics/non_sobel_img.png', left_image)

# GaussianBlur apply

 #   blurred_ir = cv2.GaussianBlur(left_image, (5, 5), 100)
#    ret, thresh = cv2.threshold(left_image, 127, 255, cv2.THRESH_BINARY)

#contour filter

 #   contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# it will apply contour on left_image
 #   cv2.drawContours(left_image, contours, -1, (0,255,0), 3) 

# sobel filter 
    sobel_x = cv2.Sobel(left_image, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(left_image, cv2.CV_64F, 0, 1, ksize=5)
    sobel = np.sqrt(np.square(sobel_x) + np.square(sobel_y))
    sobel = np.uint8(sobel)
    cv2.imwrite('/home/basit/Realsense/Pics/sobel_img.png', sobel)


# spatial filter
#    spatial_frame = rs.spatial_filter(0.5,20.0,2.0,1).process(right_ir_frame)
#    spatial_image = np.asanyarray(spatial_frame.get_data())

# temporal filter
#    temporal_frame = rs.temporal_filter(0.5,50.0,2).process(right_ir_frame)
#    temporal_image = np.asanyarray(temporal_frame.get_data())

# threshold filter
    right_image = np.asanyarray(right_ir_frame.get_data())
    ret, thresh = cv2.threshold(right_image, 127, 255, cv2.THRESH_BINARY)

#    cv2.imwrite('/home/basit/Realsense/Pics/threshold_img.png', thresh)
#    cv2.imwrite('/home/basit/Realsense/Pics/non_threshold_img.png', right_image)

  #  color_image = np.asanyarray(color_frame.get_data())
  #  cv2.imwrite('/home/basit/Realsense/Pics/color_img.png', color_image)

    images = np.hstack((sobel,thresh))

    cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('RealSense', images)

    cv2.waitKey(1)

pipeline.stop()
pipeline.close()
