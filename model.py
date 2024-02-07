class User:
    def __init__(self, username):
        self.username = username
        self.linked_places = []

class UserLinkedPlace:
    def __init__(self, place_name,feedback):
        self.place_name = place_name
        self.feedback = feedback

class Place:
    def __init__(self, name, country, weather, description):
        self.name = name
        self.country = country
        self.weather = weather
        self.description = description
        self.total_votes = 0
        self.all_feedback = []

# Store user
userdata = []
class Place:
    def __init__(self, name, country, weather, description):
        self.name = name
        self.country = country
        self.weather = weather
        self.description = description
        self.total_votes = 0
        self.all_feedback = []


def findUserHistory(username):
    if userdata and len(userdata) > 1:
        quickSort(userdata,0,len(userdata) - 1,lambda x:x.username)

    target_index = binary_search(userdata,0,len(userdata)-1,username,key=lambda x:x.username if not isinstance(x, str) else x)


    history_records = []

    if target_index== -1:
        return history_records

    userhistory = userdata[target_index].linked_places
    for i in userhistory:
        history_records.append((i.place_name,i.feedback))
    return history_records

# Search for filtered places
def partition2(array, low, high, key=lambda x: x):
    pivot = key(array[high])
    i = low - 1
    for j in range(low, high):
        if key(array[j]) <= pivot:
            i = i + 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1

def quickSort2(array, low, high, key=lambda x: x):
    if low < high:
        pi = partition2(array, low, high, key)
        quickSort2(array, low, pi - 1, key)
        quickSort2(array, pi + 1, high, key)


def binary_search_places(places, target_country, target_weather, low, high):

    quickSort2(places, 0, len(places) - 1, key=lambda x: (x.country.lower(), x.weather.lower()))

    if low > high:
        return []

    mid = (low + high) // 2
    country_matches = target_country is None or places[mid].country.lower() == target_country.lower()
    weather_matches = target_weather is None or places[mid].weather.lower() == target_weather.lower()

    if country_matches and weather_matches:
        results = [places[mid]]

        left = mid - 1
        while left >= low and places[left].country.lower() == target_country.lower() and places[left].weather.lower() == target_weather.lower():
            results.insert(0, places[left])
            left -= 1

        right = mid + 1
        while right <= high and places[right].country.lower() == target_country.lower() and places[right].weather.lower() == target_weather.lower():
            results.append(places[right])
            right += 1
        return results
    elif places[mid].country.lower() < (target_country or '').lower() or places[mid].weather.lower() < (
                    target_weather or '').lower():
        return binary_search_places(places, target_country, target_weather, mid + 1, high)
    else:
        return binary_search_places(places, target_country, target_weather, low, mid - 1)


# Vote
def createVote(user_name,voted_place,feedback,place_list):
    existing_user = next((user for user in userdata if user.username == user_name), None)

    if existing_user:
        existing_user.linked_places.append(UserLinkedPlace(voted_place, feedback))

    else:

        new_user = User(user_name)
        new_user.linked_places.append(UserLinkedPlace(voted_place, feedback))
        userdata.append(new_user)

    voted_place = next((place for place in place_list if place.name == voted_place), None)
    if voted_place:
        voted_place.total_votes += 1
        voted_place.all_feedback.append(feedback)
        print(voted_place.all_feedback)
    else:
        print("Error: Place not found.")

    return 'ok'

# search history
def findUserVoteHistory(username, voted_place_name):
    for user in userdata:
        print(user.username)
        if username == user.username:
            print('User Exists')
            quickSort(user.linked_places, 0, len(user.linked_places) - 1, key=lambda x: x.place_name)
            linked_places_sorted = sorted(user.linked_places, key=lambda x: x.place_name)
            place_index = binary_search(linked_places_sorted, 0, len(linked_places_sorted) - 1, voted_place_name,
                                            key=lambda x: x.place_name if not isinstance(x, str) else x)

            return place_index != -1
        else:
            continue
    return False

# top 10 voted country
def findTop10(place_list):
    quickSort(place_list,0,len(place_list)-1,lambda x:x.total_votes)
    top_place_list = place_list[-10:]
    top_place_name = []
    top_place_votes = []
    for place in top_place_list:
        top_place_votes.append(place.total_votes)
        top_place_name.append(place.name)
    return top_place_name, top_place_votes

