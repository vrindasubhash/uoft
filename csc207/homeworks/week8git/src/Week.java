// TODO: Task 1 make Week iterable
import java.util.Iterator;
import java.util.NoSuchElementException;

public class Week implements Iterable<String>  {
    private final String[] days = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};


    public String getDay(int i) {
        return days[i];
    }

    /**
     * Sample usage of the Week class. See WeekTest.java for the tests.
     */
    public static void main(String[] args) {
        Week week = new Week();

        for (String day: week) {
            System.out.println(day);
        }

//        for (int i = 0; i != 7; i++) {
//            System.out.println(week.getDay(i));
//        }
    }

    @Override
    public Iterator<String> iterator() {
        return new iter();
    }

    public class iter implements Iterator<String> {
        private int index = 0;
        @Override
        public boolean hasNext() {
            return index < days.length;
        }

        @Override
        public String next() {
            if (hasNext()) {
                return days[index++];
            }
            throw new NoSuchElementException();
        }
    }

}
