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


# userdata = []
# ruihan = User('ruihan')
# ruihan.linked_places.append(UserLinkedPlace('Chengdu', 'delicious'))
# ruiyang = User('ruiyang')
# ruihan.linked_places.append(UserLinkedPlace('Hongkong', 'Expensive'))
# userdata.append(ruihan)
# userdata.append(ruiyang)


class Place:
    def __init__(self, name, country, weather, description):
        self.name = name
        self.country = country
        self.weather = weather
        self.description = description
        self.total_votes = 0
        self.all_feedback = []


def findUserHistory(username):
    quickSort(userdata,0,1,lambda x:x.username)
    target_index = binary_search(userdata,0,len(userdata),username,key=lambda x:x.username if not isinstance(x, str) else x)


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
    if places[mid].country.lower() == target_country.lower() and places[mid].weather.lower() == target_weather.lower():
        results = [places[mid]]
        # 向左查找所有匹配项
        left = mid - 1
        while left >= low and places[left].country.lower() == target_country.lower() and places[left].weather.lower() == target_weather.lower():
            results.insert(0, places[left])
            left -= 1
        # 向右查找所有匹配项
        right = mid + 1
        while right <= high and places[right].country.lower() == target_country.lower() and places[right].weather.lower() == target_weather.lower():
            results.append(places[right])
            right += 1
        return results
    elif (places[mid].country.lower(), places[mid].weather.lower()) < (target_country.lower(), target_weather.lower()):
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

def findUser():
    pass


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
            name, country, weather, description = line.strip().split(',')
            places.append(Place(name, country, weather, description))

    # 读取用户关联地点数据
    with open(user_linked_places_file, 'r', encoding='utf-8') as file:
        for line in file:
            username, place_name, feedback = line.strip().split(',')
            if username in userdata:
                username.linked_places.append(UserLinkedPlace(place_name, feedback))

    return userdata,places



def update_places_file(place_list):
    with open('places.txt', 'w', encoding='utf-8') as file:
        for place in place_list:
            file.write(f"{place.name},{place.country},{place.weather},{place.description}\n")


def update_vote_history_file(remark):
    with open('vote_history.txt', 'w', encoding='utf-8') as file:
        for entry in remark:
            user_name, voted_place, feedback = entry
            file.write(f"{user_name},{voted_place},{feedback}\n")






if __name__ == '__main__':
    userdata,places=load_data_from_files(user_file='users.txt', places_file='places.txt',
                         user_linked_places_file='user_linked_places.txt')
    userdata = []
    ruihan = User('ruihan')
    ruihan.linked_places.append(UserLinkedPlace('Chengdu','delicious'))
    ruiyang = User('ruiyang')
    ruihan.linked_places.append(UserLinkedPlace('Hongkong','Expensive'))
    userdata.append(ruihan)
    userdata.append(ruiyang)
    place1 = Place('1','2','3','4')
    place2 = Place('5', '6', '7', '8')
    places=[]
    places.append(place1)
    places.append(place2)
    print(places)
    print(binary_search_places(places, target_country='2', target_weather='Any',low = 0,high=len(places)-1))

    print(findUserHistory('ruihan'))
    print(findUserHistory('yubin'))

    