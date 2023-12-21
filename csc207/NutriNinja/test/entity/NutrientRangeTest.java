package entity;

import app.custom_data.Range;
import org.junit.Before;
import org.junit.Test;

import static org.junit.Assert.*;

public class NutrientRangeTest {
    NutrientRange nutrientRange;

    @Before
    public void setUp() throws Exception {
        nutrientRange = new NutrientRange(
                new Range<>(10, 20),
                new Range<>(30, 40),
                new Range<>(50, 60),
                new Range<>(70, 80)
        );
    }


    @Test
    public void getCalorieRange() {
        int[] expectedValues = new int[]{10, 20};
        int[] actualValues = new int[]{
                nutrientRange.getCalorieRange().getLowerBound(),
                nutrientRange.getCalorieRange().getUpperBound()
        };
        assertArrayEquals(expectedValues, actualValues);
    }

    @Test
    public void setCalorieRange() {
        Range<Integer> calRange = new Range<>(100, 200);
        nutrientRange.setCalorieRange(calRange);
        assertEquals(calRange, nutrientRange.getCalorieRange());
    }

    @Test
    public void getFatRange() {
        int[] expectedValues = new int[]{30, 40};
        int[] actualValues = new int[]{
                nutrientRange.getFatRange().getLowerBound(),
                nutrientRange.getFatRange().getUpperBound()
        };
        assertArrayEquals(expectedValues, actualValues);
    }

    @Test
    public void setFatRange() {
        Range<Integer> fatRange = new Range<>(300, 400);
        nutrientRange.setFatRange(fatRange);
        assertEquals(fatRange, nutrientRange.getFatRange());
    }

    @Test
    public void getProteinRange() {
        int[] expectedValues = new int[]{50, 60};
        int[] actualValues = new int[]{
                nutrientRange.getProteinRange().getLowerBound(),
                nutrientRange.getProteinRange().getUpperBound()
        };
        assertArrayEquals(expectedValues, actualValues);
    }

    @Test
    public void setProteinRange() {
        Range<Integer> proteinRange = new Range<>(500, 600);
        nutrientRange.setProteinRange(proteinRange);
        assertEquals(proteinRange, nutrientRange.getProteinRange());
    }

    @Test
    public void getCarbRange() {
        int[] expectedValues = new int[]{70, 80};
        int[] actualValues = new int[]{
                nutrientRange.getCarbRange().getLowerBound(),
                nutrientRange.getCarbRange().getUpperBound()
        };
        assertArrayEquals(expectedValues, actualValues);
    }

    @Test
    public void setCarbRange() {
        Range<Integer> carbRange = new Range<>(700, 800);
        nutrientRange.setCarbRange(carbRange);
        assertEquals(carbRange, nutrientRange.getCarbRange());
    }
}