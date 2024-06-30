from ext import app

if __name__ == "__main__":
    from routes import index, contact, register, registered, add, explore, product
    app.run(debug=True)