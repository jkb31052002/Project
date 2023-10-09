from Project import initialize_app

app = initialize_app()

if __name__ == "__main__":
    app.run(port=9000, debug=True)
