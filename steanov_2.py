from PIL import Image
import numpy as np

class Steganography:
    def create_stegeo_image(self, directory, filename, cipher_text):
        img = Image.open(directory + filename)
        img_arr = np.asarray(img)
        flat_arr = img_arr.flatten()
        flat_list = flat_arr.tolist()

        for x in range(0, len(cipher_text)):
            temp = flat_list[x]
            temp = bin(temp)
            temp = temp[:-1]
            temp += cipher_text[x]
            temp = eval(temp)
            flat_list[x] = temp

        modified_flat_arr = np.array(flat_list, dtype='uint8')
        modified_arr = modified_flat_arr.reshape(img_arr.shape)

        final_img = Image.fromarray(modified_arr, 'RGB')
        filename2 = directory + 'stego_' + filename
        final_img.save(filename2)

        return 'stego_' + filename

    def cypher_text_extracter(self, directory, filename):
        img = Image.open(directory + filename)
        img_arr = np.asarray(img)
        flat_arr = img_arr.flatten()
        flat_list = flat_arr.tolist()

        k = 25
        length = ""
        for x in range(k):
            temp = flat_list[x]
            if temp % 2 == 0:
                length += "0"
            else:
                length += "1"

        length_bin = "0b" + length
        cypher_txt = ""
        cypher_txt_length = eval(length_bin)

        for x in range(25, 25 + cypher_txt_length):
            temp = flat_list[x]
            if temp % 2 == 0:
                cypher_txt += "0"
            else:
                cypher_txt += "1"

        cypher_txt = length + cypher_txt
        return cypher_txt
