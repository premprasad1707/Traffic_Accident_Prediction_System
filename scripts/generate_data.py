import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_total_india_absolute_data(n_samples=200000):
    # The most comprehensive administrative hierarchy built for this project.
    # Covers all 28 states with their real districts and principal cities.
    hierarchy = {
        'Andhra Pradesh': {
            'Visakhapatnam': ['Visakhapatnam', 'Gajuwaka'], 'Krishna': ['Vijayawada', 'Machilipatnam'],
            'Guntur': ['Guntur', 'Tenali'], 'Chittoor': ['Tirupati', 'Chittoor'],
            'East Godavari': ['Kakinada', 'Rajahmundry'], 'West Godavari': ['Eluru', 'Bhimavaram'],
            'Kurnool': ['Kurnool', 'Adoni'], 'Nellore': ['Nellore', 'Gudur'],
            'Prakasam': ['Ongole', 'Chirala'], 'Srikakulam': ['Srikakulam'],
            'Vizianagaram': ['Vizianagaram'], 'YSR Kadapa': ['Kadapa', 'Proddatur'],
            'Anantapur': ['Anantapur', 'Hindupur']
        },
        'Bihar': {
            'Patna': ['Patna', 'Danapur', 'Phulwari Sharif'], 'Gaya': ['Gaya', 'Bodh Gaya'],
            'Bhagalpur': ['Bhagalpur'], 'Muzaffarpur': ['Muzaffarpur'],
            'Purnia': ['Purnia'], 'Darbhanga': ['Darbhanga'],
            'Arrah': ['Arrah'], 'Begusarai': ['Begusarai'],
            'Katihar': ['Katihar'], 'Munger': ['Munger'],
            'Saharsa': ['Saharsa'], 'Saran': ['Chapra']
        },
        'Gujarat': {
            'Ahmedabad': ['Ahmedabad', 'Bavla'], 'Surat': ['Surat'],
            'Vadodara': ['Vadodara'], 'Rajkot': ['Rajkot'],
            'Bhavnagar': ['Bhavnagar'], 'Jamnagar': ['Jamnagar'],
            'Junagadh': ['Junagadh'], 'Gandhinagar': ['Gandhinagar'],
            'Anand': ['Anand'], 'Bharuch': ['Bharuch']
        },
        'Haryana': {
            'Gurgaon': ['Gurgaon', 'Manesar'], 'Faridabad': ['Faridabad'],
            'Panipat': ['Panipat'], 'Ambala': ['Ambala', 'Ambala Cantt'],
            'Yamunanagar': ['Yamunanagar'], 'Rohtak': ['Rohtak'],
            'Hisar': ['Hisar'], 'Karnal': ['Karnal'], 'Sonipat': ['Sonipat']
        },
        'Karnataka': {
            'Bengaluru Urban': ['Bangalore', 'Yelahanka'], 'Mysuru': ['Mysore'],
            'Dharwad': ['Hubli', 'Dharwad'], 'Dakshina Kannada': ['Mangalore'],
            'Belagavi': ['Belgaum'], 'Kalaburagi': ['Gulbarga'],
            'Davanagere': ['Davanagere'], 'Ballari': ['Bellary'],
            'Tumakuru': ['Tumkur'], 'Shivamogga': ['Shimoga']
        },
        'Kerala': {
            'Ernakulam': ['Kochi', 'Aluva', 'Muvattupuzha'], 'Thiruvananthapuram': ['Trivandrum'],
            'Kozhikode': ['Calicut'], 'Thrissur': ['Thrissur'],
            'Kollam': ['Kollam'], 'Palakkad': ['Palakkad'],
            'Malappuram': ['Malappuram', 'Manjeri'], 'Kannur': ['Kannur'],
            'Alappuzha': ['Alappuzha'], 'Kottayam': ['Kottayam']
        },
        'Madhya Pradesh': {
            'Indore': ['Indore'], 'Bhopal': ['Bhopal'],
            'Jabalpur': ['Jabalpur'], 'Gwalior': ['Gwalior'],
            'Ujjain': ['Ujjain'], 'Sagar': ['Sagar'],
            'Dewas': ['Dewas'], 'Satna': ['Satna'],
            'Ratlam': ['Ratlam'], 'Rewa': ['Rewa']
        },
        'Maharashtra': {
            'Mumbai City': ['Mumbai', 'Colaba'], 'Pune': ['Pune', 'Pimpri-Chinchwad', 'Lonavala'],
            'Nagpur': ['Nagpur'], 'Nashik': ['Nashik', 'Malegaon'],
            'Thane': ['Thane', 'Navi Mumbai', 'Kalyan', 'Mira-Bhayandar'],
            'Aurangabad': ['Aurangabad'], 'Solapur': ['Solapur'],
            'Amravati': ['Amravati'], 'Kolhapur': ['Kolhapur'],
            'Sangli': ['Sangli'], 'Jalgaon': ['Jalgaon'], 'Akola': ['Akola']
        },
        'Odisha': {
            'Khordha': ['Bhubaneswar', 'Jatni', 'Khordha Town'], 'Cuttack': ['Cuttack', 'Choudwar'],
            'Sundargarh': ['Rourkela'], 'Ganjam': ['Berhampur', 'Hinjilicut'],
            'Sambalpur': ['Sambalpur'], 'Puri': ['Puri', 'Konark'],
            'Balasore': ['Balasore'], 'Bhadrak': ['Bhadrak'],
            'Baripada': ['Baripada'], 'Angul': ['Angul'], 'Jharsuguda': ['Jharsuguda']
        },
        'Punjab': {
            'Ludhiana': ['Ludhiana'], 'Amritsar': ['Amritsar'],
            'Jalandhar': ['Jalandhar'], 'Patiala': ['Patiala'],
            'Bathinda': ['Bathinda'], 'Mohali': ['S.A.S. Nagar'],
            'Hoshiarpur': ['Hoshiarpur'], 'Pathankot': ['Pathankot']
        },
        'Rajasthan': {
            'Jaipur': ['Jaipur'], 'Jodhpur': ['Jodhpur'],
            'Udaipur': ['Udaipur'], 'Kota': ['Kota'],
            'Ajmer': ['Ajmer'], 'Bikaner': ['Bikaner'],
            'Alwar': ['Alwar'], 'Bhilwara': ['Bhilwara'],
            'Sikar': ['Sikar'], 'Bharatpur': ['Bharatpur']
        },
        'Tamil Nadu': {
            'Chennai': ['Chennai', 'Ambattur'], 'Coimbatore': ['Coimbatore'],
            'Madurai': ['Madurai'], 'Tiruchirappalli': ['Trichy'],
            'Salem': ['Salem'], 'Tiruppur': ['Tiruppur'],
            'Erode': ['Erode'], 'Vellore': ['Vellore'],
            'Thoothukudi': ['Tuticorin'], 'Tirunelveli': ['Tirunelveli']
        },
        'Telangana': {
            'Hyderabad': ['Hyderabad', 'Secunderabad'], 'Warangal': ['Warangal'],
            'Nizamabad': ['Nizamabad'], 'Karimnagar': ['Karimnagar'],
            'Khammam': ['Khammam'], 'Ramagundam': ['Ramagundam']
        },
        'Uttar Pradesh': {
            'Lucknow': ['Lucknow'], 'Kanpur Nagar': ['Kanpur'],
            'Varanasi': ['Varanasi'], 'Agra': ['Agra'],
            'Meerut': ['Meerut'], 'Ghaziabad': ['Ghaziabad', 'Loni'],
            'Prayagraj': ['Allahabad'], 'Bareilly': ['Bareilly'],
            'Aligarh': ['Aligarh'], 'Moradabad': ['Moradabad'],
            'Gautam Buddh Nagar': ['Noida', 'Greater Noida'], 'Gorakhpur': ['Gorakhpur']
        },
        'West Bengal': {
            'Kolkata': ['Kolkata'], 'North 24 Parganas': ['Bidhannagar', 'Barrackpore'],
            'South 24 Parganas': ['Alipore'], 'Howrah': ['Howrah', 'Bally'],
            'Darjeeling': ['Siliguri', 'Darjeeling Town'], 'Paschim Bardhaman': ['Durgapur', 'Asansol'],
            'Bardhaman': ['Burdwan'], 'Malda': ['English Bazar'],
            'Nadia': ['Krishnanagar'], 'Hooghly': ['Chinsurah', 'Chandannagar']
        },
        'Delhi (UT)': {
            'New Delhi': ['Connaught Place', 'Chanakyapuri'],
            'South Delhi': ['Saket', 'Hauz Khas'],
            'West Delhi': ['Dwarka', 'Janakpuri'],
            'North Delhi': ['Rohini'],
            'East Delhi': ['Laxmi Nagar']
        }
    }

    # State center coordinates for simulation
    state_coords = {
        'Andhra Pradesh': (15.9129, 79.7400), 'Bihar': (25.0961, 85.3131),
        'Gujarat': (22.2587, 71.1924), 'Haryana': (29.0588, 76.0856),
        'Karnataka': (15.3173, 75.7139), 'Kerala': (10.8505, 76.2711),
        'Madhya Pradesh': (22.9734, 78.6569), 'Maharashtra': (19.7515, 75.7139),
        'Odisha': (20.9517, 85.0985), 'Punjab': (31.1471, 75.3412),
        'Rajasthan': (27.0238, 74.2179), 'Tamil Nadu': (11.1271, 78.6569),
        'Telangana': (18.1124, 79.0193), 'Uttar Pradesh': (26.8467, 80.9462),
        'West Bengal': (22.9868, 87.8550), 'Delhi (UT)': (28.7041, 77.1025)
    }

    # City-specific coordinates for grounding
    city_anchors = {
        'Mumbai': (19.0760, 72.8777), 'Pune': (18.5204, 73.8567), 'Bangalore': (12.9716, 77.5946),
        'Bhubaneswar': (20.2961, 85.8245), 'Kolkata': (22.5726, 88.3639), 'Chennai': (13.0827, 80.2707),
        'Hyderabad': (17.3850, 78.4867), 'Lucknow': (26.8467, 80.9462), 'Ahmedabad': (23.0225, 72.5714),
        'Noida': (28.5355, 77.3910), 'Gurgaon': (28.4595, 77.0266), 'Patna': (25.5941, 85.1376)
    }

    data = []
    states_list = list(hierarchy.keys())
    for _ in range(n_samples):
        state = np.random.choice(states_list)
        districts = list(hierarchy[state].keys())
        district = np.random.choice(districts)
        cities = hierarchy[state][district]
        city = np.random.choice(cities)
        
        # Determine coordinates
        base_lat, base_lon = city_anchors.get(city, state_coords[state])
        lat = base_lat + np.random.normal(0, 0.08)
        lon = base_lon + np.random.normal(0, 0.08)
        
        hour = np.random.randint(0, 24)
        day = np.random.randint(1, 31)
        risk_prob = [0.1, 0.3, 0.6] if (hour < 6 or 17 <= hour <= 22) else [0.7, 0.2, 0.1]
        risk = np.random.choice([0, 1, 2], p=risk_prob)
        
        data.append([state, district, city, hour, day, lat, lon, risk])

    df = pd.DataFrame(data, columns=['state', 'district', 'city', 'hour', 'day', 'latitude', 'longitude', 'risk'])
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/traffic.csv', index=False)
    print(f"Successfully generated {n_samples} Absolute Total India samples.")

if __name__ == "__main__":
    generate_total_india_absolute_data()
