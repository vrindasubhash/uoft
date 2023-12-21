import org.junit.Test;
import static org.junit.Assert.assertEquals;

/*
  Reminder: There are no hidden tests for this assignment.
 */
public class ReduceTest {

    // Note: you can comment out the tests in this file until you complete Task 3 if you want to run the other tests;
    //       just remember to uncomment it later!
    // See https://blog.jetbrains.com/idea/2022/04/comment-your-code-like-a-pro-with-intellij-idea/ if you aren't
    // sure how to quickly comment blocks of code.
    @Test(timeout = 500)
    public void testMain() {
        assertEquals("Reduce.main(100) is incorrect", 9, Reduce.main(100));
    }

    @Test(timeout = 500)
    public void testMainTwoHundred() {
        assertEquals("Reduce.main(200) is incorrect", 10, Reduce.main(200));
    }

    @Test(timeout = 500)
    public void testMainFortyTwo() {
        assertEquals("Reduce.main(42) is incorrect",8, Reduce.main(42));
    }

    @Test(timeout = 500)
    public void testOne() {
        assertEquals("Reduce.main(1) is incorrect", 1, Reduce.main(1));
    }

    @Test(timeout = 500)
    public void testTwo() {
        assertEquals("Reduce.main(2) is incorrect", 2, Reduce.main(2));
    }
}