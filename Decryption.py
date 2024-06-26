from preprocessing import Preprocessing

class Decryption(Preprocessing):
    def Decrypt(self, C_Is, KEYS):
        # FIRST HALF #tuples of Key and C_Is cipher text each of 32 bits are passed
        CI1, CI2, CI3, CI4 = C_Is
        K1, K2, K3, K4 = KEYS

        CI2 = self.xor_32bits(CI2, CI1)
        CI4 = self.xor_32bits(CI4, CI3)
        CI1 = self.anti_clockwise_CircularShift(CI1, 2)
        CI3 = self.anti_clockwise_CircularShift(CI3, 2)
        CI1 = self.xor_32bits(CI1, CI2)
        CI3 = self.xor_32bits(CI4, CI3)
        CI2 = self.clockwise_CircularShift(CI2, 2)
        CI4 = self.clockwise_CircularShift(CI4, 2)

        # SECOND HALF
        CI3 = self.xor_32bits(K4, CI3)
        CI4 = self.xor_32bits(CI4, K2)
        CI3 = self.anti_clockwise_CircularShift(CI3, 2)
        CI4 = self.anti_clockwise_CircularShift(CI4, 2)
        CI4 = self.xor_32bits(CI2, CI4)
        CI3 = self.xor_32bits(CI1, CI3)

        CI2 = self.clockwise_CircularShift(CI2, 2)
        CI1 = self.clockwise_CircularShift(CI1, 2)

        EI1 = CI2
        EI2 = CI1
        EI3 = CI4
        EI4 = CI3

        return (EI1, EI2, EI3, EI4)
