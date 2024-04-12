from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        user_input = request.form['user_input']
        # Logic to determine the URL based on user input
        if user_input == 'example':
            return redirect('https://example.com')
        else:
            return redirect('https://google.com')
    return '''
        <form method="post">
            <input type="text" name="user_input" />
            <input type="submit" value="Go" />
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
