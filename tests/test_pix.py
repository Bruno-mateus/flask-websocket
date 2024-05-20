import sys
sys.path.append('../')
import os

import pytest
from payments.pix import Pix


def test_pix_create():
    pix = Pix()
    
    ## create payment
    pix_created = pix.create_payment(root="../")
    
    ## should be has a bank_payment_id
    assert "bank_payment_id" in pix_created
    
    ## should be has qr_code_path
    assert "qr_code_path" in pix_created
    
    ## should be save image qr code in temp/img
    assert os.path.isfile(f"../static/temp/img/{pix_created["qr_code_path"]}.png")