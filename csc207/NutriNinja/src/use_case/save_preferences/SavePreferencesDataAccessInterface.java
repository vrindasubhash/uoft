package use_case.save_preferences;

import entity.UserPreferences;

public interface SavePreferencesDataAccessInterface {
    void saveUserPreferences(String username, UserPreferences preferences);
}
