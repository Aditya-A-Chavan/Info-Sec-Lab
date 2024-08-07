import math

class ciphers():

    def vigenere_encrypt(self, text: str, keyword: str)-> str:
        encrypted_text = []
        keyword = list(keyword)

        if len(text) == len(keyword):
            keyword = keyword
        else:
            for i in range(len(text) - len(keyword)):
                keyword.append(keyword[i % len(keyword)])

        keyword_final = "".join(keyword)

        for i in range(len(text)):
            char = text[i]
            if char.isupper():
                encrypted_char = chr((ord(char) + ord(keyword_final[i].upper()) - 2 * ord('A')) % 26 + ord('A'))
            elif char.islower():
                encrypted_char = chr((ord(char) + ord(keyword_final[i].lower()) - 2 * ord('a')) % 26 + ord('a'))
            else:
                encrypted_char = char
            encrypted_text.append(encrypted_char)

        return "".join(encrypted_text)

    def caesar_encrypt(self, text, shift):
        encrypted_text = ""
        for char in text:
            if char.isupper():
                encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
            elif char.islower():
                encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
            else:
                encrypted_text += char
        return encrypted_text
    
    def affine_encrypt(self, text: str, a: int, b: int) -> str:
        encrypted_text = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    encrypted_text += chr((a * (ord(char) - ord('A')) + b) % 26 + ord('A'))
                else:
                    encrypted_text += chr((a * (ord(char) - ord('a')) + b) % 26 + ord('a'))
            else:
                encrypted_text += char
        return encrypted_text
    
    def caesar_decrypt(self, encrypted_text, shift):
        return self.caesar_encrypt(encrypted_text, -shift)

    def vigenere_decrypt(self, encrypted_text, keyword):
        decrypted_text = []
        keyword = list(keyword)
        if len(encrypted_text) == len(keyword):
            keyword = keyword
        else:
            for i in range(len(encrypted_text) - len(keyword)):
                keyword.append(keyword[i % len(keyword)])
        
        keyword_final = "".join(keyword)

        for i in range(len(encrypted_text)):
            char = encrypted_text[i]
            if char.isupper():
                decrypted_char = chr((ord(char) - ord(keyword_final[i].upper()) + 26) % 26 + ord('A'))
            elif char.islower():
                decrypted_char = chr((ord(char) - ord(keyword_final[i].lower()) + 26) % 26 + ord('a'))
            else:
                decrypted_char = char
            decrypted_text.append(decrypted_char)
        
        return "".join(decrypted_text)

    def affine_decrypt(self, encrypted_text: str, a: int, b: int) -> str:
        decrypted_text = ""
        a_inverse = self.mod_inverse(a, 26)
        for char in encrypted_text:
            if char.isalpha():
                if char.isupper():
                    decrypted_text += chr((a_inverse * (ord(char) - ord('A') - b)) % 26 + ord('A'))
                else:
                    decrypted_text += chr((a_inverse * (ord(char) - ord('a') - b)) % 26 + ord('a'))
            else:
                decrypted_text += char
        return decrypted_text

    def mod_inverse(self, a: int, m: int) -> int:
        for i in range(1, m):
            if (a * i) % m == 1:
                return i
        return None

def main():
    cipher = ciphers()
    while True:
        print("\nChoose a cipher:")
        print("1. Vigenère Cipher")
        print("2. Caesar Cipher")
        print("3. Affine Cipher")
        print("4. Exit")
        
        user_input = input("Enter choice (1-4): ")

        if user_input == '4':
            print("Exiting program. Goodbye!")
            break

        text = input("Enter text to cipher: ")

        if user_input == '1':
            keyword = input("Enter keyword: ")
            encrypted_text = cipher.vigenere_encrypt(text, keyword)
            print("Encrypted:", encrypted_text)
            print("Decrypted:", cipher.vigenere_decrypt(encrypted_text, keyword))

        elif user_input == '2':
            shift = int(input("Enter shift: "))
            encrypted_text = cipher.caesar_encrypt(text, shift)
            print("Encrypted:", encrypted_text)
            print("Decrypted:", cipher.caesar_decrypt(encrypted_text, shift))

            a = int(input("Enter value of a: "))
            b = int(input("Enter valye of b: "))
            if math.gcd(a, 26) != 1:
                print("Error: 'a' must be coprime with 26")
                continue
            encrypted_text = cipher.affine_encrypt(text, a, b)
            print("Encrypted:", encrypted_text)
            print("Decrypted:", cipher.affine_decrypt(encrypted_text, a, b))

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()