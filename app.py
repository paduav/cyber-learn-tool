from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/lesson-plan")
    def lesson_plan_page():
        return render_template("lesson-plan.html")
    
    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
