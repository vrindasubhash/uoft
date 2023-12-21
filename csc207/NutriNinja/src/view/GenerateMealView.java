package view;

import interface_adapter.ViewManagerModel;
import interface_adapter.generate_meal.GenerateMealController;
import interface_adapter.generate_meal.GenerateMealState;
import interface_adapter.generate_meal.GenerateMealViewModel;
import interface_adapter.generate_random_meal.GenerateRandomMealController;
import interface_adapter.save_preferences.SavePreferencesController;
import interface_adapter.save_preferences.SavePreferencesState;
import interface_adapter.save_preferences.SavePreferencesViewModel;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.beans.PropertyChangeEvent;
import java.beans.PropertyChangeListener;
import java.io.IOException;
import java.net.URL;

public class GenerateMealView extends JPanel implements ActionListener, PropertyChangeListener {

    public final String viewName = "Generate Meal";

    public final GenerateMealViewModel generateMealViewModel;
    public GenerateMealController generateMealController;
    public SavePreferencesController savePreferencesController;
    public final SavePreferencesViewModel savePreferencesViewModel;
    public GenerateRandomMealController generateRandomMealController;



    public JLabel mealSuggested = new JLabel("");
    public JLabel imageURL = new JLabel("");
    public JLabel servings = new JLabel("");
    public JLabel calories = new JLabel("");
    public JLabel protein = new JLabel("");
    public JLabel carbs = new JLabel("");
    public JLabel fat = new JLabel("");
    public JLabel ingredients = new JLabel("");
    public JLabel recipeSource = new JLabel("");
    public JLabel recipeURL = new JLabel("");

    public JLabel pictureLabel = new JLabel();

    public JLabel ingredientsFormatted = new JLabel();


    public JButton regenerateButton;


