from db_app.formatter import prepare_activities_for_ai

topic = "phishing"
grade = "middle"
time = 60
standards = "CSTA K12 (3A-CS-02)"

result = prepare_activities_for_ai(topic, grade, time, standards)

print("\n===== RESULT =====\n")
print(result)