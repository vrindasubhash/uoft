public class Multiples {

    public static int main() {
        return main(1000,3,5);
    }

    public static int main(int n, int a, int b) {
        int i = 1;
        int count = 0;
        while (i < n) {
            boolean divisibleBya = i % a == 0;
            boolean divisibleByb = i % b == 0;
            if (divisibleBya || divisibleByb) {
                count ++;
            }
            i++;
        }
        return count;
    }
}
