# Web-Based Travel Survey System-Group 2
## Developer:
- Gao Ruihan -G2300276G
- Liu Yubin - G2300287B
- Hung Yui-Yeung - G2302633E
- Gong Xinyi - G2302498G
- Chen Xi - G2300290K
## About The Project
This project creates an online platform aimed at collecting global user interest and feedback on tourist spots. It allows users to propose new tourist interest points, vote for existing places, and provide valuable feedback based on their travel experiences. Additionally, the platform provides insights for the tourism industry by analyzing user data.
### Why Our Platform is Useful
#### For Users
- Enables travel enthusiasts to discover and share new tourist destinations.
- Enhances the personalization and interactivity of travel experiences.
#### For the Industry
- Provides valuable insights based on real user data.
- Contributes to the development and innovation of the industry.
## Main Features
There are 6 main functions in our platform:
1. **Add Place**: Allows users to add new places by providing details such as username, place name, country, weather, and description. Includes verification to avoid duplicates and updates filter options and place lists accordingly.
2. **View All Places**: Displays all places with their respective details.
3. **View Filtered Places**: Enables users to search for places based on specific criteria like country or weather, allowing for a narrowed down selection.
4. **Vote & Feedback**: Allows users to vote for their favorite place and provide feedback, ensuring a one-vote-per-location rule to prevent duplicates.
5. **View History**: Provides users with a history of their voted places, including place name and feedback. Users can search for their voting history by entering their name.
6. **View Data Analysis**: Offers data visualization graphs to analyze voting patterns, such as the number of votes for G7 countries, proportion of votes across continents, and more.

## Getting Started

### Prerequisites
- Python 3.11
- Flask

### Installation Steps

Follow these steps to install and run our project:

```bash
# Clone the repository
git clone https://github.com/Ruihan2001/AN6007-AJAX.git

# Navigate to the project directory
cd AN6007-AJAX

# Set up a virtual environment
python3 -m venv venv

# Activate the virtual environment
## Windows
venv\Scripts\activate
## MacOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
flask run