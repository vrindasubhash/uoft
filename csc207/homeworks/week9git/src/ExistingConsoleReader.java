// DO NOT MODIFY THIS FILE
import java.util.*;

/**
 * This class will wait for user input from the console when it runs out of stored characters.
 * <p>
 * If the user types "quit", then its hasNext() method will return false.
 */
public class ExistingConsoleReader {

    private final List<Character> characters;
    private final Scanner scan;

    /**
     * Initialize this console character reader.
     */
    public ExistingConsoleReader()
    {
        characters = new ArrayList<>();
        scan = new Scanner(System.in);
    }

    public boolean hasNext() {

        if (characters.isEmpty()) {
            String word = scan.nextLine();
            if (word.equals("quit"))
                return false;
            for (char c : word.toCharArray()){
                characters.add(c);
            }
            characters.add('\n'); // add a newline to the end
        }

        return true;
    }

    public char next() {
        if (!hasNext()) {
            throw new NoSuchElementException();
        }
        return characters.remove(0);
    }
}
