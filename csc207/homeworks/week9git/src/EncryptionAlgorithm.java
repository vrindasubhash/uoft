// DO NOT MODIFY THIS FILE
/**
 * An encryption algorithm consists of an encrypt and a decrypt method, which can be used to
 * encrypt and decrypt characters.
 */
public interface EncryptionAlgorithm {

    /**
     * Encrypt the character using the encryption algorithm.
     * @param c the character to encrypt
     * @return the decrypted character if it is a lowercase letter [a-z], otherwise the original character
     */
    char encrypt(char c);

    /**
     * Decrypt the character using the inverse of the encryption algorithm.
     * @param c the character to decrypt
     * @return the decrypted character if it is a lowercase letter [a-z], otherwise the original character
     */
    char decrypt(char c);
}
