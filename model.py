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


def findUserHistory(username,userdata):
    if userdata and len(userdata) > 1:
        quickSort(userdata,0,len(userdata) - 1,lambda x:x.username)

    user_index = binary_search_all(userdata,0,len(userdata)-1,username,key=lambda x:x.username if not isinstance(x, str) else x)


    history_records = []

    if not user_index:
        return history_records
    else:
        userhistory = userdata[user_index[0]].linked_places
        for record in userhistory:
            history_records.append((record.place_name, record.feedback))
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


# def binary_search_places(places, target_country, target_weather, low, high):
#
#     quickSort2(places, 0, len(places) - 1, key=lambda x: (x.country.lower(), x.weather.lower()))
#
#     if low > high:
#         return []
#
#     mid = (low + high) // 2
#     country_matches = target_country is None or places[mid].country.lower() == target_country.lower()
#     weather_matches = target_weather is None or places[mid].weather.lower() == target_weather.lower()
#
#     if country_matches and weather_matches:
#         results = [places[mid]]
#
#         left = mid - 1
#         while left >= low and places[left].country.lower() == target_country.lower() and places[left].weather.lower() == target_weather.lower():
#             results.insert(0, places[left])
#             left -= 1
#
#         right = mid + 1
#         while right <= high and places[right].country.lower() == target_country.lower() and places[right].weather.lower() == target_weather.lower():
#             results.append(places[right])
#             right += 1
#         return results
#     elif places[mid].country.lower() < (target_country or '').lower() or places[mid].weather.lower() < (
#                     target_weather or '').lower():
#         return binary_search_places(places, target_country, target_weather, mid + 1, high)
#     else:
#         return binary_search_places(places, target_country, target_weather, low, mid - 1)

def binary_search_places(places, target_country=None, target_weather=None):
    if target_country is not None and target_weather is not None:
        key = lambda x: (x.country.lower(), x.weather.lower())
        target = (target_country.lower(), target_weather.lower())
    elif target_country is not None:
        key = lambda x: x.country.lower()
        target = target_country.lower()
    elif target_weather is not None:
        key = lambda x: x.weather.lower()
        target = target_weather.lower()
    else:
        key = lambda x: (x.country.lower(), x.weather.lower())
        target = None


    quickSort2(places, 0, len(places) - 1, key=key)

    if target is None:
        return places

    results = []
    low, high = 0, len(places) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = key(places[mid])

        if target_country and target_weather:
            compare_result = (mid_val[0] < target[0]) or (mid_val[0] == target[0] and mid_val[1] < target[1])
        else:
            compare_result = mid_val < target

        if compare_result:
            low = mid + 1
        else:
            if mid_val == target:
                results.append(places[mid])

                expand_search(mid, places, results, key, target)
            high = mid - 1

    return results

def expand_search(mid, places, results, key, target):

    left = mid - 1
    while left >= 0 and key(places[left]) == target:
        results.insert(0, places[left])
        left -= 1

    right = mid + 1
    while right < len(places) and key(places[right]) == target:
        results.append(places[right])
        right += 1


# Vote
def createVote(user_name,voted_place,feedback,place_list,userdata):
    quickSort(place_list,0,len(place_list)-1,lambda x:x.name)
    place_index = binary_search_all(place_list,0,len(place_list)-1,voted_place,lambda x:x.name if not isinstance(x, str) else x)

    if not place_index:
        return 0
    else:
        quickSort(userdata,0,len(userdata)-1,lambda x:x.username)
        user_index = binary_search_all(userdata,0,len(userdata)-1,user_name,lambda x:x.username if not isinstance(x, str) else x)
        if not user_index:
            user = User(user_name)
            user.linked_places.append(UserLinkedPlace(voted_place,feedback))
            userdata.append(user)

            place_list[place_index[0]].total_votes += 1
            place_list[place_index[0]].all_feedback.append(feedback)     
        else:
            user_linked_place = userdata[user_index[0]].linked_places
            quickSort(user_linked_place,0,len(user_linked_place)-1,lambda x:x.place_name)
            linked_place_index = binary_search_all(user_linked_place,0,len(user_linked_place)-1,voted_place,lambda x:x.place_name if not isinstance(x, str) else x)
            if not linked_place_index:
                userdata[user_index[0]].linked_places.append(UserLinkedPlace(voted_place,feedback))

                place_list[place_index[0]].total_votes += 1
                place_list[place_index[0]].all_feedback.append(feedback)
            else:
                return 1
    


