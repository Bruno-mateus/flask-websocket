from uuid import uuid4
import qrcode

class Pix:
    def __init__(self):
        pass
    def create_payment(self):
        ## simulate a bank_payment_id
        bank_payment_id = str(uuid4())     
        key_pix = f'random_payment_{bank_payment_id}'
        
        ## simulate a valid qr_code with key pix
        qr_code_img = qrcode.make(key_pix)     
        qr_code_img.save(f'./static/img/qr_code_{key_pix}.png')
        
        return {
            "bank_payment_id":bank_payment_id,
            "qr_code_path":f'qr_code_{key_pix}'
        }