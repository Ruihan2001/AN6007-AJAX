from flask import Flask, redirect, url_for, request
from flask import render_template,flash
import model, BinarySearch
app = Flask(__name__)
app.secret_key = 'Grh@20010321'

@app.route('/')
def index():
    return redirect(url_for('main'))

@app.route('/main')
def main():
    return render_template("index.html")

place_list = []
@app.route('/add_place',methods=['GET','POST'])
def add_place():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        place = request.form.get('place')
        country = request.form.get('country')
        weather = request.form.get('weather')
        description = request.form.get('description')

        for existed_place in place_list:
            if existed_place.name == place and existed_place.country == country:
                flash("Error: A place with the same name and country already exists.",'danger')
                return redirect(url_for('add_place'))
        new_place = model.Place(place, country,weather,description)
        place_list.append(new_place)

        flash("Place added successfully",'success')
        return redirect(url_for('add_place'))

    return render_template("add_places.html")

@app.route('/view_places',methods=['GET','POST'])
def view_places():
    if request.method == 'POST':
        filter_country = request.form.get('filter_country')
        filter_weather = request.form.get('filter_weather')
    return render_template("view_places.html")


@app.route('/place_detail',methods=['GET','POST'])
def place_detail():

    return render_template("place_detail.html")


remark=[]
@app.route('/vote',methods=['GET','POST'])
def vote():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        voted_place = request.form.get('voted_place')
        feedback = request.form.get('feedback')
        vote_history_records = model.findUserVoteHistory(user_name,voted_place)
        # print(vote_history_records)
        if vote_history_records:
            flash("You already voted", 'danger')
            return redirect(url_for('vote'))

        else:
            model.createVote(user_name, voted_place, feedback)
            remark.append([user_name, voted_place, feedback])

            flash("Feedback added successfully", 'success')
            return redirect(url_for('vote'))


    return render_template("vote.html")

@app.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'POST':
        user_name = request.form.get('username')
        history_records = model.findUserHistory(user_name)
        if history_records:
            return render_template("history.html",history_records=history_records,)
        else:
            flash('No related results! Please enter the correct username or re-vote!', 'danger')
            return redirect(url_for('history'))
    else:
        return render_template("history.html")




@app.route('/analysis',methods=['GET','POST'])
def analysis():
    return render_template("analysis.html")

if __name__ == '__main__':
    app.run()
