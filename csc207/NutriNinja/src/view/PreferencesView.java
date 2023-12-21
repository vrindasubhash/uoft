package view;

import interface_adapter.generate_meal.GenerateMealController;
import interface_adapter.generate_meal.GenerateMealViewModel;
import interface_adapter.generate_random_meal.GenerateRandomMealController;
import interface_adapter.save_preferences.SavePreferencesController;
import interface_adapter.save_preferences.SavePreferencesState;
import interface_adapter.save_preferences.SavePreferencesViewModel;

import javax.swing.*;
import java.util.ArrayList;
import java.util.List;
import java.awt.*;
import java.awt.event.*;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;

public class PreferencesView extends JPanel implements ActionListener, PropertyChangeListener {

    public final String viewName = "Preferences";

    public final JButton savePreferences;
    public final JButton generateMeal;
    public final JButton feelingLucky;

    JTextField minimumCalorieInputField = new JTextField(15);
    private final JLabel minimumCalorieErrorField = new JLabel();
    final JTextField maximumCalorieInputField = new JTextField(15);
    private final JLabel maximumCalorieErrorField = new JLabel();


    final JTextField minimumFatInputField = new JTextField(15);
    private final JLabel minimumFatErrorField = new JLabel();
    final JTextField maximumFatInputField = new JTextField(15);
    private final JLabel maximumFatErrorField = new JLabel();


    final JTextField minimumProteinInputField = new JTextField(15);
    private final JLabel minimumProteinErrorField = new JLabel();
    final JTextField maximumProteinInputField = new JTextField(15);
    private final JLabel maximumProteinErrorField = new JLabel();


    final JTextField minimumCarbInputField = new JTextField(15);
    private final JLabel minimumCarbErrorField = new JLabel();
    final JTextField maximumCarbInputField = new JTextField(15);
    private final JLabel maximumCarbErrorField = new JLabel();

    JLabel successLabel = new JLabel("");
    JLabel usernameInfo = new JLabel("");

    String[] healthPreferencesOptions = {"dairy-free", "fish-free", "gluten-free", "keto-friendly",
    "kosher", "low-sugar", "peanut-free", "pescatarian", "pork-free", "vegan", "vegetarian"};
    String[] dishTypeOptions = {"Desserts", "Main Course", "Salad", "Sandwiches", "Side Dish", "Soup", "Starter"};
    String[] mealTypeOptions = {"Breakfast", "Lunch", "Dinner", "Snack"};

    final JList<String> healthPreferencesInputField = new JList<>(healthPreferencesOptions);
    private final JLabel healthPreferencesErrorField = new JLabel();

    final JList<String> dishTypeInputField = new JList<>(dishTypeOptions);
    private final JLabel dishTypeErrorField = new JLabel();

    final JList<String> mealTypeInputField = new JList<>(mealTypeOptions);
    private final JLabel mealTypeErrorField = new JLabel();

    LabelTextPanel minimumCalorieInfo = new LabelTextPanel(
            new JLabel("Minimum Calories"), minimumCalorieInputField);
    LabelTextPanel maximumCalorieInfo = new LabelTextPanel(
            new JLabel("Maximum Calories"), maximumCalorieInputField);

    LabelTextPanel minimumFatInfo = new LabelTextPanel(
            new JLabel("Minimum Fat (g)"), minimumFatInputField);
    LabelTextPanel maximumFatInfo = new LabelTextPanel(
            new JLabel("Maximum Fat (g)"), maximumFatInputField);

    LabelTextPanel minimumProteinInfo = new LabelTextPanel(
            new JLabel("Minimum Protein (g)"), minimumProteinInputField);
    LabelTextPanel maximumProteinInfo = new LabelTextPanel(
            new JLabel("Maximum Protein (g)"), maximumProteinInputField);

    LabelTextPanel minimumCarbInfo = new LabelTextPanel(
            new JLabel("Minimum Carbs (g)"), minimumCarbInputField);
    LabelTextPanel maximumCarbInfo = new LabelTextPanel(
            new JLabel("Maximum Carbs (g)"), maximumCarbInputField);

    JPanel healthPreferencesInfo = new JPanel();{
        healthPreferencesInfo.add(new JLabel("Health Preferences"));
        healthPreferencesInfo.add(healthPreferencesInputField);
    }

    JPanel dishTypeInfo = new JPanel();{
        dishTypeInfo.add(new JLabel("Dish Type"));
        dishTypeInfo.add(dishTypeInputField);
    }

    JPanel mealTypeInfo = new JPanel();{
        mealTypeInfo.add(new JLabel("Meal Type"));
        mealTypeInfo.add(mealTypeInputField);
    }


