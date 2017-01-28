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
        """Convert message into bit list
        
            Args:
                msg(str): message to convert
                
            Returns:
                bit_list(list): list of bits (boolean variables)
        """
        to_bits = bitarray()
        to_bits.fromstring(msg)
        bit_list = to_bits.tolist()
        return bit_list
        
    def bit_to_msg(self, bitlist):
        """Convert list of bits into string
        
            Args:
                bitlist(list): list of bits (boolean variables)
            
            Returns:
                str: converted message
        """
        to_msg = bitarray(bitlist)
        return to_msg.tostring()
        
    def lsb_replace(self, color, bit):
        """Functon for lsb replace
        
            Args:
                color(str): one of rgb parts
                bit(bool): bit to which is to be converted
                
            Returns:
                new_color(str): color with replaced lsb
        """
        new_color = int()
        if bit:
            new_color = color | 1
        else:
            new_color = color & ~1
        return new_color
        
    def get_lsb(self, color):
        """ Function for putting out a LSB from color variable
            
            Args:
                color(str): one of rgb parts
                
            Returns:
                lsb(bool): True is 0, False is 1
        """
        if color & 1:
            lsb = True
        else:
            lsb = False
        return lsb
        
    def encode_image(self):
        '''
            Function used for encoding message into .bnp file, hiding 
            it in LSB of rgb bytes in pixels.
            
            Return:
                encoded(Image): image file ready to save
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
        """Function used for decoding hidden text from the image.
           Image must be a .bmp file. 
           It decode LSB in the picture.
           
           Returns:
                message(str): decoded message encrypted by SHA-512
        """
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
                
                if index >= length:
                    break
            if index >= length:
                break
        msg_bitlist = msg_bitlist[:length]
        message = self.bit_to_msg(msg_bitlist)
        
        return message


if __name__ == '__main__':

    from crypto import Crypto

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