    public GenerateMealView(GenerateMealViewModel generateMealViewModel_,
                            SavePreferencesViewModel savePreferencesViewModel_,
                            GenerateMealController generateMealController_,
                            SavePreferencesController savePreferencesController_,
                            GenerateRandomMealController generateRandomMealController_) throws IOException{

        this.generateMealViewModel = generateMealViewModel_;
        this.generateMealController = generateMealController_;
        this.savePreferencesController = savePreferencesController_;
        this.generateRandomMealController = generateRandomMealController_;
        this.savePreferencesViewModel = savePreferencesViewModel_;
        generateMealViewModel.addPropertyChangeListener(this);
        savePreferencesViewModel.addPropertyChangeListener(this);



        Font f1 = new Font("Lucida Grande", Font.PLAIN, 13);
        Font f2 = new Font("Lucida Grande", Font.BOLD, 15);


        JLabel title = new JLabel(GenerateMealViewModel.TITLE);
        title.setFont(new Font("Lucida Grande", Font.BOLD, 20));
        title.setAlignmentX(Component.CENTER_ALIGNMENT);

        JPanel mealSuggestedPanel = new JPanel();
        JLabel mealSuggestedHeader = new JLabel(GenerateMealViewModel.MEAL_HEADER);
        mealSuggestedHeader.setFont(f2);
        mealSuggestedPanel.add(mealSuggestedHeader);

        mealSuggestedPanel.add(mealSuggested);


        JPanel picturePanel = new JPanel();


        picturePanel.add(pictureLabel);

        JPanel infoPanel = new JPanel();
        infoPanel.setLayout(new FlowLayout());

        JPanel servingsPanel = new JPanel();
        JLabel servingsHeader = new JLabel(GenerateMealViewModel.SERVINGS_HEADER);
        servingsHeader.setFont(f2);
        servingsPanel.add(servingsHeader);
        servingsPanel.add(servings);

        JPanel caloriesPanel= new JPanel();
        JLabel caloriesHeader = new JLabel(GenerateMealViewModel.CALORIES_HEADER);
        caloriesHeader.setFont(f2);
        caloriesPanel.add(caloriesHeader);
        caloriesPanel.add(calories);

        JPanel proteinPanel = new JPanel();
        JLabel proteinHeader = new JLabel(GenerateMealViewModel.PROTEIN_HEADER);
        proteinHeader.setFont(f2);
        proteinPanel.add(proteinHeader);
        proteinPanel.add(protein);

        JPanel carbsPanel = new JPanel();
        JLabel carbsHeader = new JLabel(GenerateMealViewModel.CARBS_HEADER);
        carbsHeader.setFont(f2);
        carbsPanel.add(carbsHeader);
        carbsPanel.add(carbs);

        JPanel fatPanel = new JPanel();
        JLabel fatHeader = new JLabel(GenerateMealViewModel.FAT_HEADER);
        fatHeader.setFont(f2);
        fatPanel.add(fatHeader);
        fatPanel.add(fat);

        infoPanel.add(servingsPanel);
        infoPanel.add(caloriesPanel);
        infoPanel.add(proteinPanel);
        infoPanel.add(carbsPanel);
        infoPanel.add(fatPanel);


        JPanel ingredientsPanel = new JPanel();
        JLabel ingredientHeader = new JLabel(GenerateMealViewModel.INGREDIENTS_HEADER);
        ingredientHeader.setFont(f2);
        ingredientsPanel.add(ingredientHeader);

        ingredientsFormatted.setFont(f1);
        ingredientsPanel.add(ingredientsFormatted);
        ingredientsPanel.setPreferredSize(new Dimension(500, 200));


        JPanel recipeSourcePanel = new JPanel();
        JLabel recipeSourceHeader = new JLabel(GenerateMealViewModel.RECIPE_SOURCE_HEADER);
        recipeSourceHeader.setFont(f2);
        recipeSourcePanel.add(recipeSourceHeader);
        recipeSourcePanel.add(recipeSource);

        JPanel recipeLinkPanel = new JPanel();
        JLabel recipeLinkHeader = new JLabel(GenerateMealViewModel.RECIPE_LINK_HEADER);
        recipeLinkHeader.setFont(f2);
        recipeLinkPanel.add(recipeLinkHeader);
        recipeLinkPanel.add(recipeURL);


        JPanel buttonsPanel = new JPanel();
        buttonsPanel.setLayout(new FlowLayout());


        JButton backButton = new JButton(GenerateMealViewModel.BACK_BUTTON_LABEL);
        regenerateButton = new JButton(GenerateMealViewModel.REGENERATE_BUTTON_LABEL);
        JButton feelingLuckyButton = new JButton(GenerateMealViewModel.FEELING_LUCKY_BUTTON_LABEL);


        buttonsPanel.add(backButton);
        buttonsPanel.add(regenerateButton);
        buttonsPanel.add(feelingLuckyButton);

        backButton.addActionListener(
                new ActionListener() {
                    public void actionPerformed(ActionEvent evt) {
                        if (evt.getSource().equals(backButton)) {
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
                        }
                    }
                }
        );

        regenerateButton.addActionListener(
                new ActionListener() {
                    public void actionPerformed(ActionEvent evt) {
                        if (evt.getSource().equals(regenerateButton)) {
                            SavePreferencesState currentState = savePreferencesViewModel.getState();

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

                        }
                    }
                }
        );

        feelingLuckyButton.addActionListener(
                new ActionListener() {
                    public void actionPerformed(ActionEvent evt) {
                        if (evt.getSource().equals(feelingLuckyButton)){
                            generateRandomMealController.execute();
                        }
                    }
                }
        );


        this.setLayout(new BoxLayout(this, BoxLayout.Y_AXIS));
        this.setPreferredSize(new Dimension(1920,1080));
        this.add(title);
        this.add(mealSuggestedPanel);
        this.add(picturePanel);
        this.add(infoPanel);
        this.add(ingredientsPanel);
        this.add(recipeSourcePanel);
        this.add(recipeLinkPanel);
        this.add(buttonsPanel);


    }

    @Override
    public void actionPerformed(ActionEvent e) {

    }

    @Override
    public void propertyChange(PropertyChangeEvent evt) {
        if (evt.getNewValue().getClass().equals(GenerateMealState.class)){
            GenerateMealState state = (GenerateMealState) evt.getNewValue();
            setFields(state);
        }

    }

    private void setFields (GenerateMealState state){
        mealSuggested.setText(state.getMealName());
        imageURL.setText(state.getImageURL());
        try {
            pictureLabel.setIcon(new ImageIcon(ImageIO.read(new URL(imageURL.getText()))));

        } catch (Exception e){
            pictureLabel.setText("No Image Available");
        }
        servings.setText(String.valueOf(state.getServings()));
        calories.setText(Math.round(state.getMealCalories() / state.getServings()) + "kcal");
        protein.setText(Math.round(state.getMealProtein() / state.getServings()) + "g");
        carbs.setText(Math.round(state.getMealCarbs() / state.getServings()) + "g");
        fat.setText(Math.round(state.getMealFat() / state.getServings()) + "g");

        ingredients.setText(state.getIngredientsLabel());
        if (!ingredients.getText().isEmpty()){
            String ingredientsFormat = "<html>" + ingredients.getText().replace(",", "<br/>").substring(1,ingredients.getText().length()-1 ) + "</html>";
            ingredientsFormatted.setText(ingredientsFormat);
        }


        recipeSource.setText(state.getRecipeSource());
        recipeURL.setText(state.getRecipeURL());

    }
}
