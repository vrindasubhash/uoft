public class Reduce {

    public static int main() {
       return main(100);
    }

    public static int main(int n) {
        int i = n;
        int steps = 0;
        while (i > 0) {
            boolean isEven = i % 2 == 0;
            if (isEven) {
                i = i / 2;
            }
            else {
                i = i -1;
            }
            steps++;
        }
        return steps;
    }
}
