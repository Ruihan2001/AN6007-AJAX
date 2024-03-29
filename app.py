import os
import threading

from flask import Flask, redirect, url_for, request, jsonify, render_template, flash, json
import model
app = Flask(__name__)
app.secret_key = 'Grh@20010321'

@app.route('/')
def index():
    return render_template("index.html")

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
        if user_name =='' or place =='' or country =='' or weather =='' or description =='':
            return jsonify(error2="Please enter all the information!")
        else:
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
    # print(type(place_list))
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
            filtered_places = place_list

        else:
            filtered_places = []
            if filter_country and filter_weather:
                filtered_places = model.binary_search_places(place_list, filter_country, filter_weather,)
            elif filter_country:
                filtered_places = model.binary_search_places(place_list, filter_country, None)
            elif filter_weather:
                filtered_places = model.binary_search_places(place_list, None, filter_weather)

        places_info = [f"{place.name},{place.country},{place.weather},{place.description},{place.total_votes}," + ';'.join(place.all_feedback) for place in set(filtered_places)]
        # print(places_info)
        return jsonify(places_info)
    else:
        return jsonify([])


@app.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'POST':
        user_name = request.form.get('username2')
        history_records = model.findUserHistory(str(user_name),userdata)
        if history_records:
            print(history_records)
            return jsonify(history_records=history_records)
        else:
            print('No related results! Please enter the correct username or re-vote!', 'danger')
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
        print(type(user_name))
        print(user_name)
        if user_name =='':
            return jsonify(error='Error: Please enter your username.')
        # vote_history_records = model.findUserVoteHistory(user_name,voted_place)
        # print(vote_history_records)
        # if vote_history_records:
            # flash("You already voted", 'danger')
            # return jsonify(error='You already voted')
        else:
        # flash("Feedback added successfully", 'success')
            place_search = model.createVote(user_name, voted_place, feedback, place_list,userdata)
            print(place_search)
            if place_search == 0:

                return jsonify(error2='Error: Place not found.')
            elif place_search == 1:
                return jsonify(error3='Error: You already voted for this place')
            else:
                print("vote info:",user_name,voted_place,feedback)
                remark.append([user_name, voted_place, feedback])
                model.update_users_file(remark)
                # Update places.txt with the new state of all places
                model.update_places_file(place_list)
                return jsonify(success="Feedback added successfully")

    return render_template("vote.html")

@app.route('/analysis',methods=['GET','POST'])
def analysis():
    top_place_names, top_place_votes = model.findTop3(place_list)
    map = model.prepareMap(place_list)

    total_places_num ,total_voted_places= model.cal_number_of_places_and_votes(place_list)
    return render_template("analysis.html",top_place_names=top_place_names, top_place_votes=top_place_votes,map_data = map,total_voted_places=total_voted_places,total_places_num=total_places_num)

def merge():
    print("Excuting timed task...")
    model.merge_and_clear_files()

def run_schedule():
    schedule.every(10).minutes.do(merge)

    while True:
        schedule.run_pending()
        time.sleep(1)

def is_file_empty(file_path):
    try:
        return os.path.getsize(file_path) == 0
    except OSError:
        return True

if __name__ == '__main__':
    import schedule
    import time

    users_file_path = 'users.txt'
    places_file_path = 'places.txt'


    userdata, place_list = model.load_data_from_files(users_file_path,places_file_path)
    t = threading.Thread(target=run_schedule)
    t.start()

    app.run(port=4060)
    #
    # schedule.every(10).seconds.do(model.merge_and_clear_files)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
