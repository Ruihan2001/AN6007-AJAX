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



# ruihan = User('ruihan')
# ruihan.linked_places.append(UserLinkedPlace('Chengdu', 'delicious'))
# ruiyang = User('ruiyang')
# ruihan.linked_places.append(UserLinkedPlace('Hongkong', 'Expensive'))
# userdata.append(ruihan)
# userdata.append(ruiyang)

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


def binary_search_all(data, country, weather):
    result_indices = []

    def binary_search_recursive(start, end):
        if start > end:
            return

        mid = (start + end) // 2

        if data[mid].country == country and data[mid].weather == weather:
            result_indices.append(mid)

        binary_search_recursive(start, mid - 1)
        binary_search_recursive(mid + 1, end)

    binary_search_recursive(0, len(data) - 1)
    return result_indices

def filterPlaces():
    places = [
        Place("Place1", "Country1", "Weather1"),
        Place("Place2", "Country2", "Weather2"),
        Place("Place3", "Country3", "Weather3"),
    ]

    country_index = []
    weather_index = []

    for place in places:
        country_index.append((place.country, place))
        weather_index.append((place.weather, place))

    country_index.sort()
    weather_index.sort()

    def binary_search(sorted_list, target):
        pass

    target_country = "Country1"
    target_weather = "Weather2"

    result_country = binary_search(country_index, target_country)
    result_weather = binary_search(weather_index, target_weather)

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
        # 如果没有找到地点，可能需要处理错误或添加新地点
        print("Error: Place not found.")

    return 'ok'

def findUserVoteHistory(username, voted_place_name):
    # 使用二分查找法找到用户
    for user in userdata:
        print(user.username)
        if username == user.username:
            print('存在用户')
            quicksort(user.linked_places, 0, len(user.linked_places) - 1, key=lambda x: x.place_name)
            # 为了使用二分查找，确保linked_places已经根据place_name排序
            linked_places_sorted = sorted(user.linked_places, key=lambda x: x.place_name)
            place_index = binary_search_new(linked_places_sorted, 0, len(linked_places_sorted) - 1, voted_place_name,
                                            key=lambda x: x.place_name)

            return place_index != -1  # 如果找到了voted_place，返回True，否则返回False
        else:
            continue
    return False

def binary_search_new(arr, low, high, x, key=lambda x: x):
    if high >= low:
        mid = (high + low) // 2
        if key(arr[mid]) == x:
            return mid
        elif key(arr[mid]) > x:
            return binary_search_new(arr, low, mid - 1, x, key)
        else:
            return binary_search_new(arr, mid + 1, high, x, key)
    else:
        return -1

def quicksort(arr, low, high, key=lambda x: x):
    if low < high:
        pi = partition(arr, low, high, key)
        quicksort(arr, low, pi-1, key)
        quicksort(arr, pi+1, high, key)


def partition(array, low, high,key = lambda x:x):
  pivot = key(array[high]).lower()
  i = low - 1
  for j in range(low, high):
    if key(array[j]).lower() <= pivot:
      i = i + 1
      (array[i], array[j]) = (array[j], array[i])
  (array[i + 1], array[high]) = (array[high], array[i + 1])
  return i + 1



#
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


def binary_search(arr, low, high, x, key = lambda x:x if not isinstance(x, str) else x):
    """
    Please update the argument 'get_string' here in order to get the String for differnet element in array
    the format is - lambda x: x
    
    If found the wanted string, the function will return the index of element in array.
    Otherwise, the function will return -1
    """
    if high >= low:
        mid = (high + low) // 2

        if key(arr[mid]) == key(x):
            return mid
        
        elif key(arr[mid]) > key(x):
            return binary_search(arr, low, mid - 1, x, key)

        else:
            return binary_search(arr, mid + 1, high, x, key)

    else:
        return -1


def load_data_from_files(user_file='users.txt', places_file='places.txt', user_linked_places_file='user_linked_places.txt'):
    userdata = []
    places = []

    # 读取用户数据
    with open(user_file, 'r', encoding='utf-8') as file:
        for line in file:
            username = line.strip()
            userdata.append(User(username))

    # 读取地点数据
    with open(places_file, 'r', encoding='utf-8') as file:
        for line in file:
            name, country, weather, description, total_votes, feedback_str = line.strip().split(',')
            feedback_list = feedback_str.split(';') if feedback_str else []
            place = Place(name, country, weather, description)
            place.total_votes = int(total_votes)
            place.all_feedback = feedback_list
            places.append(place)

    # 读取用户关联地点数据
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







# if __name__ == '__main__':
#     userdata,places=load_data_from_files(user_file='users.txt', places_file='places.txt',
#                          user_linked_places_file='user_linked_places.txt')
#     userdata = []
#     ruihan = User('ruihan')
#     ruihan.linked_places.append(UserLinkedPlace('Chengdu','delicious'))
#     ruiyang = User('ruiyang')
#     ruihan.linked_places.append(UserLinkedPlace('Hongkong','Expensive'))
#     userdata.append(ruihan)
#     userdata.append(ruiyang)
#     place1 = Place('1','2','3','4')
#     place2 = Place('5', '6', '7', '8')
#     places=[]
#     places.append(place1)
#     places.append(place2)
#     print(places)
#     print(binary_search_places(places, target_country='2', target_weather='Any',low = 0,high=len(places)-1))
#
#     print(findUserHistory('ruihan'))
#     print(findUserHistory('yubin'))

    