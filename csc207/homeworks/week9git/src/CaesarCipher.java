public class CaesarCipher implements EncryptionAlgorithm {
    int shift = 0;
    public CaesarCipher(int shift) {
        this.shift = shift;
    }

    @Override
    public char encrypt(char c) {
        if ('a' <= c && c <= 'z')
            return (char) (((c + this.shift - 'a') % (26)) + 'a');
        return c;
    }

    @Override
    public char decrypt(char c) {
        if ('a' <= c && c <= 'z')
            return (char) (((c + (26 - this.shift) - 'a') % (26)) + 'a');
        return c;
    }
}
