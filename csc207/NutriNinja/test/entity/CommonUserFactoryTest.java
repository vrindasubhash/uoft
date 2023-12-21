package entity;

import app.custom_data.Range;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class CommonUserFactoryTest {
    UserFactory userFactory = new CommonUserFactory();

    @Test
    public void create() {
        List<String> healthPreferences = new ArrayList<>(Arrays.asList("test0", "test1"));
        List<String> dishType = new ArrayList<>(Arrays.asList("test2", "test3"));

        User user = userFactory.create("test_username", "test_password",
                healthPreferences, dishType,
                new int[]{0, 1}, new int[]{2, 3},
                new int[]{4, 5}, new int[]{6, 7}
        );

        assertEquals("test_username", user.getUsername());
        assertEquals("test_password", user.getPassword());

        UserPreferences userPreferences = user.getUserPreferences();
        List<String> expectedHealthPreferences = new ArrayList<>(Arrays.asList("test0", "test1"));
        List<String> expectedDishType = new ArrayList<>(Arrays.asList("test2", "test3"));
        assertEquals(expectedHealthPreferences, userPreferences.getHealthPreferences());
        assertEquals(expectedDishType, userPreferences.getDishType());

        NutrientRange nutrientRange = user.getUserPreferences().getNutrientRange();
        Range<Integer> calRange = nutrientRange.getCalorieRange();
        Range<Integer> fatRange = nutrientRange.getFatRange();
        Range<Integer> proteinRange = nutrientRange.getProteinRange();
        Range<Integer> carbRange = nutrientRange.getCarbRange();
        assertArrayEquals(new int[]{0, 1}, new int[]{calRange.getLowerBound(), calRange.getUpperBound()});
        assertArrayEquals(new int[]{2, 3}, new int[]{fatRange.getLowerBound(), fatRange.getUpperBound()});
        assertArrayEquals(new int[]{4, 5}, new int[]{proteinRange.getLowerBound(), proteinRange.getUpperBound()});
        assertArrayEquals(new int[]{6, 7}, new int[]{carbRange.getLowerBound(), carbRange.getUpperBound()});
    }

    @Test
    public void createDefault() {
        User user = userFactory.create("test_username", "test_password");

        assertEquals("test_username", user.getUsername());
        assertEquals("test_password", user.getPassword());

        UserPreferences userPreferences = user.getUserPreferences();
        List<String> emptyList = new ArrayList<>();
        assertEquals(emptyList, userPreferences.getHealthPreferences());
        assertEquals(emptyList, userPreferences.getDishType());

        NutrientRange nutrientRange = user.getUserPreferences().getNutrientRange();
        Range<Integer> calRange = nutrientRange.getCalorieRange();
        Range<Integer> fatRange = nutrientRange.getFatRange();
        Range<Integer> proteinRange = nutrientRange.getProteinRange();
        Range<Integer> carbRange = nutrientRange.getCarbRange();
        assertArrayEquals(new int[]{0, 2000}, new int[]{calRange.getLowerBound(), calRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 100}, new int[]{fatRange.getLowerBound(), fatRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 150}, new int[]{proteinRange.getLowerBound(), proteinRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 500}, new int[]{carbRange.getLowerBound(), carbRange.getUpperBound()});
    }
}