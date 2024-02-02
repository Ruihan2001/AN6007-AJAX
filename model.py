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


userdata = []
ruihan = User('ruihan')
ruihan.linked_places.append(UserLinkedPlace('Chengdu', 'delicious'))
ruiyang = User('ruiyang')
ruihan.linked_places.append(UserLinkedPlace('Hongkong', 'Expensive'))
userdata.append(ruihan)
userdata.append(ruiyang)


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

get_string = lambda place: place.country + place.weather
def binary_search_all(data, country, weather):
        result_indices = []
        sorted_data = quickSort(data, 0, len(data) - 1, get_string)
        print("Hi",sorted_data)
        def binary_search_recursive(start, end):
            if start > end:
                return

            mid = (start + end) // 2
            mid_value = get_string(sorted_data[mid])

            if mid_value == country + weather:
                result_indices.append(mid)
                # 向左搜索更多匹配项
                left = mid - 1
                while left >= start and get_string(sorted_data[left]) == mid_value:
                    result_indices.append(left)
                    left -= 1
                # 向右搜索更多匹配项
                right = mid + 1
                while right <= end and get_string(sorted_data[right]) == mid_value:
                    result_indices.append(right)
                    right += 1
            elif mid_value < country + weather:
                binary_search_recursive(mid + 1, end)
            else:
                binary_search_recursive(start, mid - 1)

        binary_search_recursive(0, len(sorted_data) - 1)
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
    
# if __name__ == '__main__':
#     userdata = []
#     ruihan = User('ruihan')
#     ruihan.linked_places.append(UserLinkedPlace('Chengdu','delicious'))
#     ruiyang = User('ruiyang')
#     ruihan.linked_places.append(UserLinkedPlace('Hongkong','Expensive'))
#     userdata.append(ruihan)
#     userdata.append(ruiyang)
#
#
#     print(findUserHistory('ruihan'))
#     # print(findUserHistory('yubin'))

    