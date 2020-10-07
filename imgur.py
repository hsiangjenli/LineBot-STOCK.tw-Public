# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 11:15:16 2020

@author: User
"""
import pyimgur

def upload_to_imgur(CLIENT_ID, savefig):
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(savefig, title="")
    return uploaded_image.link