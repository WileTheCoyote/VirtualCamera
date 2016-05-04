# Python Script that uses the user and password to access the livestream for
# the camera with the provided ip address, opens video with imshow from openCV
# - Also look to VirtualCamMotor.py
# - Found a very few very helpful instructibles tutorial that I referenced for this project,
# based off a popular project from fabericate.io - they had completed a similiar
# task with a kaiCong camera (I also used a KaiCong but a different model) - intructables
# url and other links in below references


from base.KaicongInput import KaicongInput

class VirtualCamVideo(KaicongInput):
    PACKET_SIZE = 1024
    URI = "http://%s:81/livestream.cgi?user=%s&pwd=%s&streamid=3&audio=1&filename="
    
    def __init__(self, domain, callback, user="rysm7991", pwd="rysm7991"):
        KaicongInput.__init__(
            self, 
            callback,
            domain, 
            VirtualCamVideo.URI, 
            VirtualCamVideo.PACKET_SIZE, 
            user, 
            pwd
        )
        self.bytes = ''
    
    def handle(self, data):
        self.bytes += data
        a = self.bytes.find('\xff\xd8')
        b = self.bytes.find('\xff\xd9')
        if a!=-1 and b!=-1:
            jpg = self.bytes[a:b+2]
            self.bytes = self.bytes[b+2:]
            return jpg
            
            
if __name__ == "__main__":
    import numpy as np
    import cv2
    import sys
    
    if len(sys.argv) != 2:
        print "Usage: %s <ip_address>" % sys.argv[0]
        sys.exit(-1)
    
    def show_video(jpg):    
        img = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
        cv2.imshow('Virtual Video',img)
        
        # Note: waitKey() actually pushes the image out to screen
        if cv2.waitKey(1) ==27:
            exit(0)  
    
    video = VirtualCamVideo(sys.argv[1], show_video)
    video.run()


# URL References
# KaiCong User Manual - http://www.kaicong.net/word/SIP1406en.pdf
# Main Instruc. - http://www.instructables.com/id/Hack-a-30-WiFi-Pan-Tilt-Camera-Video-Audio-and-Mot/
# Other Instruc. - http://www.instructables.com/id/Android-controlled-RC-Vehicle-with-real-time-Video/
# http://fabricate.io
