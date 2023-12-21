package entity;

import app.custom_data.Range;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class UserPreferencesTest {
    UserPreferences userPreferences;

    @Before
    public void setUp() throws Exception {
        NutrientRange nutrientRange = new NutrientRange(
                new Range<>(0, 2000),
                new Range<>(0, 100),
                new Range<>(0, 150),
                new Range<>(0, 500)
        );
        userPreferences = new UserPreferences(
                nutrientRange,
                new ArrayList<>(Arrays.asList("test0", "test1")),
                new ArrayList<>(Arrays.asList("test2", "test3"))
        );
    }

    @Test
    public void getNutrientRange() {
        NutrientRange nutrientRange = userPreferences.getNutrientRange();
        Range<Integer> calRange = nutrientRange.getCalorieRange();
        Range<Integer> fatRange = nutrientRange.getFatRange();
        Range<Integer> proteinRange = nutrientRange.getProteinRange();
        Range<Integer> carbRange = nutrientRange.getCarbRange();

        assertArrayEquals(new int[]{0, 2000}, new int[]{calRange.getLowerBound(), calRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 100}, new int[]{fatRange.getLowerBound(), fatRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 150}, new int[]{proteinRange.getLowerBound(), proteinRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 500}, new int[]{carbRange.getLowerBound(), carbRange.getUpperBound()});
    }

    @Test
    public void setNutrientRange() {
        NutrientRange nutrientRange = new NutrientRange(
                new Range<>(0, 1),
                new Range<>(0, 2),
                new Range<>(0, 3),
                new Range<>(0, 4)
        );
        userPreferences.setNutrientRange(nutrientRange);
        assertEquals(nutrientRange, userPreferences.getNutrientRange());
    }

    @Test
    public void getHealthPreferences() {
        List<String> expected = new ArrayList<>(Arrays.asList("test0", "test1"));
        List<String> actual = userPreferences.getHealthPreferences();
        assertEquals(expected, actual);
    }

    @Test
    public void setHealthPreferences() {
        List<String> diff = new ArrayList<>();
        userPreferences.setHealthPreferences(diff);
        assertEquals(diff, userPreferences.getHealthPreferences());
    }

    @Test
    public void getDishType() {
        List<String> expected = new ArrayList<>(Arrays.asList("test2", "test3"));
        List<String> actual = userPreferences.getDishType();
        assertEquals(expected, actual);
    }

    @Test
    public void setDishType() {
        List<String> diff = new ArrayList<>();
        userPreferences.setDishType(diff);
        assertEquals(diff, userPreferences.getDishType());
    }
}