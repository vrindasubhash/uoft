

import org.junit.Test;
import static org.junit.Assert.assertEquals;

/*
  Reminder: There are no hidden tests for this assignment.
 */
public class MultiplesDefaultTest {

    // Note: you can comment out this test until you complete Task 2 if you want to run the other tests;
    //       just remember to uncomment it later!
    // See https://blog.jetbrains.com/idea/2022/04/comment-your-code-like-a-pro-with-intellij-idea/ if you aren't
    // sure how to quickly comment blocks of code.
    @Test(timeout = 500)
    public void testDefault() {
        assertEquals("Multiples.main() is incorrect for default values", 466, Multiples.main());
    }

}