# search history
# def findUserVoteHistory(username,userdata):
#     if userdata and len(userdata) > 1:
#         quickSort(userdata,0,len(userdata) - 1,lambda x:x.username)

#     target_index = binary_search_all(userdata,0,len(userdata)-1,username,key=lambda x:x.username if not isinstance(x, str) else x)


#     history_records = [] 

#     if not target_index:
#         return 1
#     else:
#         userhistory = userdata[target_index[0]].linked_places
#         for record in userhistory:
#             history_records.append((record.place_name, record.feedback))
#     return history_records



# top 10 voted country
def findTop3(place_list):
    quickSort(place_list,0,len(place_list)-1,lambda x:str(x.total_votes))
    top_place_list = place_list[-3:]
    top_place_name = []
    top_place_votes = []
    for place in top_place_list:
        top_place_votes.append(place.total_votes)
        top_place_name.append(place.name)
    return top_place_name, top_place_votes

# map data
def prepareMap(place_list):
    abb_country = [['AE', 'United Arab Emirates'], ['AF', 'Afghanistan'], ['AL', 'Albania'], ['AM', 'Armenia'], ['AO', 'Angola'], ['AR', 'Argentina'], ['AT', 'Austria'], ['AU', 'Australia'], ['AZ', 'Azerbaijan'], ['BA', 'Bosnia and Herzegovina'], ['BD', 'Bangladesh'], ['BE', 'Belgium'], ['BF', 'Burkina Faso'], ['BG', 'Bulgaria'], ['BI', 'Burundi'], ['BJ', 'Benin'], ['BN', 'Brunei Darussalam'], ['BO', 'Plurinational State of Bolivia'], ['BR', 'Brazil'], ['BT', 'Bhutan'], ['BW', 'Botswana'], ['BY', 'Belarus'], ['BZ', 'Belize'], ['CA', 'Canada'], ['CD', 'The Democratic Republic of the Congo'], ['CF', 'Central African Republic'], ['CG', 'Congo'], ['CH', 'Switzerland'], ['CI', 'Ivory Coast'], ['CL', 'Chile'], ['CM', 'Cameroon'], ['CN', 'China'], ['CO', 'Colombia'], ['CR', 'Costa Rica'], ['CU', 'Cuba'], ['CY', 'Cyprus'], ['CZ', 'Czech Republic'], ['DE', 'Germany'], ['DJ', 'Djibouti'], ['DK', 'Denmark'], ['DO', 'Dominican Republic'], ['DZ', 'Algeria'], ['EC', 'Ecuador'], ['EE', 'Estonia'], ['EG', 'Egypt'], ['EH', 'Western Sahara'], ['ER', 'Eritrea'], ['ES', 'Spain'], ['ET', 'Ethiopia'], ['FI', 'Finland'], ['FJ', 'Fiji'], ['FK', 'Falkland Islands (Malvinas)'], ['FR', 'France'], ['GA', 'Gabon'], ['GB', 'United Kingdom'], ['GE', 'Georgia'], ['GF', 'French Guiana'], ['GH', 'Ghana'], ['GL', 'Greenland'], ['GM', 'Gambia'], ['GN', 'Guinea'], ['GQ', 'Equatorial Guinea'], ['GR', 'Greece'], ['GT', 'Guatemala'], ['GW', 'Guinea-Bissau'], ['GY', 'Guyana'], ['HN', 'Honduras'], ['HR', 'Croatia'], ['HT', 'Haiti'], ['HU', 'Hungary'], ['ID', 'Indonesia'], ['IE', 'Ireland'], ['IL', 'Israel'], ['IN', 'India'], ['IQ', 'Iraq'], ['IR', 'Islamic Republic of Iran'], ['IS', 'Iceland'], ['IT', 'Italy'], ['JM', 'Jamaica'], ['JO', 'Jordan'], ['JP', 'Japan'], ['KE', 'Kenya'], ['KG', 'Kyrgyzstan'], ['KH', 'Cambodia'], ['KP', 'Democratic People’s Republic of Korea'], ['KR', 'Republic of Korea'], ['KW', 'Kuwait'], ['KZ', 'Kazakhstan'], ['LA', 'Lao People’s Democratic Republic'], ['LB', 'Lebanon'], ['LK', 'Sri Lanka'], ['LR', 'Liberia'], ['LS', 'Lesotho'], ['LT', 'Lithuania'], ['LU', 'Luxembourg'], ['LV', 'Latvia'], ['LY', 'Libyan Arab Jamahiriya'], ['MA', 'Morocco'], ['MD', 'Republic of Moldova'], ['MG', 'Madagascar'], ['MK', 'The Former Yugoslav Republic of Macedonia'], ['ML', 'Mali'], ['MM', 'Myanmar'], ['MN', 'Mongolia'], ['MR', 'Mauritania'], ['MW', 'Malawi'], ['MX', 'Mexico'], ['MY', 'Malaysia'], ['MZ', 'Mozambique'], ['NA', 'Namibia'], ['NC', 'New Caledonia'], ['NE', 'Niger'], ['NG', 'Nigeria'], ['NI', 'Nicaragua'], ['NL', 'Netherlands'], ['NO', 'Norway'], ['NP', 'Nepal'], ['NZ', 'New Zealand'], ['OM', 'Oman'], ['PA', 'Panama'], ['PE', 'Peru'], ['PG', 'Papua New Guinea'], ['PH', 'Philippines'], ['PK', 'Pakistan'], ['PL', 'Poland'], ['PR', 'Puerto Rico'], ['PS', 'Occupied Palestinian Territory'], ['PT', 'Portugal'], ['PY', 'Paraguay'], ['QA', 'Qatar'], ['RO', 'Romania'], ['RS', 'Serbia'], ['RU', 'Russian Federation'], ['RW', 'Rwanda'], ['SA', 'Saudi Arabia'], ['SB', 'Solomon Islands'], ['SD', 'Sudan'], ['SE', 'Sweden'], ['SJ', 'Svalbard and Jan Mayen'], ['SK', 'Slovakia'], ['SL', 'Sierra Leone'], ['SN', 'Senegal'], ['SO', 'Somalia'], ['SR', 'Suriname'], ['SV', 'El Salvador'], ['SY', 'Syrian Arab Republic'], ['SZ', 'Swaziland'], ['TD', 'Chad'], ['TG', 'Togo'], ['TH', 'Thailand'], ['TJ', 'Tajikistan'], ['TL', 'Timor-Leste'], ['TM', 'Turkmenistan'], ['TN', 'Tunisia'], ['TR', 'Turkey'], ['TZ', 'United Republic of Tanzania'], ['UA', 'Ukraine'], ['UG', 'Uganda'], ['US', 'United States'], ['UY', 'Uruguay'], ['UZ', 'Uzbekistan'], ['VE', 'Bolivarian Republic of Venezuela'], ['VN', 'Viet Nam'], ['VU', 'Vanuatu'], ['YE', 'Yemen'], ['ZA', 'South Africa'], ['ZM', 'Zambia'], ['ZW', 'Zimbabwe']]

    for i in range(len(place_list)):
        if isinstance(place_list[i].country, str):
            place_list[i].country = place_list[i].country.lower()


    quickSort(place_list,0,len(place_list)-1,lambda x:x.country)
    map_data = {}
    number = 0
    for country in abb_country:
        country_name_lower = country[1].lower()

        index = binary_search_all(place_list, 0, len(place_list) - 1, country_name_lower , key = lambda x:x.country if not isinstance(x, str) else x)
        votes = 0
        for i in index:
            votes += place_list[i].total_votes
        map_data[country[0]] = dict([("value",str(votes)),("index",str(number)),("stateInitColor","0")])
        number += 1
    return map_data


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

