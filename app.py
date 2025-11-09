from flask import Flask, render_template, request
import google.generativeai as genai


import os

app = Flask(__name__)

# 🛡️ Set your Google Gemini API key securely
os.environ["GOOGLE_API_KEY"] = "AIzaSyDMyHAldMURVg--AHPxM2CNju-OddCvRe0"  # ← Replace with your real key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# ✅ Use the free-tier model
model = genai.GenerativeModel("gemini-2.5-flash")


# Function to generate recommendations
def generate_recommendation(dietary_preferences, fitness_goals, lifestyle_factors,
                            dietary_restrictions, health_conditions, user_query):
    prompt = f"""
    Create a detailed and customized health improvement plan for this user:
    Dietary Preferences: {dietary_preferences}
    Fitness Goals: {fitness_goals}
    Lifestyle Factors: {lifestyle_factors}
    Dietary Restrictions: {dietary_restrictions}
    Health Conditions: {health_conditions}
    User Query: {user_query}

    Please include the following sections clearly labeled:
    Diet Recommendations:
    - 5 specific diet types suited to their preferences and goals.

    Workout Options:
    - 5 workout recommendations aligned with their fitness level and goals.

    Meal Suggestions:
    - 5 breakfast ideas.
    - 5 dinner ideas.

    Additional Recommendations:
    - 5 useful tips about snacks, supplements, or hydration.
    """

    try:
        response = model.generate_content(prompt)
        return response.text if response else "No response from the model."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html', recommendations=None, error=None)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    try:
        dietary_preferences = request.form.get('dietary_preferences', '')
        fitness_goals = request.form.get('fitness_goals', '')
        lifestyle_factors = request.form.get('lifestyle_factors', '')
        dietary_restrictions = request.form.get('dietary_restrictions', '')
        health_conditions = request.form.get('health_conditions', '')
        user_query = request.form.get('user_query', '')

        # Generate AI-based recommendations
        recommendations_text = generate_recommendation(
            dietary_preferences, fitness_goals, lifestyle_factors,
            dietary_restrictions, health_conditions, user_query
        )

        # Split text by sections
        sections = {
            "Diet Recommendations": [],
            "Workout Options": [],
            "Meal Suggestions": [],
            "Additional Recommendations": []
        }

        current_section = None
        for line in recommendations_text.splitlines():
            line = line.strip()
            if not line:
                continue
            for section in sections.keys():
                if section.lower() in line.lower():
                    current_section = section
                    break
            else:
                if current_section:
                    sections[current_section].append(line)

        return render_template('index.html', recommendations=sections, error=None)

    except Exception as e:
        return render_template('index.html', recommendations=None, error=str(e))


if __name__ == "__main__":
    app.run(debug=True)
