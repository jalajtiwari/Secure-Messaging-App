from Decryption import Decryption
from Encryption import Encryption
from preprocessing import Preprocessing
from steanov_2 import STEGANOGRAPHY
from flask import Flask, render_template, request, redirect,url_for,abort,make_response,message_flashed,redirect
from werkzeug.utils import secure_filename
import os
import pyautogui
import random
from datetime import datetime
from PIL import Image

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = "static/uploads/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Crpytography:
    def key_generation(self):
        minimum = 9999999999
        key = []
        f = 0

        for i in range(128):
            temp = random.randint(0, 1)
            x, y = pyautogui.position()
            now = datetime.now()
            day = now.day
            month = now.month
            year = now.year

            key.append(temp ^ x ^ y ^ day ^ month ^ year)
            if f == 0:
                print(key[i], temp, x, y, day, month, year)
                f += 1
            minimum = min(minimum, key[i])

        for i in range(128):
            key[i] = key[i] - minimum

        k = "".join(map(str, key))
        return k

    def Crpyto_Encrytor_Decryptor(self, p_text):
        plain_text = p_text + "#####"
        print(f"Entered plain Txt: {plain_text}")

        preprocessor = Preprocessing()
        plain_2_binary_string = preprocessor.string_2_binary(plain_text)
        prepended_binary_string = plain_2_binary_string
        padded_binary_string = preprocessor.padding_of_text(prepended_binary_string)

        encryptor = Encryption()
        print(f"Padded Binary string pt1_txt --> : {padded_binary_string}")

        cipher_text = ""
        pt1_txt = padded_binary_string
        keys = self.key_generation()
        KEYS = preprocessor.Convert128_to_32bits(keys)

        for i in range(0, len(padded_binary_string), 128):
            string_128_bit = padded_binary_string[i:i+128]
            EI_S = preprocessor.Convert128_to_32bits(string_128_bit)
            C1, C2, C3, C4 = encryptor.Encrypt(EI_S, KEYS)
            cipher_text += C1 + C2 + C3 + C4

        print("cipher_text\n", cipher_text)
        print('\n')
        print("pt1_txt\n", pt1_txt)
        print("\n\n")

        ct_text = cipher_text
        prepended_cypher_txt = preprocessor.prepend_length_of_binary_string(cipher_text)
        padded_cypher_txt = preprocessor.padding_of_text(prepended_cypher_txt)
        cypher_txt_after_extraction = preprocessor.extract_real_binary_string(padded_cypher_txt)

        padded_pt_text = ""
        decryptor = Decryption()

        for i in range(0, len(cypher_txt_after_extraction), 128):
            cypher_128_bit = cypher_txt_after_extraction[i:i+128]
            CT_S = preprocessor.Convert128_to_32bits(cypher_128_bit)
            E1, E2, E3, E4 = decryptor.Decrypt(CT_S, KEYS)
            padded_pt_text += E1 + E2 + E3 + E4

        print("padded_pt_text\n", padded_pt_text)
        print('\n')
        print("Ab bata jara ", end="")
        print(pt1_txt == padded_pt_text)
        real_pt_text = padded_pt_text
        real_plain_text = preprocessor.binary_2_string(real_pt_text)
        print(f"\n\n\n\n\n\n\n\n\n After all the actual text was: --> {real_plain_text}\n\n\n\n\n\n\n\n\n")
        return ct_text, real_plain_text

    def Crpyto_Encrytor(self, p_text):
        plain_text = p_text + "#####"
        print(f"Entered plain Txt: {plain_text}")

        preprocessor = Preprocessing()
        plain_2_binary_string = preprocessor.string_2_binary(plain_text)
        prepended_binary_string = plain_2_binary_string
        padded_binary_string = preprocessor.padding_of_text(prepended_binary_string)

        encryptor = Encryption()
        print(f"Padded Binary string pt1_txt --> : {padded_binary_string}")

        cipher_text = ""
        pt1_txt = padded_binary_string
        keys = self.key_generation()
        KEYS = preprocessor.Convert128_to_32bits(keys)

        for i in range(0, len(padded_binary_string), 128):
            string_128_bit = padded_binary_string[i:i+128]
            EI_S = preprocessor.Convert128_to_32bits(string_128_bit)
            C1, C2, C3, C4 = encryptor.Encrypt(EI_S, KEYS)
            cipher_text += C1 + C2 + C3 + C4

        print("cipher_text\n", cipher_text)
        print('\n')
        print("pt1_txt\n", pt1_txt)
        print("\n\n")
        return cipher_text, keys

    def Crpyto_Decryptor(self, cipher_text, k, flag):
        preprocessor = Preprocessing()
        ct_text = cipher_text

        if flag == 1:
            cypher_txt_after_extraction = preprocessor.extract_real_binary_string(cipher_text)
        else:
            cypher_txt_after_extraction = cipher_text

        padded_pt_text = ""
        keys = k
        KEYS = preprocessor.Convert128_to_32bits(keys)
        decryptor = Decryption()

        for i in range(0, len(cypher_txt_after_extraction), 128):
            cypher_128_bit = cypher_txt_after_extraction[i:i+128]
            CT_S = preprocessor.Convert128_to_32bits(cypher_128_bit)
            E1, E2, E3, E4 = decryptor.Decrypt(CT_S, KEYS)
            padded_pt_text += E1 + E2 + E3 + E4

        print("padded_pt_text\n", padded_pt_text)
        print('\n')
        real_pt_text = padded_pt_text
        real_plain_text = preprocessor.binary_2_string(real_pt_text)
        print(f"\n\n\n\n\n\n\n\n\n After all the actual text was: --> {real_plain_text}\n\n\n\n\n\n\n\n\n")
        return ct_text, real_plain_text


