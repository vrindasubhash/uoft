import org.junit.Test;
import static org.junit.Assert.assertEquals;

/*
  Reminder: There are no hidden tests for this assignment.
 */
public class MultiplesTest {

    @Test(timeout = 500)
    public void testThousand() {
        assertEquals("Multiples.main(1000, 3, 5) is incorrect.",466, Multiples.main(1000, 3, 5));
    }

    @Test(timeout = 500)
    public void testEquals() {
        assertEquals("Multiples.main(1000, 4, 4) is incorrect.",249, Multiples.main(1000, 4, 4));
    }

    @Test(timeout = 500)
    public void testFifteen() {
        assertEquals("Multiples.main(16, 3, 5) is incorrect, the values" +
                " it should be counting are: 3, 5, 6, 9, 10, 12, 15",7, Multiples.main(16, 3, 5));
    }

    @Test(timeout = 500)
    public void testTen() {
        assertEquals("Multiples.main(10, 3, 5) is incorrect, the values" +
                " it should be counting are: 3, 5, 6, 9",4, Multiples.main(10, 3, 5));
    }

}