def is_file_empty(file_path):
    import os
    """检查文件是否为空"""
    try:
        return os.path.getsize(file_path) == 0
    except OSError:
        return True  # 文件不存在或无法访问


# def find_or_create_user(userdata, username):
#     """查找或创建用户，返回用户实例"""
#     for user in userdata:
#         if user.username == username:
#             return user
#     new_user = User(username)
#     userdata.append(new_user)
#     return new_user

# Load data
def load_data_from_files():
    userdata = []
    places = []
    if not is_file_empty('merged_data.txt'):
        with open('merged_data.txt', 'r', encoding='utf-8') as file:
            content = file.read()
            vote_history_section = content.split('[VOTE_HISTORY]\n')[-1].split('\n\n[PLACES]')[0].strip().split('\n')
            places_section = content.split('[PLACES]\n')[-1].strip().split('\n')


            for line in vote_history_section:
                if line.strip() == '':
                    continue
                username, place_name, feedback = line.strip().split('|')

                user_index = binary_search_all(userdata, 0, len(userdata) - 1, username, key=lambda x: x.username if not isinstance(x, str) else x)
                if not user_index:
                    new_user = User(username)
                    userdata.append(new_user)
                    quickSort(userdata, 0, len(userdata) - 1, lambda x: x.username)  # 保持排序状态
                else:
                    new_user = userdata[user_index[0]]

                new_user.linked_places.append(UserLinkedPlace(place_name, feedback))


            for line in places_section:
                if line.strip() == '':
                    continue
                name, country, weather, description, total_votes, feedback_str = line.strip().split('|')
                feedback_list = feedback_str.split(';') if feedback_str else []
                new_place = Place(name, country, weather, description)
                new_place.total_votes = int(total_votes)
                new_place.all_feedback = feedback_list
                places.append(new_place)

    return userdata, places

