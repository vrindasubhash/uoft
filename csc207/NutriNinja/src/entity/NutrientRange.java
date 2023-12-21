package entity;

import app.custom_data.Range;

public class NutrientRange {
    private Range<Integer> calorieRange;
    private Range<Integer> fatRange;
    private Range<Integer> proteinRange;
    private Range<Integer> carbRange;

    public NutrientRange(Range<Integer> calorieRange, Range<Integer> fatRange, Range<Integer> proteinRange, Range<Integer> carbRange) {
        this.calorieRange = calorieRange;
        this.fatRange = fatRange;
        this.proteinRange = proteinRange;
        this.carbRange = carbRange;
    }


    public Range<Integer> getCalorieRange() {
        return calorieRange;
    }

    public void setCalorieRange(Range<Integer> calorieRange) {
        this.calorieRange = calorieRange;
    }

    public Range<Integer> getFatRange() {
        return fatRange;
    }

    public void setFatRange(Range<Integer> fatRange) {
        this.fatRange = fatRange;
    }

    public Range<Integer> getProteinRange() {
        return proteinRange;
    }

    public void setProteinRange(Range<Integer> proteinRange) {
        this.proteinRange = proteinRange;
    }

    public Range<Integer> getCarbRange() {
        return carbRange;
    }

    public void setCarbRange(Range<Integer> carbRange) {
        this.carbRange = carbRange;
    }
}
