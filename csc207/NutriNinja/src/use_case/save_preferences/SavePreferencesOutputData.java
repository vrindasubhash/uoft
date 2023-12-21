package use_case.save_preferences;

import entity.UserPreferences;

public class SavePreferencesOutputData {
    private final String message;
    private UserPreferences userPreferences;
    public SavePreferencesOutputData(UserPreferences userPreferences){
        this.message = "Preferences Saved!";
        this.userPreferences = userPreferences;
    }
    public String getMessage(){
        return this.message;
    }
    public UserPreferences getUserPreferences(){return this.userPreferences;}
}
