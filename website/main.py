from website.website import create_app

app = create_app()

if __name__ == "__main__":
    print("pre commit works!")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
