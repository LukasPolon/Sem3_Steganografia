import sys

from PIL import Image
from bitarray import bitarray

class Steganography(object):
    def __init__(self, image, message=None):
        self.img = image
        self.msg = message
        reload(sys)  
        sys.setdefaultencoding('utf8')

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

        return new_color
        
    def get_lsb(self, color):
        if color & 1:
            lsb = True
        else:
            lsb = False
        return lsb
        
    def encode_image(self):
        length = len(self.msg)
        # limit length of message to 255
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        if img.mode != 'RGB':
            print("image mode needs to be RGB")
            return False
        # use a copy of image to hide the text in
        encoded = self.img.copy()
        width, height = self.img.size
        bitmsg = self.msg_to_bit(self.msg)
        index = 0
        for row in range(height):
            for col in range(width):
                r, g, b = self.img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    r = len(bitmsg)
                elif index <= length:
                    try:
                        bit = bitmsg.pop(0)
                        r = self.lsb_replace(r, bit)
                    except IndexError:
                        pass

                    try:
                        bit = bitmsg.pop(0)
                        g = self.lsb_replace(g, bit)
                    except IndexError:
                        pass
                        
                    try:
                        bit = bitmsg.pop(0)
                        g = self.lsb_replace(g, bit)
                    except IndexError:
                        pass

                    #c = self.msg[index]
                    #asc = ord(c)
                #else:
                    #asc = r
                    #break
                
                encoded.putpixel((col, row), (r, g, b))
                index += 1
        return encoded
        
    


    def decode_image(self):
        width, height = self.img.size
        msg_bitlist = list()
        index = 0
        length = int()

        for row in range(height):
            for col in range(width):
                try:
                    r, g, b = self.img.getpixel((col, row))
                except ValueError:
                    # need to add transparency a for some .png files
                    r, g, b, a = self.img.getpixel((col, row))
                # first pixel r value is length of message
                if row == 0 and col == 0:
                    length = r
                elif index <= length:
                    msg_bitlist.append(self.get_lsb(r))
                    msg_bitlist.append(self.get_lsb(g))
                    msg_bitlist.append(self.get_lsb(b))
                    print(index)
                index += 1
        
        return self.bit_to_msg(msg_bitlist)


if __name__ == '__main__':
    # pick a .png or .bmp file you have in the working directory
    # or give full path name
    original_image_file = "before.bmp"
    # original_image_file = "Beach7.bmp"
    #!img = Image.open(original_image_file)
    # image mode needs to be 'RGB'
    #print(img, img.mode)  # test
    # create a new filename for the modified/encoded image
    #!encoded_image_file = "enc_" + original_image_file
    # don't exceed 255 characters in the message
    secret_msg = "this is a secret message added to the image"
    #print(len(secret_msg))  # test
    #!steg_en = Steganography(img, message=secret_msg)
    #!img_encoded = steg_en.encode_image()
    #if img_encoded:
        # save the image with the hidden text
        #!img_encoded.save(encoded_image_file)
        #print("{} saved!".format(encoded_image_file))
        # view the saved file, works with Windows only
        # behaves like double-clicking on the saved file


        # get the hidden text back ...
    img2 = Image.open('enc_' + original_image_file)
    steg_de = Steganography(img2)
    hidden_text = steg_de.decode_image()
    print("Hidden text:\n{}".format(hidden_text))