# Encrypt
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/encrypt', methods=['GET'])
def encrypt():
    return render_template("Encrypt.html")


@app.route('/decrypt', methods=['POST'])
def decrypt():
    c = Crpytography()
    passed = True
    preprocessor = Preprocessing()

    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('uploaded_image filename: ' + filename)

        plain_text = request.form.get('PLAIN_TEXT')
        real_plain_text = plain_text
        cypher_text, keys = c.Crpyto_Encrytor(plain_text)
        directory = "static/uploads/"
        prepended_cypher_txt = preprocessor.prepend_length_of_binary_string(cypher_text)
        ct_text = cypher_text
        padded_cypher_txt = preprocessor.padding_of_text(prepended_cypher_txt)
        stego = STEGANOGRAPHY()
        option = 1
        stego.Steganography(option, filename, padded_cypher_txt, directory)
        print(f'filename is :: {filename}')
        return render_template('Decrypt.html', cypher_text=cypher_text, plain_text=real_plain_text, keys=keys,
                               passed=passed, filename1=filename, filename2='stego_'+filename)
    else:
        return redirect(request.url)


@app.route('/decrypts', methods=['POST'])
def decrypt_post():
    c = Crpytography()
    passed = False
    cypher_text = request.form.get("CYPHER_TEXT")
    keys = request.form.get("KEYS")
    flag = 0
    cypher_text, real_plain_text = c.Crpyto_Decryptor(cypher_text, keys, flag)
    return render_template('Decrypt.html', cypher_text=cypher_text, keys=keys, plain_text=real_plain_text, passed=passed)


@app.route('/decrypts1', methods=['POST'])
def decrypt_post1():
    c = Crpytography()
    passed = False
    cypher_text = request.form.get("CYPHER_TEXT")
    keys = request.form.get("KEYS")
    flag = 1
    cypher_text, real_plain_text = c.Crpyto_Decryptor(cypher_text, keys, flag)
    return render_template('Decrypt1.html', cypher_text=cypher_text, keys=keys, plain_text=real_plain_text)


@app.route('/decrypted_stego_image', methods=["POST"])
def decrypted_stego_image():
    c = Crpytography()
    stego = STEGANOGRAPHY()
    passed = False
    keys = request.form.get("KEYS")
    filename = request.form.get("FILENAME")
    filename = secure_filename(filename)
    print('@@@ filename: Got is :' + filename)

    option = 2
    c_text = ""
    directory = 'static/uploads/'
    cypher_text = stego.Steganography(option, filename, c_text, directory)

    flags = 1
    cypher_text, real_plain_text = c.Crpyto_Decryptor(cypher_text, keys, flags)
    return render_template('Stego.html', cypher_text=cypher_text, keys=keys, plain_text=real_plain_text, filename=filename)


@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' +filename), code=301)


@app.route('/team_info')
def team_info():
    return render_template('Team_Info.html')


if __name__ == "__main__":
    app.run(debug=True)
