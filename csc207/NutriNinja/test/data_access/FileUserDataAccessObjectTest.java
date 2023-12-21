package data_access;

import entity.CommonUserFactory;
import entity.User;
import entity.UserFactory;
import entity.UserPreferences;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.*;

public class FileUserDataAccessObjectTest {
    FileUserDataAccessObject testDao;
    UserFactory userFactory = new CommonUserFactory();

    @Before
    public void setUp() throws Exception {
        testDao = new FileUserDataAccessObject("test_dao.csv", userFactory);
        User testUser = userFactory.create("test_username", "test_password");
        testDao.saveUser(testUser);
    }

    @After
    public void tearDown() {
        File testData = new File("test_dao.csv");
        if (testData.delete()) {
            System.out.println("Deleted test_data.csv successfully.");
        } else {
            System.out.println("Deleted test_data.csv unsuccessfully.");
        }
    }

    @Test
    public void saveUser() throws IOException {
        User newUser = userFactory.create("new_user", "new_password");
        testDao.saveUser(newUser);

        // Creating a new dao to confirm user is successfully saved
        FileUserDataAccessObject testDao2 = new FileUserDataAccessObject("test_dao.csv", userFactory);
        User testNewUser = testDao2.getUser("new_user");
        assertEquals("new_user", testNewUser.getUsername());
        assertEquals("new_password", testNewUser.getPassword());
    }

    @Test
    public void saveUserPreferences() throws IOException {
        User user = testDao.getUser("test_username");
        UserPreferences userPreferences = user.getUserPreferences();

        // Modifying user preferences
        List<String> newHealthPref = new ArrayList<>(List.of("h1", "h2", "h3"));
        userPreferences.setHealthPreferences(newHealthPref);
        userPreferences.getNutrientRange().getCalorieRange().setUpperBound(1000);

        testDao.saveUserPreferences("test_username", userPreferences);

        // Creating a new dao to confirm user preference is successfully saved
        FileUserDataAccessObject testDao2 = new FileUserDataAccessObject("test_dao.csv", userFactory);
        UserPreferences newPreferences = testDao2.getUser("test_username").getUserPreferences();

        assertEquals(newHealthPref, newPreferences.getHealthPreferences());
        int actualUpperBound = newPreferences.getNutrientRange().getCalorieRange().getUpperBound();
        assertEquals(1000, actualUpperBound);
    }

    @Test
    public void userExists() {
        assertTrue(testDao.userExists("test_username"));
        assertFalse(testDao.userExists("user_does_not_exist"));
    }

    @Test
    public void getUser() {
        User user = testDao.getUser("test_username");
        assertEquals("test_username", user.getUsername());
        assertEquals("test_password", user.getPassword());
    }
}