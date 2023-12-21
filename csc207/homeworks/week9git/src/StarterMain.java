// DO NOT MODIFY THIS FILE
// TODO take the logic of the encrypt and decrypt methods from this class and put them in an appropriate
//      class.
//      Note: you do NOT need to modify this file; it is just to give you a sense of what the "before" code
//            looks like — before the code is generalized to work as is seen in SolutionMain.java.
public class StarterMain {

    /**
     * Demo usage of the program before we apply any refactoring to incorporate design patterns.
     * <p>
     * This code reads from standard input and writes the encrypted version of the input each time the user
     * presses Enter.
     * <p>
     * To quit, the user can type "quit" and then press Enter.
     *
     * @param args these are the commandline arguments and are not used by this main method
     */
    public static void main(String[] args) {
        System.out.println("Type a string and then press Enter to encrypt the string (type 'quit' to quit)");
        ExistingConsoleReader reader = new ExistingConsoleReader();
        ExistingConsoleWriter writer = new ExistingConsoleWriter();

        while(reader.hasNext()){
            writer.write(encrypt(reader.next()));
        }

    }

    /**
     * Encrypt the character using a Caesar cipher, with a shift of 5.
     * <p>
     *
     * You can see a description of the encryption algorithm on
     * <a href="https://en.wikipedia.org/wiki/Caesar_cipher">Wikipedia</a>
     *
     *
     * @param c the character to encrypt
     * @return the encrypted character if it is a lowercase letter [a-z], otherwise the original character
     */
    private static char encrypt(char c) {
        if ('a' <= c && c <= 'z')
            return (char) (((c + 5 - 'a') % (26)) + 'a');
        return c;
    }

    /**
     * Decrypt the character using a Caesar cipher, with a shift of 5.
     *
     * Note: since the original shift was 5, we apply a shift of 21 (26 - 5) to decrypt.
     *
     * @param c the character to decrypt
     * @return the decrypted character if it is a lowercase letter [a-z], otherwise the original character
     */
    private static char decrypt(char c) {
        if ('a' <= c && c <= 'z')
            return (char) (((c + 21 - 'a') % (26)) + 'a');
        return c;
    }

}
