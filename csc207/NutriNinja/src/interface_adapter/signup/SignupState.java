package interface_adapter.signup;

public class SignupState {
    private String username = "";
    private String usernameError = null;
    private String password = "";
    private String passwordError = null;
    private String repeatPassword = "";
    private String repeatPasswordError = null;

    public SignupState(SignupState copy) {
        this.username = copy.username;
        this.usernameError = copy.usernameError;
        this.password = copy.password;
        this.passwordError = copy.passwordError;
        this.repeatPassword = copy.repeatPassword;
        this.repeatPasswordError = copy.repeatPasswordError;
    }

    public SignupState() {
    }

    public String getUsername() {
        return this.username;
    }

    public String getUsernameError() {
        return this.usernameError;
    }

    public String getPassword() {
        return this.password;
    }

    public String getPasswordError() {
        return this.passwordError;
    }

    public String getRepeatPassword() {
        return this.repeatPassword;
    }

    public String getRepeatPasswordError() {
        return this.repeatPasswordError;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setUsernameError(String usernameError) {
        this.usernameError = usernameError;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setPasswordError(String passwordError) {
        this.passwordError = passwordError;
    }

    public void setRepeatPassword(String repeatPassword) {
        this.repeatPassword = repeatPassword;
    }

    public void setRepeatPasswordError(String repeatPasswordError) {
        this.repeatPasswordError = repeatPasswordError;
    }

    public String toString() {
        return "SignupState{username='" + this.username + "', password='" + this.password + "', repeatPassword='" + this.repeatPassword + "'}";
    }
}
