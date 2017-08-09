import os
import asyncio
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
from PIL import ImageDraw, ImageOps
import PIL.Image
import PIL.ImageFont
import PIL.ImageTk
import cv2
import numpy as np
import tkinter
from array import array

# Run Configuration
os.environ['COZMO_PROTOCOL_LOG_LEVEL'] = 'DEBUG'
os.environ['COZMO_LOG_LEVEL'] = 'DEBUG'
USE_LOGGING = False
WRITE_TO_FILE = False

# TO INSTALL OPENCV ON MAC:
# brew install opencv3 --HEAD --with-contrib --with-python3
# to ~/.bash_profile add:
#   PYTHONPATH="/usr/local/Cellar/opencv3/HEAD-dd379ec_4/lib/python3.5/site-packages/:$PYTHONPATH"
#   export PYTHONPATH

'''
Edge Test
-Experimenting with Cozmo's camera and OpenCV
-Displays TKinter window with both pre and post-processed live camera feed
-
@author Lindsay Wright
'''
horizontal_mean_over_time=[]
right_mean_over_time=[]
left_mean_over_time=[]



class EdgeTest:
    def __init__(self):
        self._robot = None
        self._tk_root = 0
        self._tk_label_input = 0
        self._tk_label_output = 0
        self.count = 0
        if USE_LOGGING:
            cozmo.setup_basic_logging()
        cozmo.connect(self.run)

    def on_new_camera_image(self, event, *, image:cozmo.world.CameraImage, **kw):
        raw_image_no_crop = image.raw_image
        #undistort raw image
        cv2_undistort = cv2.cvtColor(np.array(raw_image_no_crop), cv2.COLOR_RGB2BGR) #convert to openCV format
        # cv2_image = self.undistort_image(cv2_undistort) #undistort
        cv2_image = cv2_undistort[80:235, 5:315]  # 320 width 240 height
        # cv2_image=cv2_image[80:235, 5:315] #320 width 240 height

        # Apply edge filter
        cv2_edges = self.auto_canny(cv2_image)
        minLineLength = 20
        maxLineGap = 20
        maxNumLines = 30
        cv2_lines = cv2.HoughLinesP(cv2_edges, 10, np.pi / 180, 100, maxNumLines, minLineLength, maxLineGap)
        # cv2_lines = self.auto_lines(cv2_edges)
        # print(cv2_lines)

        # Save OpenCV image
        if WRITE_TO_FILE:
            cv2_image_no_crop = cv2.cvtColor(np.array(raw_image_no_crop), cv2.COLOR_RGB2BGR) # Convert PIL Image to OpenCV Image
            cv2.imwrite("input/input%d.jpg" % self.count, cv2_image_no_crop)
            cv2.imwrite("edges/edges%d.jpg" % self.count, cv2_edges)

        # Convert output image back to PIL image
        pil_edges = PIL.Image.fromarray(cv2.cvtColor(cv2_edges, cv2.COLOR_GRAY2RGB))

        # Display input and output feed
        self.catagorize_lines(cv2_lines,image.raw_image)
        display_image_input = PIL.ImageTk.PhotoImage(image=image.raw_image)
        display_image_output = PIL.ImageTk.PhotoImage(image=pil_edges)

        #This section converts back to PIL and saves images that have been drawn on (aka output image)
        if WRITE_TO_FILE:
            cv2_print_output = cv2.cvtColor(np.array(image.raw_image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("output/output%d.jpg" % self.count, cv2_print_output)
            self.count += 1

        self._tk_label_input.imgtk = display_image_input
        self._tk_label_input.configure(image=display_image_input)
        self._tk_label_output.imgtk = display_image_output
        self._tk_label_output.configure(image=display_image_output)
        self._tk_root.update()





    # Auto-paramter Canny edge detection adapted from:
    # http://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    def auto_canny(self, img, sigma=0.33):  #was .33
        blurred = cv2.GaussianBlur(img, (3, 3), 0)
        v = np.median(blurred)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(blurred, lower, upper)
        return edged

    #hough line detection
    def auto_lines(self, img):
        minLineLength = 50
        maxLineGap = 5
        maxNumLines = 30
        lines = cv2.HoughLinesP(img, 10, np.pi / 180, 100, maxNumLines, minLineLength, maxLineGap)
        return lines

    #undistort Image
    def undistort_image(slef, img):
        cameraMatrix = np.matrix('289.75,0,116.6; 0,290.51,113.6; 0,0,1')
        distCoef = np.matrix('0.0472, 0.003, 0.000272, 0.0003524')
        undistorted_image = cv2.undistort(img, cameraMatrix, distCoef)
        return undistorted_image

    #catagorizes the lines and computes the average of each type, updates the list of averages
    def catagorize_lines(self, lines, draw_on):
        draw = ImageDraw.Draw(draw_on)
        a, b, c = lines.shape
        vertical, horizontal, left, right = [],[],[],[]
        #catagorize lines into types
        for i in range(a):
            x1 = lines[i][0][0]+5
            y1 = lines[i][0][1]+80
            x2 = lines[i][0][2]+5
            y2 = lines[i][0][3]+80
            if (x1-x2)<10 and (x1-x2)>-10: #vertical
                vertical.append([x1,y1,x2,y2])

            elif (y1-y2)<6 and (y1-y2)>-6: #horizontal
                horizontal.append([x1,y1,x2,y2])

            elif ((y1-y2)/(x1-x2)) > 0.3: #right
                right.append([x1,y1,x2,y2])

            elif ((y1-y2)/(x1-x2)) < -0.3: #left
                left.append([x1,y1,x2,y2])

        #compute mean of all line types if they exist, then draw the mean of the last 15 means
        if vertical:
            vertical_mean=np.mean(vertical, axis=0,dtype=np.int)
            draw.line([(vertical_mean[0], vertical_mean[1]), (vertical_mean[2], vertical_mean[3])], fill=(0, 128, 0), width=4)  # Vertical green
        if horizontal: #if there was horizontal lines found
            horizontal_mean = np.mean(horizontal, axis=0,dtype=np.int) #calculate the mean of this frame
            horizontal_mean_over_time.append(horizontal_mean) #add it to the list that saves previous frames
            if len(horizontal_mean_over_time) > 10: #if that list gets over 15, then dump the oldest number
                horizontal_mean_over_time.pop(0)
            horizontal_mean = np.mean(horizontal_mean_over_time, axis=0, dtype=np.int)
            draw.line([(horizontal_mean[0], horizontal_mean[1]), (horizontal_mean[2], horizontal_mean[3])],fill=(128, 0, 128), width=4)  # Horizontal purple
        if not horizontal:
            horizontal_mean_over_time[:]=[]
        if right:
            right_mean = np.mean(right, axis=0,dtype=np.int)
            right_mean_over_time.append(right_mean)  # add it to the list that saves previous frames
            if len(right_mean_over_time) > 10:  # if that list gets over 5, then dump the oldest number
                 right_mean_over_time.pop(0)
            right_mean = np.mean(right_mean_over_time, axis=0, dtype=np.int)
            draw.line([(right_mean[0], right_mean[1]), (right_mean[2], right_mean[3])], fill=(135, 206, 250), width=4)  # Right light blue
        if not right:
            right_mean_over_time[:]=[]
        if left:
            left_mean =np.mean(left, axis=0,dtype=np.int)
            left_mean_over_time.append(left_mean)  # add it to the list that saves previous frames
            if len(left_mean_over_time) > 10:  # if that list gets over 15, then dump the oldest number
                 left_mean_over_time.pop(0)
            left_mean = np.mean(left_mean_over_time, axis=0, dtype=np.int)
            draw.line([(left_mean[0], left_mean[1]), (left_mean[2], left_mean[3])], fill=(255, 0, 0), width=4)  # Left red
        if not left:
            left_mean_over_time[:]=[]

    def straighten_out(self):
        if len(left_mean_over_time) == 0 and len(right_mean_over_time) > 0:
            cozmo.robot.Robot.turn_in_place(angle=degrees(5),in_parallel=True,num_retries=0).wait_for_completed() #turn left
        if len(right_mean_over_time) == 0 and len(left_mean_over_time) > 0:
            cozmo.robot.Robot.turn_in_place(angle=degrees(-5), in_parallel=True, num_retries=0).wait_for_completed() #turn right



    async def set_up_cozmo(self, coz_conn):
        asyncio.set_event_loop(coz_conn._loop)
        self._robot = await coz_conn.wait_for_robot()
        self._robot.camera.image_stream_enabled = True
        self._robot.add_event_handler(cozmo.world.EvtNewCameraImage, self.on_new_camera_image)
        self._robot.set_head_angle(cozmo.util.Angle(degrees=0))


    async def run(self, coz_conn):
        # Set up Cozmo
        await self.set_up_cozmo(coz_conn)

        self._tk_root = tkinter.Tk()
        # TODO: ESC to exit
        self._tk_label_input = tkinter.Label(self._tk_root)
        self._tk_label_output = tkinter.Label(self._tk_root)
        self._tk_label_input.pack()
        self._tk_label_output.pack()
        #self.straighten_out()

        while True:
            await asyncio.sleep(0)


if __name__ == '__main__':
    EdgeTest()