    private final SavePreferencesController savePreferencesController;
    private final GenerateMealController generateMealController;
    private final GenerateRandomMealController generateRandomMealController;
    private final SavePreferencesViewModel savePreferencesViewModel;
    private final GenerateMealViewModel generateMealViewModel;

    /**
     * A window with a title and a JButton.
     */
    public PreferencesView(GenerateMealViewModel generateMealViewModel_,
                           SavePreferencesViewModel savePreferencesViewModel_,
                           SavePreferencesController savePreferencesController_,
                           GenerateMealController generateMealController_,
                           GenerateRandomMealController generateRandomMealController_) {

        this.savePreferencesController = savePreferencesController_;
        this.generateMealController = generateMealController_;
        this.generateRandomMealController = generateRandomMealController_;
        this.savePreferencesViewModel = savePreferencesViewModel_;
        this.generateMealViewModel = generateMealViewModel_;
        savePreferencesViewModel.addPropertyChangeListener(this);

        JLabel title = new JLabel("Enter Preferences");
        title.setAlignmentX(Component.CENTER_ALIGNMENT);

        JPanel buttons = new JPanel();
        savePreferences = new JButton(SavePreferencesViewModel.SAVE_PREFERENCES_BUTTON_LABEL);
        generateMeal = new JButton((SavePreferencesViewModel.GENERATE_MEAL_BUTTON_LABEL));
        feelingLucky = new JButton((SavePreferencesViewModel.FEELING_LUCKY_BUTTON_LABEL));
        buttons.add(savePreferences);
        buttons.add(generateMeal);
        buttons.add(feelingLucky);


        savePreferences.addActionListener(
                new ActionListener() {
                    public void actionPerformed(ActionEvent evt) {
                        if (evt.getSource().equals(savePreferences)) {
                            SavePreferencesState currentState = savePreferencesViewModel.getState();

                            savePreferencesController.execute(
                                    currentState.getNutrientRange().getCalorieRange(),
                                    currentState.getNutrientRange().getFatRange(),
                                    currentState.getNutrientRange().getProteinRange(),
                                    currentState.getNutrientRange().getCarbRange(),
                                    currentState.getHealthPreferences(),
                                    currentState.getDishType(),
                                    currentState.getUsername()
                            );
                            //JOptionPane.showMessageDialog(PreferencesView.this, "Preferences Saved!");
                            successLabel.setText("Preferences Saved!");
                            successLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
                        }
                    }
                }
        );

        generateMeal.addActionListener(
                new ActionListener() {
                    public void actionPerformed(ActionEvent evt) {
                        if (evt.getSource().equals(generateMeal)) {
                            SavePreferencesState currentState = savePreferencesViewModel.getState();

                            savePreferencesController.execute(
                                    currentState.getNutrientRange().getCalorieRange(),
                                    currentState.getNutrientRange().getFatRange(),
                                    currentState.getNutrientRange().getProteinRange(),
                                    currentState.getNutrientRange().getCarbRange(),
                                    currentState.getHealthPreferences(),
                                    currentState.getDishType(),
                                    currentState.getUsername()
                            );

                                generateMealController.execute(
                                        currentState.getHealthPreferences(),
                                        currentState.getMealType(),
                                        currentState.getDishType(),
                                        currentState.getNutrientRange().getCalorieRange().getLowerBound(),
                                        currentState.getNutrientRange().getCalorieRange().getUpperBound(),
                                        currentState.getNutrientRange().getCarbRange().getLowerBound(),
                                        currentState.getNutrientRange().getCarbRange().getUpperBound(),
                                        currentState.getNutrientRange().getProteinRange().getLowerBound(),
                                        currentState.getNutrientRange().getProteinRange().getUpperBound(),
                                        currentState.getNutrientRange().getFatRange().getLowerBound(),
                                        currentState.getNutrientRange().getFatRange().getUpperBound()
                                );
                            if (generateMealViewModel.getState().getAPIError() != null){
                                JOptionPane.showMessageDialog(PreferencesView.this, generateMealViewModel.getState().getAPIError());
                            }



                        }
                    }
                }
        );

        feelingLucky.addActionListener(
                new ActionListener() {
                    public void actionPerformed(ActionEvent evt) {
                        if (evt.getSource().equals(feelingLucky)) {
                            generateRandomMealController.execute();
                        }
                    }
                }
        );

        minimumCalorieInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getCalorieRange().setLowerBound(Integer.valueOf(minimumCalorieInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        maximumCalorieInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getCalorieRange().setUpperBound(Integer.valueOf(maximumCalorieInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        minimumFatInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getFatRange().setLowerBound(Integer.valueOf(minimumFatInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        maximumFatInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getFatRange().setUpperBound(Integer.valueOf(maximumFatInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        minimumProteinInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getProteinRange().setLowerBound(Integer.valueOf(minimumProteinInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        maximumProteinInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getProteinRange().setUpperBound(Integer.valueOf(maximumProteinInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        minimumCarbInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getCarbRange().setLowerBound(Integer.valueOf(minimumCarbInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        maximumCarbInputField.addKeyListener(new KeyListener() {
            @Override
            public void keyTyped(KeyEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.getNutrientRange().getCarbRange().setUpperBound(Integer.valueOf(maximumCarbInputField.getText() + e.getKeyChar()));
                savePreferencesViewModel.setState(currentState);
            }

            @Override
            public void keyPressed(KeyEvent e) {
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }
        });

        healthPreferencesInputField.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.setHealthPreferences(healthPreferencesInputField.getSelectedValuesList());
                savePreferencesViewModel.setState(currentState);
            }
        });

        dishTypeInputField.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.setDishType(dishTypeInputField.getSelectedValuesList());
                savePreferencesViewModel.setState(currentState);
            }
        });

        mealTypeInputField.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                SavePreferencesState currentState = savePreferencesViewModel.getState();
                currentState.setMealType(mealTypeInputField.getSelectedValuesList());
                savePreferencesViewModel.setState(currentState);
            }
        });

        this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        this.setPreferredSize(new Dimension(1020,1080));
        this.add(usernameInfo);
        this.add(title);

        this.add(minimumCalorieInfo);
        this.add(minimumCalorieErrorField);
        this.add(maximumCalorieInfo);
        this.add(maximumCalorieErrorField);

        this.add(minimumFatInfo);
        this.add(minimumFatErrorField);
        this.add(maximumFatInfo);
        this.add(maximumFatErrorField);

        this.add(minimumProteinInfo);
        this.add(minimumProteinErrorField);
        this.add(maximumProteinInfo);
        this.add(maximumProteinErrorField);

        this.add(minimumCarbInfo);
        this.add(minimumCarbErrorField);
        this.add(maximumCarbInfo);
        this.add(maximumCarbErrorField);

        this.add(healthPreferencesInfo);
        this.add(healthPreferencesErrorField);
        this.add(dishTypeInfo);
        this.add(dishTypeErrorField);
        this.add(mealTypeInfo);
        this.add(mealTypeErrorField);

        this.add(buttons);
        this.add(successLabel);
    }

    /**
     * React to a button click that results in evt.
     */
    public void actionPerformed(ActionEvent evt) {
        System.out.println("Click " + evt.getActionCommand());
    }
    private int[] get_indices(List<String> selected_preferences, String[] options) {
        List<Integer> res = new ArrayList<>();

        for (int i = 0; i < options.length; i++) {
            if (selected_preferences.contains(options[i])) {
                res.add(i);
            }
        }
        return res.stream().mapToInt(Integer::intValue).toArray();
    }

    @Override
    public void propertyChange(PropertyChangeEvent evt) {
        if (evt.getNewValue().getClass().equals(SavePreferencesState.class)){
            SavePreferencesState state = (SavePreferencesState) evt.getNewValue();
            usernameInfo.setText("Currently logged in: " + state.getUsername());
            usernameInfo.setAlignmentX(Component.CENTER_ALIGNMENT);
            minimumCalorieInputField.setText(state.getNutrientRange().getCalorieRange().getLowerBound().toString());
            maximumCalorieInputField.setText(state.getNutrientRange().getCalorieRange().getUpperBound().toString());
            minimumFatInputField.setText(state.getNutrientRange().getFatRange().getLowerBound().toString());
            maximumFatInputField.setText(state.getNutrientRange().getFatRange().getUpperBound().toString());
            minimumProteinInputField.setText(state.getNutrientRange().getProteinRange().getLowerBound().toString());
            maximumProteinInputField.setText(state.getNutrientRange().getProteinRange().getUpperBound().toString());
            minimumCarbInputField.setText(state.getNutrientRange().getCarbRange().getLowerBound().toString());
            maximumCarbInputField.setText(state.getNutrientRange().getCarbRange().getUpperBound().toString());
            healthPreferencesInputField.setSelectedIndices(get_indices(state.getHealthPreferences(), healthPreferencesOptions));
            dishTypeInputField.setSelectedIndices(get_indices(state.getDishType(), dishTypeOptions));
        }

    }
}