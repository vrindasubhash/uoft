package app.custom_data;

import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class RangeTest {
    private Range<Integer> range;

    @Before
    public void init() throws Exception {
        range = new Range<>(6, 8);
    }

    @Test
    public void getLowerBound() {
        int expectedValue = 6;
        int actualValue = range.getLowerBound();
        assertEquals(expectedValue, actualValue);
    }

    @Test
    public void setLowerBound() {
        range.setLowerBound(7);
        int expectedValue = 7;
        int actualValue = range.getLowerBound();
        assertEquals(expectedValue, actualValue);
    }

    @Test
    public void getUpperBound() {
        int expectedValue = 8;
        int actualValue = range.getUpperBound();
        assertEquals(expectedValue, actualValue);
    }

    @Test
    public void setUpperBound() {
        range.setUpperBound(7);
        int expectedValue = 7;
        int actualValue = range.getUpperBound();
        assertEquals(expectedValue, actualValue);
    }

    @Test
    public void getRangeString() {
        String expectedValue = "6-8";
        String actualValue = range.getRangeString();
        assertEquals(expectedValue, actualValue);
    }
}