# map data
def prepareMap(place_list):
    abb_country = [['AE', 'United Arab Emirates'], ['AF', 'Afghanistan'], ['AL', 'Albania'], ['AM', 'Armenia'], ['AO', 'Angola'], ['AR', 'Argentina'], ['AT', 'Austria'], ['AU', 'Australia'], ['AZ', 'Azerbaijan'], ['BA', 'Bosnia and Herzegovina'], ['BD', 'Bangladesh'], ['BE', 'Belgium'], ['BF', 'Burkina Faso'], ['BG', 'Bulgaria'], ['BI', 'Burundi'], ['BJ', 'Benin'], ['BN', 'Brunei Darussalam'], ['BO', 'Plurinational State of Bolivia'], ['BR', 'Brazil'], ['BT', 'Bhutan'], ['BW', 'Botswana'], ['BY', 'Belarus'], ['BZ', 'Belize'], ['CA', 'Canada'], ['CD', 'The Democratic Republic of the Congo'], ['CF', 'Central African Republic'], ['CG', 'Congo'], ['CH', 'Switzerland'], ['CI', 'Ivory Coast'], ['CL', 'Chile'], ['CM', 'Cameroon'], ['CN', 'China'], ['CO', 'Colombia'], ['CR', 'Costa Rica'], ['CU', 'Cuba'], ['CY', 'Cyprus'], ['CZ', 'Czech Republic'], ['DE', 'Germany'], ['DJ', 'Djibouti'], ['DK', 'Denmark'], ['DO', 'Dominican Republic'], ['DZ', 'Algeria'], ['EC', 'Ecuador'], ['EE', 'Estonia'], ['EG', 'Egypt'], ['EH', 'Western Sahara'], ['ER', 'Eritrea'], ['ES', 'Spain'], ['ET', 'Ethiopia'], ['FI', 'Finland'], ['FJ', 'Fiji'], ['FK', 'Falkland Islands (Malvinas)'], ['FR', 'France'], ['GA', 'Gabon'], ['GB', 'United Kingdom'], ['GE', 'Georgia'], ['GF', 'French Guiana'], ['GH', 'Ghana'], ['GL', 'Greenland'], ['GM', 'Gambia'], ['GN', 'Guinea'], ['GQ', 'Equatorial Guinea'], ['GR', 'Greece'], ['GT', 'Guatemala'], ['GW', 'Guinea-Bissau'], ['GY', 'Guyana'], ['HN', 'Honduras'], ['HR', 'Croatia'], ['HT', 'Haiti'], ['HU', 'Hungary'], ['ID', 'Indonesia'], ['IE', 'Ireland'], ['IL', 'Israel'], ['IN', 'India'], ['IQ', 'Iraq'], ['IR', 'Islamic Republic of Iran'], ['IS', 'Iceland'], ['IT', 'Italy'], ['JM', 'Jamaica'], ['JO', 'Jordan'], ['JP', 'Japan'], ['KE', 'Kenya'], ['KG', 'Kyrgyzstan'], ['KH', 'Cambodia'], ['KP', 'Democratic People’s Republic of Korea'], ['KR', 'Republic of Korea'], ['KW', 'Kuwait'], ['KZ', 'Kazakhstan'], ['LA', 'Lao People’s Democratic Republic'], ['LB', 'Lebanon'], ['LK', 'Sri Lanka'], ['LR', 'Liberia'], ['LS', 'Lesotho'], ['LT', 'Lithuania'], ['LU', 'Luxembourg'], ['LV', 'Latvia'], ['LY', 'Libyan Arab Jamahiriya'], ['MA', 'Morocco'], ['MD', 'Republic of Moldova'], ['MG', 'Madagascar'], ['MK', 'The Former Yugoslav Republic of Macedonia'], ['ML', 'Mali'], ['MM', 'Myanmar'], ['MN', 'Mongolia'], ['MR', 'Mauritania'], ['MW', 'Malawi'], ['MX', 'Mexico'], ['MY', 'Malaysia'], ['MZ', 'Mozambique'], ['NA', 'Namibia'], ['NC', 'New Caledonia'], ['NE', 'Niger'], ['NG', 'Nigeria'], ['NI', 'Nicaragua'], ['NL', 'Netherlands'], ['NO', 'Norway'], ['NP', 'Nepal'], ['NZ', 'New Zealand'], ['OM', 'Oman'], ['PA', 'Panama'], ['PE', 'Peru'], ['PG', 'Papua New Guinea'], ['PH', 'Philippines'], ['PK', 'Pakistan'], ['PL', 'Poland'], ['PR', 'Puerto Rico'], ['PS', 'Occupied Palestinian Territory'], ['PT', 'Portugal'], ['PY', 'Paraguay'], ['QA', 'Qatar'], ['RO', 'Romania'], ['RS', 'Serbia'], ['RU', 'Russian Federation'], ['RW', 'Rwanda'], ['SA', 'Saudi Arabia'], ['SB', 'Solomon Islands'], ['SD', 'Sudan'], ['SE', 'Sweden'], ['SJ', 'Svalbard and Jan Mayen'], ['SK', 'Slovakia'], ['SL', 'Sierra Leone'], ['SN', 'Senegal'], ['SO', 'Somalia'], ['SR', 'Suriname'], ['SV', 'El Salvador'], ['SY', 'Syrian Arab Republic'], ['SZ', 'Swaziland'], ['TD', 'Chad'], ['TG', 'Togo'], ['TH', 'Thailand'], ['TJ', 'Tajikistan'], ['TL', 'Timor-Leste'], ['TM', 'Turkmenistan'], ['TN', 'Tunisia'], ['TR', 'Turkey'], ['TZ', 'United Republic of Tanzania'], ['UA', 'Ukraine'], ['UG', 'Uganda'], ['US', 'United States'], ['UY', 'Uruguay'], ['UZ', 'Uzbekistan'], ['VE', 'Bolivarian Republic of Venezuela'], ['VN', 'Viet Nam'], ['VU', 'Vanuatu'], ['YE', 'Yemen'], ['ZA', 'South Africa'], ['ZM', 'Zambia'], ['ZW', 'Zimbabwe']]
    quickSort(place_list,0,len(place_list)-1,lambda x:x.country)
    map_data = {}
    for country in abb_country:
        index = binary_search(place_list, 0, len(place_list) - 1, country[1] , key = lambda x:x if not isinstance(x, str) else x)
        
        map_data[country[0]] = place_list[index].



