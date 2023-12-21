package use_case.save_preferences;

import entity.UserPreferences;

public class SavePreferencesInteractor implements SavePreferencesInputBoundary {
        final SavePreferencesDataAccessInterface saveDataAccessObject;
        final SavePreferencesOutputBoundary savePresenter;


    public SavePreferencesInteractor(SavePreferencesDataAccessInterface saveDataAccessObject,
                                     SavePreferencesOutputBoundary savePresenter){
        this.saveDataAccessObject = saveDataAccessObject;
        this.savePresenter = savePresenter;
    }

    /**
     * Saves the UserPreferences and passes it through as output data
     * @param savePreferencesInputData
     */
    @Override
    public void execute(SavePreferencesInputData savePreferencesInputData) {
        UserPreferences userPreferences = new UserPreferences(savePreferencesInputData.getNutrientRange(),
                savePreferencesInputData.getHealthPreferences(),
                savePreferencesInputData.getDishType());
        saveDataAccessObject.saveUserPreferences(savePreferencesInputData.getUsername(), userPreferences);
        SavePreferencesOutputData savePreferencesOutputData = new SavePreferencesOutputData(userPreferences);
        savePresenter.prepareSuccessView(savePreferencesOutputData);
    }

}
