package entity;

import app.custom_data.Range;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import static org.junit.Assert.*;

public class CommonUserTest {
    User user;

    @Before
    public void setUp() throws Exception {
        NutrientRange nutrientRange = new NutrientRange(
                new Range<>(0, 2000),
                new Range<>(0, 100),
                new Range<>(0, 150),
                new Range<>(0, 500)
        );
        UserPreferences userPreferences = new UserPreferences(
                nutrientRange,
                new ArrayList<>(Arrays.asList("test0", "test1")),
                new ArrayList<>(Arrays.asList("test2", "test3"))
        );
        user = new CommonUser("test_username", "test_password", userPreferences);
    }

    @Test
    public void getUsername() {
        assertEquals("test_username", user.getUsername());
    }

    @Test
    public void getPassword() {
        assertEquals("test_password", user.getPassword());
    }

    @Test
    public void getUserPreferences() {
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
        assertArrayEquals(new int[]{0, 2000}, new int[]{calRange.getLowerBound(), calRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 100}, new int[]{fatRange.getLowerBound(), fatRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 150}, new int[]{proteinRange.getLowerBound(), proteinRange.getUpperBound()});
        assertArrayEquals(new int[]{0, 500}, new int[]{carbRange.getLowerBound(), carbRange.getUpperBound()});
    }

    @Test
    public void setUsername() {
        user.setUsername("test_username_1");
        assertEquals("test_username_1", user.getUsername());
    }

    @Test
    public void setPassword() {
        user.setPassword("test_password_1");
        assertEquals("test_password_1", user.getPassword());
    }

    @Test
    public void setUserPreferences() {
        NutrientRange nutrientRange = new NutrientRange(
                new Range<>(0, 1),
                new Range<>(0, 2),
                new Range<>(0, 3),
                new Range<>(0, 4)
        );
        UserPreferences userPreferences =  new UserPreferences(nutrientRange, new ArrayList<>(), new ArrayList<>());
        user.setUserPreferences(userPreferences);
        assertEquals(userPreferences, user.getUserPreferences());
    }
}