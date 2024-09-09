from website import create_app

app = create_app()

# Al ejecutar este archivo desde este archivo, no desde un importacion, se ejecuta la funcion
if __name__ == '__main__':
    app.run(debug=True)