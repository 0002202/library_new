import qrcode
import datetime
# import os
import random
def generate_dynamic_qrcode(data, file_path):
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=20, border=1)      
    # ERROR_CORRECT_L:7%的错误会被纠正
   
    qr.add_data(data)

    # while True:
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)

    # time.sleep(1)
    # os.remove(file_path)

if __name__ == '__main__':
    create_qrcode_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = "http://www.nbdj.xyz:8000/sign_success?create_qrcode_time="+str(create_qrcode_time)
    # data = "https://nbdj.xyz"
    
    file_path = "/python_item/my-library-2.0/user/static/img/qrcode/qrcode.png"
    generate_dynamic_qrcode(data, file_path)
