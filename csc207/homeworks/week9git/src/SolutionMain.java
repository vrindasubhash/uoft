// DO NOT MODIFY THIS FILE
public class SolutionMain {

    // TODO Using the supplied interfaces and existing code, implement any code required in order
    //      for the below code to run correctly.
    //      Note: Do NOT modify any of the code in this file nor any of the provided files;
    //            you should define any required classes in other files.
    //      Note: There will be additional tests made available later, but if you get this code working, then
    //            you should pass the tests.
    //      Hint: think about the various design patterns we have learned about.

    /**
     * This code will try all possible shifts of the Caesar cipher to decrypt the message hidden in message.txt.
     */
    public static void main(String[] args) {
        for(int shift=0; shift< 26; shift++) {
            System.out.print(shift + " ... ");
            Encrypter encrypter = new Encrypter(new FileCharReader("message.txt"),
                                                new ConsoleCharWriter(), new CaesarCipher(shift));
            encrypter.encrypt();
        }
    }
}
