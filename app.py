from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained ML model
model = joblib.load("scholarship_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    # Get data from form
    data = {
        "age": float(request.form["age"]),
        "cgpa": float(request.form["cgpa"]),
        "academic_percentage": float(request.form["academic_percentage"]),
        "ielts_score": float(request.form["ielts_score"]),

        "english_proficiency": request.form["english_proficiency"],
        "extracurricular_activities": request.form["extracurricular_activities"],
        "leadership_experience": request.form["leadership_experience"],
        "internship_experience": request.form["internship_experience"],
        "volunteer_experience": request.form["volunteer_experience"],
        "research_paper": request.form["research_paper"],
        "recommendation_strength": request.form["recommendation_strength"],
        "family_income_level": request.form["family_income_level"],
        "financial_need": request.form["financial_need"],
        "study_destination": request.form["study_destination"]
    }

    # Convert to DataFrame
    input_data = pd.DataFrame([data])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Get probability
    probabilities = model.predict_proba(input_data)[0]

    # Find probability of predicted class
    classes = model.classes_
    predicted_index = list(classes).index(prediction)

    probability = probabilities[predicted_index] * 100

    # Student information
    name = request.form.get("name", "Student")
    semester = request.form.get("semester", "")

    # Send result to result page
    return render_template(
        "result.html",
        name=name,
        semester=semester,
        prediction=prediction,
        probability=round(probability, 2)
    )


if __name__ == "__main__":
    app.run(debug=True)