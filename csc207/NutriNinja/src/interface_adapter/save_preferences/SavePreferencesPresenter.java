package interface_adapter.save_preferences;

import interface_adapter.ViewManagerModel;
import use_case.save_preferences.SavePreferencesOutputBoundary;
import use_case.save_preferences.SavePreferencesOutputData;

public class SavePreferencesPresenter implements SavePreferencesOutputBoundary {
    private final SavePreferencesViewModel saveViewModel;
    private ViewManagerModel viewManagerModel;


    public SavePreferencesPresenter(SavePreferencesViewModel saveViewModel, ViewManagerModel viewManagerModel){

        this.saveViewModel = saveViewModel;
        this.viewManagerModel = viewManagerModel;
    }

    /**
     * Receives the SavePreferenecesOutputData Updates the ViewModel
     * @param response
     */
    @Override
    public void prepareSuccessView(SavePreferencesOutputData response) {
        // On success, present the user with the success message

        SavePreferencesState saveState = saveViewModel.getState();
        saveState.setDishType(response.getUserPreferences().getDishType());
        saveState.setHealthPreferences(response.getUserPreferences().getHealthPreferences());
        saveState.setNutrientRange(response.getUserPreferences().getNutrientRange());
        this.saveViewModel.setState(saveState);
        this.saveViewModel.firePropertyChanged();

        this.viewManagerModel.setActiveView(saveViewModel.getViewName());
        this.viewManagerModel.firePropertyChanged();
    }
}

