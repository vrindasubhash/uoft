package entity;

import java.util.Arrays;
import java.util.List;

public interface UserFactory {
    /**
     * Creates a user object
     * @param username of user
     * @param password of user
     * @param healthPreference of user
     * @param dishType preference of user
     * @param calRange where index 0 is the lower bound and index 1 is the upper bound
     * @param fatRange where index 0 is the lower bound and index 1 is the upper bound
     * @param proteinRange where index 0 is the lower bound and index 1 is the upper bound
     * @param carbRange where index 0 is the lower bound and index 1 is the upper bound
     * @return the user created
     */
    User create(
            String username,
            String password,
            List<String> healthPreference,
            List<String> dishType,
            int[] calRange,
            int[] fatRange,
            int[] proteinRange,
            int[] carbRange
    );

    /**
     * Creates a new user. Intended for creating users with default preferences on sign up.
     * @param username of user
     * @param password of user
     * @return the user
     */
    User create(String username, String password);
}
