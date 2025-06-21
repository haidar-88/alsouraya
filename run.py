from app import create_app
from flask import redirect, session

app = create_app()

@app.route('/')
def index():
    if 'username' in session:
        return redirect('/products-page')
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
