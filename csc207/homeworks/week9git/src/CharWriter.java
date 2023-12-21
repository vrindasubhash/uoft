// DO NOT MODIFY THIS FILE
/**
 * This interface defines what it means to be able to write a character of output.
 * The details of where the output goes are left to the implementing class.
 */
public interface CharWriter {
    /**
     * Write a character to output.
     * @param c the character to write to output
     */
    void write(char c);
}
