import streamlit as st
import requests
import json
import openai

# Function to get token
def get_token():
    url = 'https://megatechapi.com:9098/api/Account/login/'
    data = {
        "email": "pasban.rad@megatechapi.com",
        "password": "##radpasban@@"
    }
    response = requests.post(url, json=data)
    token = json.loads(response.text)['token']
    return token

# Function to fetch driver information
def fetch_driver_info(get_id, token):
    userId = get_id
    access_token = token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://megatechapi.com:9098/api/Dashboard/get-counters/1"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data['Detail']:
            if d['UserId'] == get_id:
                return d
    else:
        return None

# Function to fetch trainee information
def get_trainee_info(id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = "https://Megatechapi.com:9098/api/Pasban/get-AllHSEManualTraining"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data:
            if d['Id'] == id:
                return d
    else:
        return None

def business_vehicle_count(city_name, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://megatechapi.com:9098/api/Dashboard/get-masterGraph-detailData/{city_name}"
    response = requests.get(url, headers=headers, verify=False)
    data = json.loads(response.text)
    return data

def pasban_user_info(id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = "https://Megatechapi.com:9098/api/MobileApp/get-allPasbanUsersInfo"
    response = requests.get(url, headers=headers, verify=False)
    data = json.loads(response.text)
    for d in  data:
        if d['driverId'] == str(id):
            return d

def user_vehicle_information(id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = "https://Megatechapi.com:9098/api/Pasban/get-AllUserWithVehicleCurrentStatus"
    response = requests.get(url, headers=headers, verify=False)
    data = json.loads(response.text)
    for d in data:
        if d['UserId'] == id:
            return d

def fetch_LTO_info(UserId, token):
    headers = { 
        "Authorization": f"Bearer {token}"
    }
    url = "https://megatechapi.com:9098/api/Dashboard/get-lto-counters/1"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data['Detail']:
            if d['userid'] == UserId:
                return d

def all_tracker_status(regno, token):
    headers = { 
        "Authorization": f"Bearer {token}" 
    }
    url = "https://Megatechapi.com:9098/api/Pasban/get-allTrackersStatus"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data:
            if d['Regno'] == regno:
                return d
    else:
        return None

def fetch_vehicle_info(UserId, token):
    headers = {
        "Authorization": f"Bearer {token}" 
    }
    url = "https://Megatechapi.com:9098/api/Pasban/get-allVehicleMasterData"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data:
            if d['Id'] == UserId:
                return d
    else:
        return None

def fetch_transfer_status(UserId, token):
    headers = {
        "Authorization": f"Bearer {token}" 
    }
    url = "https://Megatechapi.com:9098/api/Pasban/get-allTransferStatuses"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data:
            if d['Id'] == UserId:
                return d
    else:
        return None

# Function to fetch NDII_IID user information
def fetch_user_info(UserId, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = "https://Megatechapi.com:9098/api/NDII_IID"
    response = requests.get(url, headers=headers, verify=False)
    
    if response.status_code == 200:
        data = json.loads(response.text)
        for d in data:
            if d['UserId'] == UserId:
               return d
    else:
        return None

# Function to generate bot response
def generate_answer(question, context):
    openai.api_key = "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"
    prompt = f"Question: {question}\nContext: {context}\nAnswer:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

# Streamlit app
def main():
    st.sidebar.title("API Selection")
    options = ["Driver Information", "Training Information", "Business Vehicle Information", 'Pasban User Info', 'Employee Vehicle Information',
               'All Tracker Status', 'NDII_IID User Info', 'Vehicle Master Data', 'LTO Information', "Transfer Status"]
    selected_option = st.sidebar.selectbox("Select API", options)

    token = get_token()
    if selected_option == 'Driver Information':
        question = ''
        user_id = st.number_input("Enter UserId:", step=1)
        if user_id:
            user_info = fetch_driver_info(int(user_id), token)
        question = st.text_input("What would you like to know?")
        if question:
            context = f"""You are a friendly sincere chatbot. This is all about the user details,
                    You can be asked for about:
                    {list(user_info.keys())}
                    You can get all the information below
                    {user_info}
                    """
            result = generate_answer(question, context)
            st.write(result)

    if selected_option == 'Training Information':
        question = ''
        user_id = st.number_input("Enter UserId:", step=1)
        if user_id:
            trainee_info = get_trainee_info(int(user_id), token)
            question = st.text_input("What would you like to know?")
            if question:
                context = f"""You are a friendly sincere chatbot. This is all about the user details,
                        You can be asked for about:
                        {list(trainee_info.keys())}
                        You can get all the information below
                        {trainee_info}
                        """
                result = generate_answer(question, context)
                st.write(result)

    if selected_option == 'Business Vehicle Information':
        question = ''
        selected_city = st.selectbox("Select a city:", ["None", "Karachi", "Lahore", "Islamabad"])
        if selected_city != 'None':
            business_vehicle_info = business_vehicle_count(selected_city, token)
            question = st.text_input("What would you like to know?")
            if question:
                context = f"""You are a friendly sincere chatbot. This is all about the user details,
                            You can be asked for about:
                            {list(business_vehicle_info.keys())}
                            You can get all the information below
                            {business_vehicle_info}
                            """
                result = generate_answer(question, context)
                st.write(result)

    if selected_option == 'Pasban User Info':
        question = ''
        user_id = ''
        user_id = st.number_input("Enter UserId:", step=1)
        if user_id:
            pasban_user = pasban_user_info(int(user_id), token)
            question = st.text_input("What would you like to know?")
            if question:
                context = f"""You are a friendly sincere chatbot. This is all about the user details,
                            You can be asked for about:
                            {list(pasban_user.keys())}
                            You can get all the information below
                            {pasban_user}
                            """
                result = generate_answer(question, context)
                st.write(result)

    if selected_option == 'Employee Vehicle Information':
        question = ''
        user_id = ''
        user_id = st.text_input("Enter UserId:")
        if user_id:
            vehicle_user = user_vehicle_information(user_id, token)
            question = st.text_input("What would you like to know?")
            if question:
                context = f"""You are a friendly sincere chatbot. This is all about the user details,
                            You can be asked for about:
                            {list(vehicle_user.keys())}
                            You can get all the information below
                            {vehicle_user}
                            """
                result = generate_answer(question, context)
                st.write(result)

    if selected_option == 'NDII_IID User Info':        
        user_id = st.number_input("Enter UserId:", step=1)        
        if user_id:            
            NDII_info = fetch_user_info(int(user_id), token)            
            question = st.text_input("What would you like to know?")            
            if question:                
                context = f"""You are a friendly sincere chatbot. This is all about the user details,                    
                You can be asked for about:                    
                {list(NDII_info.keys())}                    
                You can get all the information below                    
                {NDII_info}    
                """
                
                result = generate_answer(question, context)                
                st.write(result)     

    if selected_option == "Vehicle Master Data":        
        user_id = st.number_input("Enter UserId:", step=1)        
        if user_id:            
            vehicle_info = fetch_vehicle_info(int(user_id), token)            
            question = st.text_input("What would you like to know?")            
            if question:                
                context = f"""You are a friendly sincere chatbot. This is all about the user details,                    
                You can be asked for about:                    
                {list(vehicle_info.keys())}                    
                You can get all the information below                    
                {vehicle_info}    
                """
                
                result = generate_answer(question, context)                
                st.write(result)     

    if selected_option == "LTO Information":        
        user_id = st.number_input("Enter UserId:", step=1)        
        if user_id:            
            LTO_info = fetch_LTO_info(int(user_id), token)            
            question = st.text_input("What would you like to know?")            
            if question:                
                context = f"""You are a friendly sincere chatbot. This is all about the user details,                    
                You can be asked for about:                    
                {list(LTO_info.keys())}                    
                You can get all the information below                    
                {LTO_info}    
                """
                
                result = generate_answer(question, context)                
                st.write(result)     

    if selected_option == "All Tracker Status":        
        regno = st.text_input("Enter Registration No.:")        
        if regno:            
            tracker_info = all_tracker_status(str(regno), token)            
            question = st.text_input("What would you like to know?")            
            if question:                
                context = f"""You are a friendly sincere chatbot. This is all about the user details,                    
                You can be asked for about:                    
                {list(tracker_info.keys())}                    
                You can get all the information below                    
                {tracker_info}    
                """
                
                result = generate_answer(question, context)                
                st.write(result)     
    
    if selected_option == "Transfer Status":        
        user_id = st.number_input("Enter UserId:", step=1)        
        if user_id:            
            transfer_info = fetch_transfer_status(int(user_id), token)            
            question = st.text_input("What would you like to know?")            
            if question:                
                context = f"""You are a friendly sincere chatbot. This is all about the user details,                    
                You can be asked for about:                    
                {list(transfer_info.keys())}                    
                You can get all the information below                    
                {transfer_info}    
                """
                
                result = generate_answer(question, context)                
                st.write(result)

if __name__ == "__main__":
    main()



#cd C:\Users\WAQSA\anaconda3\Scripts
#streamlit run "E:\Unilever\New folder\app (1).py"