def update_places_file(place_list):
    with open('places.txt', 'w', encoding='utf-8') as file:
        for place in place_list:
            feedback_str = ";".join(place.all_feedback)  # Join all feedback with ';'
            file.write(
                f"{place.name}|{place.country}|{place.weather}|{place.description}|{place.total_votes}|{feedback_str}\n")

def update_users_file(remark):
    try:
        with open('users.txt', 'r+', encoding='utf-8') as file:
            existing_lines = file.readlines()
            existing_lines = [line.strip() for line in existing_lines]
            for entry in remark:
                new_record = f"{entry[0]}|{entry[1]}|{entry[2]}"
                if new_record not in existing_lines:
                    if not existing_lines:
                        file.write(new_record)
                    else:
                        file.write(f"\n{new_record}")
                    existing_lines.append(new_record)
    except FileNotFoundError:
        with open('users.txt', 'w', encoding='utf-8') as file:
            first_entry = remark[0]
            file.write(f"{first_entry[0]}|{first_entry[1]}|{first_entry[2]}")

def merge_and_clear_files():
    try:
        with open('merged_data.txt', 'r', encoding='utf-8') as file:
            merged_content = file.readlines()
    except FileNotFoundError:
        merged_content = []


    vote_history_section = []
    places_section = []
    current_section = None
    for line in merged_content:
        if '[VOTE_HISTORY]' in line:
            current_section = vote_history_section
        elif '[PLACES]' in line:
            current_section = places_section
        elif current_section is not None:
            current_section.append(line.strip())


    new_vote_history_content = open('users.txt', 'r', encoding='utf-8').read().strip().split('\n')
    new_places_content = open('places.txt', 'r', encoding='utf-8').read().strip().split('\n')


    for new_vote in new_vote_history_content:
        if new_vote and new_vote not in vote_history_section:
            vote_history_section.append(new_vote)


    updated_places = []
    for new_place_line in new_places_content:
        if new_place_line:
            new_place_parts = new_place_line.split('|')
            updated = False
            for i, existing_place_line in enumerate(places_section):
                existing_place_parts = existing_place_line.split('|')

                if new_place_parts[0] == existing_place_parts[0] and new_place_parts[1] == existing_place_parts[1]:

                    existing_feedback = set(existing_place_parts[-1].split(';'))
                    new_feedback = set(new_place_parts[-1].split(';'))
                    merged_feedback = existing_feedback.union(new_feedback)

                    existing_place_parts[-2] = str(len(merged_feedback))
                    existing_place_parts[-1] = ';'.join(merged_feedback)
                    places_section[i] = '|'.join(existing_place_parts)
                    updated = True
                    break
            if not updated:
                places_section.append(new_place_line)

    merged_data_content = '[VOTE_HISTORY]\n' + '\n'.join(vote_history_section) + '\n\n[PLACES]\n' + '\n'.join(places_section) + '\n'

    with open('merged_data.txt', 'w', encoding='utf-8') as file:
        file.write(merged_data_content)

    open('users.txt', 'w').close()
    open('places.txt', 'w').close()




def cal_number_of_places_and_votes(place_list):
    total_places_num = len(place_list)
    total_voted_places = sum(place.total_votes for place in place_list if place.total_votes > 0)
    return total_places_num,total_voted_places
# userdata,place_list = load_data_from_files()
# print(vars(place_list[1]))
