# GymDietAIPlanner.py

import google.generativeai as genai
import matplotlib.pyplot as plt

class GymDietAIPlanner:
    def __init__(self, api_key):
        """Initialize the Generative AI Diet Planner"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def calculate_bmr(self, gender, weight, height, age):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        return bmr

    def calculate_tdee(self, bmr, activity_level):
        """Calculate Total Daily Energy Expenditure"""
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725
        }
        return bmr * activity_multipliers.get(activity_level, 1.2)

    def generate_ai_diet_plan(self, user_profile, health_analysis):
        """Use Generative AI to create a personalized diet plan"""
        prompt = f"""
        Create a detailed gym-focused diet plan based on these parameters:
        - Goal: {user_profile['health_goal']}
        - Daily Calories: {health_analysis['adjusted_calories']:.0f}
        - Body Weight: {user_profile['weight']} kg
        - Activity Level: {user_profile['activity_level']}

        Provide:
        1. Meal-by-meal breakdown
        2. Macro and micro nutrient recommendations
        3. Specific food suggestions for muscle gain/performance
        4. Timing of meals relative to workout
        5. Hydration recommendations
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"AI Generation Error: {e}"

    def analyze_health_profile(self, user_profile):
        """Comprehensive health profile analysis"""
        # Calculate metabolic metrics
        bmr = self.calculate_bmr(
            user_profile['gender'],
            user_profile['weight'],
            user_profile['height'],
            user_profile['age']
        )

        tdee = self.calculate_tdee(bmr, user_profile['activity_level'])

        # Goal-based calorie adjustment
        goal_adjustments = {
            'muscle_gain': 300,
            'weight_loss': -500,
            'maintenance': 0,
            'athletic_performance': 200
        }

        adjusted_calories = tdee + goal_adjustments.get(user_profile['health_goal'], 0)

        return {
            'bmr': bmr,
            'tdee': tdee,
            'adjusted_calories': adjusted_calories
        }

    def visualize_diet_analysis(self, health_analysis):
        """Create visualization of metabolic metrics"""
        plt.figure(figsize=(10, 6))
        plt.title('Metabolic Analysis Dashboard', fontsize=15)

        metrics = [
            'Basal Metabolic Rate (BMR)',
            'Total Daily Energy Expenditure (TDEE)',
            'Adjusted Calories'
        ]
        values = [
            health_analysis['bmr'],
            health_analysis['tdee'],
            health_analysis['adjusted_calories']
        ]

        plt.bar(metrics, values, color=['blue', 'green', 'red'])
        plt.ylabel('Calories')
        plt.xticks(rotation=45)

        for i, v in enumerate(values):
            plt.text(i, v, f'{v:.0f}', ha='center', va='bottom')

        plt.tight_layout()

        # Save visualization to file for use in Flask app
        plt.savefig('static/metabolic_chart.png')
        plt.close()
