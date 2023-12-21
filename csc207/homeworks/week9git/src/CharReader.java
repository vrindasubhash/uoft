// DO NOT MODIFY THIS FILE
/**
 * This interface defines what it means to be able to read a character of input.
 * The details of where the input comes from are left to the implementing class.
 */
public interface CharReader {

    /**
     *
     * @return whether this reader has a next character or not
     */
    boolean hasNext();

    /**
     * Return the next character from this reader.
     * Note: The behaviour is unspecified if there is no next character.
     * @return the next character from this reader
     */
    char next();
}
