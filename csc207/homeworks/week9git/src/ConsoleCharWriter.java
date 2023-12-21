public class ConsoleCharWriter implements CharWriter {
    ExistingConsoleWriter consoleWriter = new ExistingConsoleWriter();
    @Override
    public void write(char c) {
        this.consoleWriter.write(c);
    }
}
