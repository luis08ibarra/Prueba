
from app import create_app, db

app = create_app()


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
