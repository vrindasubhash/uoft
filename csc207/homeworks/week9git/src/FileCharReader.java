public class FileCharReader implements CharReader {
    ExistingFileReader fileReader;
    public FileCharReader(String file) {
        this.fileReader = new ExistingFileReader(file);
    }

    @Override
    public boolean hasNext() {
        return this.fileReader.hasNext();
    }

    @Override
    public char next() {
        return this.fileReader.next();
    }
}
