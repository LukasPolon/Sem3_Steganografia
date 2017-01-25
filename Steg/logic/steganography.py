import sys

from PIL import Image
from bitarray import bitarray

class Steganography(object):
    def __init__(self, image, message=None):
        self.img = image
        self.msg = message
        reload(sys)  
        sys.setdefaultencoding('windows-1251')

    def msg_to_bit(self, msg):
        to_bits = bitarray()
        to_bits.fromstring(msg)
        bit_list = to_bits.tolist()
        return bit_list
        
    def bit_to_msg(self, bitlist):
        to_msg = bitarray(bitlist)
        return to_msg.tostring()
        
    def lsb_replace(self, color, bit):
        new_color = int()
        if bit:
            new_color = color | 1
        else:
            new_color = color & ~1
        #print(color,bit, new_color)
        return new_color
        
    def get_lsb(self, color):
        if color & 1:
            lsb = True
        else:
            lsb = False
        return lsb
        
    def encode_image(self):
        
        # limit length of message to 255
        '''
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False
        # use a copy of image to hide the text in
        '''
        encoded = self.img.copy()
        width, height = self.img.size
        bitmsg = self.msg_to_bit(self.msg)
        leng = len(bitmsg)
        flag = False
        index = 0
        
        for row in range(height):
            for col in range(width):
                r, g, b = self.img.getpixel((col, row))

                if row == 0 and col == 0 and index < leng:
                    leng_split = [leng/3, leng/3, leng-((leng/3)*2)]
                    r = leng_split[0]
                    g = leng_split[1]
                    b = leng_split[2]
                elif index < leng:
                    new_colors = list()
                    for color in (r,g,b):
                        try:
                            bit = bitmsg.pop(0)
                            new_colors.append(self.lsb_replace(color, bit))
                            index += 1
                        except:
                            #print('err')
                            pass
                    try:
                        r = new_colors[0]
                    except:
                        pass
                        
                    try:
                        g = new_colors[1]
                    except:
                        pass
                        
                    try:
                        b = new_colors[2]
                    except:
                        pass
                     
                encoded.putpixel((col, row), (r, g, b))
                    

            if len(bitmsg) is 0:
                break
                
        return encoded
        

    def decode_image(self):
        width, height = self.img.size
        msg_bitlist = list()
        index = 0
        length = int()

        for row in range(height):
            for col in range(width):
                
                r, g, b = self.img.getpixel((col, row))
                if row == 0 and col == 0:
                    length = r + g + b
                elif index < length:
                    msg_bitlist.append(self.get_lsb(r))
                    msg_bitlist.append(self.get_lsb(g))
                    msg_bitlist.append(self.get_lsb(b))
                    index += 3
                #print(index, length)
                if index >= length:
                    break
            if index >= length:
                break
        msg_bitlist = msg_bitlist[:length]
        #print(msg_bitlist)
        return self.bit_to_msg(msg_bitlist)
        #return msg_bitlist

'''
if __name__ == '__main__':
    # pick a .png or .bmp file you have in the working directory
    # or give full path name
    original_image_file = "before.bmp"
    #original_image_file = "Beach7.bmp"
    #img = Image.open(original_image_file)
    # image mode needs to be 'RGB'
    #print(img, img.mode)  # test
    # create a new filename for the modified/encoded image
        #encoded_image_file = "enc_" + original_image_file
    # don't exceed 255 characters in the message
    secret_msg = "this is a secret message added to the image"
    #print(len(secret_msg))  # test
        #steg_en = Steganography(img, message=secret_msg)
        #img_encoded = steg_en.encode_image()
    #if img_encoded:
        # save the image with the hidden text
    #img_encoded.save(encoded_image_file)
    #print("{} saved!".format(encoded_image_file))
    #image = Image.open(encoded_image_file)
    #r, g, b = image.getpixel((0,0))
    #print(r)
        # view the saved file, works with Windows only
        # behaves like double-clicking on the saved file


        # get the hidden text back ...
    img2 = Image.open('enc_' + original_image_file)
    steg_de = Steganography(img2)
    hidden_text = steg_de.decode_image()
    print("Hidden text:\n{}".format(hidden_text))
    #hidden_text.pop(0)
    #to_msg = bitarray(hidden_text)
    #print(to_msg.tostring())
'''
from crypto import Crypto
#reload(sys)  
#sys.setdefaultencoding('windows-1251')

message = 'asfdhfgjhgfyujh'
cr1 = Crypto('pass', msg=message)
enc_mess = cr1.encrypt()
#print(enc_mess)
img = Image.open('before.bmp')
steg = Steganography(img, message=enc_mess)
img_encoded = steg.encode_image()
if img_encoded:
    img_encoded.save('after.bmp')
    print('Saved!')

img2 = Image.open('after.bmp')
steg2 = Steganography(img2)
encoded_text = steg2.decode_image()
#print(encoded_text)
cr2 = Crypto('pass', enc_msg=encoded_text)
print(cr2.decrypt())

#print(normal)
