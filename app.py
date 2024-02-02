from flask import Flask, redirect, url_for, request,jsonify,render_template,flash
import model
app = Flask(__name__)
app.secret_key = 'Grh@20010321'

@app.route('/')
def index():
    return render_template("index.html")

place_list = []
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
    print(all_weathers)
    return jsonify(all_weathers)


@app.route('/places')
def get_places():
    all_places = list(set(place.name for place in place_list))
    all_places.sort()
    return jsonify(all_places)

@app.route('/view_places', methods=['GET', 'POST'])
def view_places():
    if request.method == 'POST':
        filter_country = request.form.get('filter_country')
        filter_weather = request.form.get('filter_weather')

        # print(filter_country)
        match_index = model.binary_search_all(place_list, filter_country, filter_weather)
        match_index.sort()
        print("okk",match_index)
        filtered_places = []
        for i in match_index:
            filtered_places.append(place_list[i])


        return jsonify(filtered_places=filtered_places)
    return render_template("view_places.html", filtered_places=place_list)


@app.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'POST':
        user_name = request.form.get('username2')
        print(user_name)
        print(type(user_name))
        history_records = model.findUserHistory(str(user_name))
        print("1",history_records)
        if history_records:
            print("2",history_records)
            return jsonify(history_records=history_records)
        else:
            flash('No related results! Please enter the correct username or re-vote!', 'danger')
            return jsonify(error='No related results')
    else:
        return render_template("index.html")


@app.route('/analysis',methods=['GET','POST'])
def analysis():
    return render_template("analysis.html")
if __name__ == '__main__':
    app.run(port=4060)
