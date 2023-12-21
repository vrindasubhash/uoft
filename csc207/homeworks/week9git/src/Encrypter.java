public class Encrypter {
    CharReader charReader;
    CharWriter charWriter;
    EncryptionAlgorithm encrypter;
    public Encrypter(CharReader charReader, CharWriter charWriter, EncryptionAlgorithm encrypter) {
        this.charReader = charReader;
        this.charWriter = charWriter;
        this.encrypter = encrypter;
    }

    public void encrypt() {
        while (this.charReader.hasNext()) {
            this.charWriter.write(this.encrypter.encrypt(this.charReader.next()));
        }
    }
}