# binary search
def partition(array, low, high,key = lambda x:x):
  pivot = key(array[high]).lower()
  i = low - 1
  for j in range(low, high):
    if key(array[j]).lower() <= pivot:
      i = i + 1
      (array[i], array[j]) = (array[j], array[i])
  (array[i + 1], array[high]) = (array[high], array[i + 1])
  return i + 1


def quickSort(array, low, high, get_string):
  """
  Please update the argument 'get_string' here in order to get the String for differnet element in array
  the format is - lambda x: x
  """
  if low < high:

    pi = partition(array, low, high, get_string)
    quickSort(array, low, pi - 1,get_string)
    quickSort(array, pi + 1, high,get_string)


def binary_search_all(arr, low, high, x, key=lambda x: x if not isinstance(x, str) else x):
    """
    Please update the argument 'get_string' here to get the String for different elements in the array.
    The format is - lambda x: x

    If the wanted string is found, the function will return a list of indices of the element in the array.
    Otherwise, the function will return an empty list.
    """
    result = []

    def binary_search_recursive(start, end):
        if start > end:
            return

        mid = (start + end) // 2

        if key(arr[mid]) == key(x):
            result.append(mid)

        # Search left for additional occurrences
        binary_search_recursive(start, mid - 1)

        # Search right for additional occurrences
        binary_search_recursive(mid + 1, end)

    binary_search_recursive(low, high)
    return result

# Load data
def load_data_from_files(user_file='users.txt', places_file='places.txt', user_linked_places_file='user_linked_places.txt'):
    userdata = []
    places = []

    with open(user_file, 'r', encoding='utf-8') as file:
        for line in file:
            username = line.strip()
            userdata.append(User(username))

    with open(places_file, 'r', encoding='utf-8') as file:
        for line in file:
            name, country, weather, description, total_votes, feedback_str = line.strip().split(',')
            feedback_list = feedback_str.split(';') if feedback_str else []
            place = Place(name, country, weather, description)
            place.total_votes = int(total_votes)
            place.all_feedback = feedback_list
            places.append(place)

    with open(user_linked_places_file, 'r', encoding='utf-8') as file:
        for line in file:
            username, place_name, feedback = line.strip().split(',')
            user = next((user for user in userdata if user.username == username), None)
            if user:
                user.linked_places.append(UserLinkedPlace(place_name, feedback))


    return userdata,places



def update_places_file(place_list):
    with open('places.txt', 'w', encoding='utf-8') as file:
        for place in place_list:
            feedback_str = ";".join(place.all_feedback)  # Join all feedback with ';'
            file.write(
                f"{place.name},{place.country},{place.weather},{place.description},{place.total_votes},{feedback_str}\n")

def update_vote_history_file(remark):
    with open('vote_history.txt', 'w', encoding='utf-8') as file:
        for entry in remark:
            user_name, voted_place, feedback = entry
            file.write(f"{user_name},{voted_place},{feedback}\n")
