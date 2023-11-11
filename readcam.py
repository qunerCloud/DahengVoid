import gxipy as gx
import cv2

device_manager = gx.DeviceManager()
dev_num, dev_info_list = device_manager.update_device_list()
if dev_num == 0:
    sys.exit(1)
#change sn here to read different cam.
str_sn = dev_info_list[0].get("sn")

class DahengCamera:
    def __init__(self, serial_number):
        # ??????????
        self.device_manager = gx.DeviceManager()
        _, dev_info_list = self.device_manager.update_device_list()
        if not dev_info_list:
            raise RuntimeError("No Daheng devices found")
        
        # ??????????????????
        self.cam = self.device_manager.open_device_by_sn(str_sn, 4)
        # ????????
        self.cam.stream_on()

    def read(self):
        # ????????????
        raw_image = self.cam.data_stream[0].get_image()
        if raw_image is None:
            return False, None
        rgb_image = raw_image.convert("RGB")
        numpy_image = rgb_image.get_numpy_array()
        if numpy_image is None:
            return False, None
        # ?? RGB ?????? BGR
        bgr_image = cv2.cvtColor(numpy_image, cv2.COLOR_RGB2BGR)
        return True, bgr_image

    def release(self):
        # ??????????????????
        self.cam.stream_off()
        self.cam.close_device()

def main(args=None):
    camera = DahengCamera(str_sn)
