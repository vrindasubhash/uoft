package interface_adapter.clear_users;

import use_case.clear_users.ClearUserDataAccessInterface;
import use_case.signup.SignupInputBoundary;
import use_case.signup.SignupInputData;

import javax.swing.*;
import java.util.Set;

// TODO Complete me
public class ClearController {

    private final ClearUserDataAccessInterface clearUserDataAccessInterface;

    public ClearController(ClearUserDataAccessInterface clearUserDataAccessInterface) {
        this.clearUserDataAccessInterface = clearUserDataAccessInterface;
    }
    public void execute() {
        Set<String> users = this.clearUserDataAccessInterface.clear();
        StringBuilder stringBuilder = new StringBuilder();
        for (String user : users) {
            stringBuilder.append(user).append("\n");
        }
        String result = stringBuilder.toString();

        JFrame frame = new JFrame("Message");
        JOptionPane.showMessageDialog(frame, result, "Message", JOptionPane.PLAIN_MESSAGE);


    }
}
