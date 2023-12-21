package interface_adapter.signup;

import interface_adapter.ViewManagerModel;
import interface_adapter.login.LoginState;
import use_case.signup.SignupOutputBoundary;
import use_case.signup.SignupOutputData;
import interface_adapter.login.LoginViewModel;

public class    SignupPresenter implements SignupOutputBoundary {
    private final SignupViewModel signupViewModel;
    private final LoginViewModel loginViewModel;
    private ViewManagerModel viewManagerModel;

    public SignupPresenter(ViewManagerModel viewManagerModel, SignupViewModel signupViewModel, LoginViewModel loginViewModel) {
        this.viewManagerModel = viewManagerModel;
        this.signupViewModel = signupViewModel;
        this.loginViewModel = loginViewModel;
    }

    public void prepareSuccessView(SignupOutputData response) {
        LoginState loginState = this.loginViewModel.getState();
        loginState.setUsername(response.getUsername());
        this.loginViewModel.setState(loginState);
        this.loginViewModel.firePropertyChanged();
        this.viewManagerModel.setActiveView(this.loginViewModel.getViewName());
        this.viewManagerModel.firePropertyChanged();
    }

    public void prepareFailView(String error) {
        SignupState signupState = this.signupViewModel.getState();
        signupState.setUsernameError(error);
        this.signupViewModel.firePropertyChanged();
    }
}

