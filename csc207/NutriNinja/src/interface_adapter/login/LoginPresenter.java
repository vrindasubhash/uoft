package interface_adapter.login;

import interface_adapter.ViewManagerModel;
import interface_adapter.save_preferences.SavePreferencesState;
import interface_adapter.save_preferences.SavePreferencesViewModel;
import use_case.login.LoginOutputBoundary;
import use_case.login.LoginOutputData;

public class LoginPresenter implements LoginOutputBoundary {

    private final LoginViewModel loginViewModel;
    private final SavePreferencesViewModel savePreferencesViewModel;
    private ViewManagerModel viewManagerModel;

    public LoginPresenter(ViewManagerModel viewManagerModel, SavePreferencesViewModel savePreferencesViewModel,
                          LoginViewModel loginViewModel) {
        this.viewManagerModel = viewManagerModel;
        this.savePreferencesViewModel = savePreferencesViewModel;
        this.loginViewModel = loginViewModel;
    }

    /**
     * Creates the success view (save preferences) if the login was successful.
     * @param response
     */
    @Override
    public void prepareSuccessView(LoginOutputData response) {
        // On success, switch to the save preferences view.
        SavePreferencesState savePreferencesState = savePreferencesViewModel.getState();
        savePreferencesState.setUsername(response.getUsername());
        savePreferencesState.setNutrientRange(response.getUserPreferences().getNutrientRange());
        savePreferencesState.setHealthPreferences(response.getUserPreferences().getHealthPreferences());
        savePreferencesState.setDishType(response.getUserPreferences().getDishType());
        this.savePreferencesViewModel.setState(savePreferencesState);
        this.savePreferencesViewModel.firePropertyChanged();

        this.viewManagerModel.setActiveView(savePreferencesViewModel.getViewName());
        this.viewManagerModel.firePropertyChanged();
    }

    /**
     * Creates the fail view if the login fails.
     * @param error
     */
    @Override
    public void prepareFailView(String error) {
        loginViewModel.getState().setError(error);
        loginViewModel.firePropertyChanged();
    }
}
