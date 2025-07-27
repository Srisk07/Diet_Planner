from flask import Flask, render_template, request
import matplotlib.pyplot as plt
from GymDietAIPlanner import GymDietAIPlanner

# Initialize Flask app

app = Flask(__name__)

# Initialize the AI Planner
API_KEY = "AIzaSyBbG70G13oczClVPQw5QWP0TYCp-Nvj_ZU"
diet_planner = GymDietAIPlanner(api_key=API_KEY)

@app.route('/')
def index():
    """Render the main input form."""
    return render_template('HTML.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze the health profile and generate a diet plan."""
    # Retrieve form data
    user_profile = {
        'age': int(request.form['age']),
        'gender': request.form['gender'],
        'height': float(request.form['height']),
        'weight': float(request.form['weight']),
        'activity_level': request.form['activity_level'],
        'health_goal': request.form['health_goal']
    }

    # Perform health analysis
    health_analysis = diet_planner.analyze_health_profile(user_profile)

    # Generate AI Diet Plan
    ai_diet_plan = diet_planner.generate_ai_diet_plan(user_profile, health_analysis)

    # Save chart to static folder
    chart_path = "static/metabolic_chart.png"
    diet_planner.visualize_diet_analysis(health_analysis)
    plt.savefig(chart_path)
    plt.close()

    # Render result page
    return render_template(
        'RESULTS.html',
        user_profile=user_profile,
        health_analysis=health_analysis,
        diet_plan=ai_diet_plan,
        chart_path=chart_path
    )

if __name__ == "__main__":
    app.run(debug=True)

