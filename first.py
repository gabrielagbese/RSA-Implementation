from email import message
import random
import binascii

first_hundred_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                    31, 37, 41, 43, 47, 53, 59, 61, 67,
                    71, 73, 79, 83, 89, 97, 101, 103,
                    107, 109, 113, 127, 131, 137, 139,
                    149, 151, 157, 163, 167, 173, 179,
                    181, 191, 193, 197, 199, 211, 223,
                    227, 229, 233, 239, 241, 251, 257,
                    263, 269, 271, 277, 281, 283, 293,
                    307, 311, 313, 317, 331, 337, 347,
                    349, 353, 359, 367, 373, 379, 383,
                    389, 397, 401, 409, 419, 421, 431,
                    433, 439, 443, 449, 457, 461, 463,
                    467, 479, 487, 491, 499, 503, 509,
                    521, 523, 541]

def getRandom(n):
    #n is for the number of bits
    return random.randrange(2**(n-1)+1, 2**n - 1)

def gcdExtended(a, b):

    # Base Case
    if a == 0 : 
        return b, 0, 1
            
    gcd, x1, y1 = gcdExtended(b%a, a)
    
    # Update x and y using results of recursive
    # call
    x = y1 - (b//a) * x1
    y = x1
    
    return gcd, x, y

def modinv(a, m):
    g, x, y = gcdExtended(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    

def getPrime(n):
    while True:
        # Obtain a random number
        prime_candidate = getRandom(n)
        # Test its divisibility by first 100 primes
        for divisor in first_hundred_primes:
            if prime_candidate % divisor == 0 and divisor**2 <= prime_candidate:
                break
        else: return prime_candidate

def isMillerRabinPassed(mrc):
    #mrc stands for miller-rabin candidate
    
    maxDivisionsByTwo = 0
    mrcminusone = mrc-1
    
    #find the number of divisions by two
    while mrcminusone % 2 == 0:
        mrcminusone >>= 1 #bitwise division by 2
        maxDivisionsByTwo += 1 #increment of the max number of divisions
        
    
    #assert(2**maxDivisionsByTwo * mrcminusone == mrc-1)

    def trialComposite(round_tester):
        #tests if our tester number raised to mcrminusone mod mrc is 1
        if pow(round_tester, mrcminusone, mrc) == 1:
            return False
        #next we perform the "a^2^1*d" test as many times as we have divisions by two
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * mrcminusone, mrc) == mrc-1:
                return False
        #if we get here, we have proven that the number is composite
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    
    for i in range(numberOfRabinTrials):
        #the round_tester is a random number between 2 and mrc
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            #returns false if the number is composite
            return False
    #if we get here, we have proven that the number is probably prime
    return True
def fast_modular_exponentiation(a, b, m):
    r = 1
    while b>0:
        if b&1==1: #bitwise AND ppeartion to check if the bit is 1
            r = r*a 
        a = (a*a)%m
        b = b>>1  #shift b by one bit to the right
    return r%m

def encrypt(message, e, n):
    #convert the message to a number
    message = int(binascii.hexlify(message.encode("utf-8")), 16)
    return fast_modular_exponentiation(message,e,n)

def decrypt(message, d, n):
    hex_decode = fast_modular_exponentiation(message,d,n)      
    #converts the decrypted number back to a string
    return binascii.unhexlify(hex(hex_decode)[2:]).decode("utf-8")
        
if __name__ == '__main__':
    while True:
        print("Generating keys...")
        #genrate random 1024-bit numbers that have a higher probability of being prime
        n = 1024
        p = getPrime(n)
        q = getPrime(n)
        #test if p and q are prime using Miller-Rabin
        while((isMillerRabinPassed(p) and isMillerRabinPassed(q)) == False):
            p = getPrime(n)
            q = getPrime(n)
        #print("p =", p ,"q =", q)
        
        #now we have our probably prime p and q
        n = p*q
        phi_n = (p-1)*(q-1)
        
        #pick e such that phi_n and e are coprime and e<phi_n
        e=65537
        
        #d is the modular inverse
        d = modinv(e, phi_n)
        
        message = input("Enter a message to encrypt: ")
        encrypted_message = encrypt(message, e, n)
        print("encrypted message =", encrypted_message)
        while input("Do You Want To Decrypt? [y/n]") == "y":
            decrypted_message = decrypt(encrypted_message, d, n)
            print("decrypted message =", decrypted_message)
        break