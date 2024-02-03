from flask import Flask, redirect, url_for, request,jsonify,render_template,flash
import model
app = Flask(__name__)
app.secret_key = 'Grh@20010321'

@app.route('/')
def index():
    return render_template("index.html")

# def read_list():



place_list = []
remark=[]

@app.route('/add_place', methods=['GET','POST'])
def add_place():
    if request.method == 'POST':
        user_name = request.form.get('username1')
        place = request.form.get('place')
        country = request.form.get('country')
        weather = request.form.get('weather')
        description = request.form.get('description')
        # print(user_name,place,country,weather,description)
        existing_place = next((p for p in place_list if p.name == place and p.country == country), None)
        if existing_place:
            flash("Error: A place with the same name and country already exists.",'danger')
            return jsonify(error = 'Error')
            # return jsonify({'status': 'error', 'message': 'A place with the same name and country already exists.'})

        new_place = model.Place(place, country, weather, description)
        place_list.append(new_place)
        model.update_places_file(place_list)
        return jsonify(success = 'Success!')
        # flash("Place added successfully",'success')

@app.route('/country')
def get_countries():
    all_countries = list(set(place.country for place in place_list))
    all_countries.sort()
    return jsonify(all_countries)

@app.route('/weather')
def get_weathers():
    all_weathers = list(set(place.weather for place in place_list))
    all_weathers.sort()
    return jsonify(all_weathers)

@app.route('/places')
def get_places():
    all_places = list(set(place.name for place in place_list))
    all_places.sort()
    return jsonify(all_places)

@app.route('/view_places', methods=['GET', 'POST'])
def view_places():
    if request.method == 'POST':
        filter_country = request.form.get('filter_country','Any')
        filter_weather = request.form.get('filter_weather','Any')

        if filter_country in [None, '', 'Any']:
            filter_country = None
        if filter_weather in [None, '', 'Any']:
            filter_weather = None

        if filter_country is None and filter_weather is None:
            print('00')
            filtered_places = place_list
            # 问题在这 place_list都是空的，当然找不到
            print(place_list)
            print(filtered_places)
        else:
            filtered_places = []
            if filter_country and filter_weather:
                print('1')
                filtered_places = model.binary_search_places(place_list, filter_country, filter_weather, 0,
                                                             len(place_list) - 1)
            elif filter_country:
                print('2')
                filtered_places = model.binary_search_places(place_list, filter_country, '', 0, len(place_list) - 1)

            elif filter_weather:
                print('3')
                filtered_places = model.binary_search_places(place_list, '', filter_weather, 0, len(place_list) - 1)
                print(filtered_places)

        places_info = [f"{place.name},{place.country},{place.weather},{place.description},{place.total_votes},{place.all_feedback}" for place in filtered_places]
        return jsonify(places_info)
    else:
        return jsonify([])

# update_vote_history_file(remark)


@app.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'POST':
        user_name = request.form.get('username2')
        history_records = model.findUserHistory(str(user_name))
        if history_records:
            print(history_records)
            return jsonify(history_records=history_records)
        else:
            flash('No related results! Please enter the correct username or re-vote!', 'danger')
            return jsonify(error='No related results')
    else:
        return render_template("index.html")


@app.route('/vote',methods=['GET','POST'])
def vote():
    if request.method == 'POST':
        user_name = request.form.get('username3')
        voted_place = request.form.get('votedplace')
        feedback = request.form.get('feedback')
        vote_history_records = model.findUserVoteHistory(user_name,voted_place)
        # print(vote_history_records)
        if vote_history_records:
            flash("You already voted", 'danger')
            return jsonify(error='You already voted')

        else:
            model.createVote(user_name, voted_place, feedback)
            remark.append([user_name, voted_place, feedback])
            flash("Feedback added successfully", 'success')
            return jsonify(success="Feedback added successfully")


    return render_template("vote.html")
@app.route('/analysis',methods=['GET','POST'])
def analysis():
    return render_template("analysis.html")


if __name__ == '__main__':
    app.run(port=4060)
