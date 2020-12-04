
from flask import Flask, render_template,request
import website_checker
from flask import render_template
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        random_id = request.form['random_id']
        print(random_id)
        if random_id == 'demo_token':
            list_of_required, list_of_adopted = website_checker.get_crawler()
    
            return render_template('index.html',display_table = True,
            from_list = list_of_adopted,
            from_adopted = list_of_required)
        else:
            return 'TIME UP '
    else:
        random_id = 12
        return render_template('index.html', random_id = 'demo_token', display_table = False)

if __name__ == "__main__":
    app.run(debug=True)