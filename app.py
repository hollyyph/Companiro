import json
import gradio as gr
import numpy as np
import requests
import pandas as pd
import pymongo
import names
import random
import pickle

# Load model
filename = 'random_model_fixlengkap.pkl'
with open(filename, 'rb') as f:
    model = pickle.load(f)

# Mapping attribute
details = {
    "numToStr": {
        "gender": {
            "1": "Male",
            "2": "Female"
        },
        "field": {
            "1": "Law",
            "2": "Math",
            "3": "Social Science, Psychologist",
            "4": "Medical Science, Pharmaceuticals, and Bio Tech",
            "5": "Engineering",
            "6": "English/Creative Writing/ Journalism",
            "7": "History/Religion/Philosophy",
            "8": "Business/Econ/Finance",
            "9": "Education, Academia",
            "10": "Biological Sciences/Chemistry/Physics",
            "11": "Social Work",
            "12": "Undergrad/undecided",
            "13": "Political Science/International Affairs",
            "14": "Film",
            "15": "Fine Arts/Arts Administration",
            "16": "Languages",
            "17": "Architecture",
            "18": "Other"
        },
        "race": {
            "1": "Black/African American",
            "2": "European/Caucasian-American",
            "3": "Latino/Hispanic American",
            "4": "Asian/Pacific Islander/Asian-American",
            "5": "Native American",
            "6": "Other"
        },
        "go_out": {
            "1": "Several times a week",
            "2": "Twice a week",
            "3": "Once a week",
            "4": "Twice a month",
            "5": "Once a month",
            "6": "Several times a year",
            "7": "Almost never"
        },

        "date": {
            "1": "Several times a week",
            "2": "Twice a week",
            "3": "Once a week",
            "4": "Twice a month",
            "5": "Once a month",
            "6": "Several times a year",
            "7": "Almost never"
        },

        "goal": {
            "1": "Seemed like a fun night out",
            "2": "To meet new people",
            "3": "To get a date",
            "4": "Looking for a serious relationship",
            "5": "To say I did it",
            "6": "Other"
        },
        "career": {
            "1": "Lawyer",
            "2": "Academic/Research",
            "3": "Psychologist ",
            "4": "Doctor/Medicine",
            "5": "Engineer",
            "6": "Creative Arts/Entertainment",
            "7": "Banking/Consulting/Finance/Marketing/Business/CEO/Entrepreneur/Admin",
            "8": "Real Estate",
            "9": "International/Humanitarian Affairs",
            "10": "Undecided",
            "11": "Social Work",
            "12": "Speech Pathology",
            "13": "Politics",
            "14": "Pro sports/Athletics",
            "15": "Other",
            "16": "Journalism",
            "17": "Architecture"
        }


    },
    "strToNum": {
        "gender": {
            "Male": "1",
            "Female": "2"
        },
        "field": {
            "Law": "1",
            "Math": "2",
            "Social Science, Psychologist": "3",
            "Medical Science, Pharmaceuticals, and Bio Tech": "4",
            "Engineering": "5",
            "English/Creative Writing/ Journalism": "6",
            "History/Religion/Philosophy": "7",
            "Business/Econ/Finance": "8",
            "Education, Academia": "9",
            "Biological Sciences/Chemistry/Physics": "10",
            "Social Work": "11",
            "Undergrad/undecided": "12",
            "Political Science/International Affairs": "13",
            "Film": "14",
            "Fine Arts/Arts Administration": "15",
            "Languages": "16",
            "Architecture": "17",
            "Other": "18"

        },

        "race": {
            "Black/African American": "1",
            "European/Caucasian-American": "2",
            "Latino/Hispanic American": "3",
            "Asian/Pacific Islander/Asian-American": "4",
            "Native American": "5",
            "Other": "6"
        },

        "go_out": {
            "Several times a week": "1",
            "Twice a week": "2",
            "Once a week": "3",
            "Twice a month": "4",
            "Once a month": "5",
            "Several times a year": "6",
            "Almost never": "7"
        },
        "date": {
            "Several times a week": "1",
            "Twice a week": "2",
            "Once a week": "3",
            "Twice a month": "4",
            "Once a month": "5",
            "Several times a year": "6",
            "Almost never": "7"
        },

        "goal": {
            "Seemed like a fun night out": "1",
            "To meet new people": "2",
            "To get a date": "3",
            "Looking for a serious relationship": "4",
            "To say I did it": "5",
            "Other": "6"
        },
        "career": {
            "Lawyer": "1",
            "Academic/Research": "2",
            "Psychologist ": "3",
            "Doctor/Medicine": "4",
            "Engineer": "5",
            "Creative Arts/Entertainment": "6",
            "Banking/Consulting/Finance/Marketing/Business/CEO/Entrepreneur/Admin": "7",
            "Real Estate": "8",
            "International/Humanitarian Affairs": "9",
            "Undecided": "10",
            "Social Work": "11",
            "Speech Pathology": "12",
            "Politics": "13",
            "Pro sports/Athletics": "14",
            "Other": "15",
            "Journalism": "16",
            "Architecture": "17"
        }

    }
}

# Randomize users profile
users = []
for i in range(40):
    user = dict()
    if i % 2 == 0:
        gender_str = "female"
        gender = 2
    else:
        gender_str = "male"
        gender = 1
    
    user['name'] = names.get_full_name(gender=gender_str)
    user['gender'] = gender
    user['age'] = random.randint(20, 36)
    user['race'] = random.randint(1, 6)
    user['field'] = random.randint(1, 18)
    user['career'] = random.randint(1, 17)
    user['bio'] = "Hey!, I'm " + user['name']
    user['go_out'] = random.randint(1, 7)
    user['date'] = random.randint(1, 7)
    user['goal'] = random.randint(1, 6)
    user['imprace'] = random.randint(1, 10)
    user['imprelig'] = random.randint(1, 10)
    
    users.append(user)
    
with open('users.json', 'w') as fp:
    json.dump(users, fp)


def transform_str_to_num(user):
    transformed_user = {}
    transformed_user['name'] = user['name']
    transformed_user['gender'] = details['strToNum']['gender'][user['gender']]
    transformed_user['age'] = user['age']
    transformed_user['race'] = details['strToNum']['race'][user['race']]
    transformed_user['field'] = details['strToNum']['field'][user['field']]
    transformed_user['career'] = details['strToNum']['career'][user['career']]
    transformed_user['bio'] = user['bio']
    transformed_user['date'] = details['strToNum']['date'][user['date']]
    transformed_user['go_out'] = details['strToNum']['go_out'][user['go_out']]
    transformed_user['goal'] = details['strToNum']['goal'][user['goal']]
    transformed_user['imprace'] = user['imprace']
    transformed_user['imprelig'] = user['imprelig']
    
    return transformed_user


def transform_num_to_str(user):
    transformed_user = {}
    transformed_user['name'] = user['name']
    transformed_user['gender'] = details['numToStr']['gender'][str(user['gender'])]
    transformed_user['age'] = user['age']
    transformed_user['race'] = details['numToStr']['race'][str(user['race'])]
    transformed_user['field'] = details['numToStr']['field'][str(user['field'])]
    transformed_user['career'] = details['numToStr']['career'][str(user['career'])]
    transformed_user['bio'] = user['bio']
    transformed_user['date'] = details['numToStr']['date'][str(user['date'])]
    transformed_user['go_out'] = details['numToStr']['go_out'][str(user['go_out'])]
    transformed_user['goal'] = details['numToStr']['goal'][str(user['goal'])]
    transformed_user['imprace'] = user['imprace']
    transformed_user['imprelig'] = user['imprelig']
    
    return transformed_user


def merge_user(user1, user2):
    '''
    Transform data from user and partner by merging necessary info into a row
    '''
    age_o = user2['age']
    race_o = user2['race']
    age = user1['age']
    field_cd = user1['field']
    race = user1['race']
    imprace = user1['imprace']
    goal = user1['goal']
    career_c = user1['career']
    field_cd_o = user2['field']
    imprace_o = user2['imprace']
    goal_o = user2['goal']
    career_c_o = user2['career']
    go_out = user1['go_out']
    date = user1['date']
    imprelig = user1['imprelig']
    imprelig_o = user2['imprelig']
    samerace = int(race == race_o)
    go_out_o = user2['go_out']
    date_o = user2['date']
    
    return [samerace, age_o, race_o, age, field_cd, race, imprace, goal, career_c, field_cd_o, imprace_o, goal_o, career_c_o, go_out, date, imprelig, imprelig_o, go_out_o, date_o]


def find_partners(user):
    '''
    Take partners based on gender
    If the user is male, take the female users
    If the user is female, take the male users
    '''
    partners = []
    for partner in users:
        if str(user['gender']) == '1':
            if str(partner['gender']) == '2':
                partners.append(partner)
        elif str(user['gender']) == '2':
            if str(partner['gender']) == '1':
                partners.append(partner)   
    return partners

def recommendations(user, partners):
    '''
    Predict match probability for each partners 
    '''
    partners = np.array(partners)
    # Transform data type for prediction 
    X = []
    for p in partners:
        merge_result = merge_user(user, p)
        X.append(merge_result)
        
    # Predict the target 'match' 
    results = model.predict_proba(X)
    results = results.transpose()
    results = results[1]
    df_results = pd.DataFrame(results)
    df_results.rename(columns={0: "match"})
    transformed_partners = []
    
    # Transform partners before showing to the app
    for p in partners:
        transformed = transform_num_to_str(p)
        transformed_partners.append(transformed)
    df_partners = pd.DataFrame(transformed_partners)
    df_partners = pd.merge(df_partners, df_results, left_index=True, right_index=True)
    
    # Sort partners based on match label 
    sorted_partners = df_partners.sort_values(0, ascending=False)
    return sorted_partners


def produce_card(results):
    text_primary = ""
    for p in results:
        print(p)
        text = '''
{}, {}, {} years old
Field: {}
Career: {}
Bio: {}
        '''.format(p['name'], p['gender'], p['age'], p['field'], p['career'], p['bio'])
        text_primary = text_primary + text    
    return text_primary

def inputProfile(Name, Gender, Age, Race, Field, Career, Bio, GoOut, Date, Goal, ImpRelig, ImpRace):
    new_user = dict()
    new_user['name'] = Name
    new_user['gender'] = Gender
    new_user['age'] = Age
    new_user['race'] = Race
    new_user['field'] = Field
    new_user['career'] = Career
    new_user['bio'] = Bio
    new_user['go_out'] = GoOut
    new_user['date'] = Date
    new_user['goal'] = Goal
    new_user['imprace'] = ImpRelig
    new_user['imprelig'] = ImpRace
    
    transformed_user = transform_str_to_num(new_user)
    partners = find_partners(transformed_user)
    results = recommendations(transformed_user, partners)
    
    dict_results = results.to_dict('records')
    
    fix_results = produce_card(dict_results)

    return fix_results

# Interface
demo = gr.Interface(
    inputProfile,
    title="Companero",
    description="Input your Profile, Behavior, and Preferences here!",
    inputs = [
        gr.Textbox(lines=1, placeholder="Your name here..."),
        gr.Radio(["Male", "Female"]),
        gr.Slider(20, 35),
        gr.Radio(["Black/African American",
                "European/Caucasian-American",
                "Latino/Hispanic American",
                "Asian/Pacific Islander/Asian-American",
                "Native American",
                "Other"]),
        gr.Radio(["Law",
                "Math",
                "Social Science, Psychologist",
                "Medical Science, Pharmaceuticals, and Bio Tech", 
                "Engineering",  
                "English/Creative Writing/ Journalism", 
                "History/Religion/Philosophy", 
                "Business/Econ/Finance", 
                "Education, Academia", 
                "Biological Sciences/Chemistry/Physics",
                "Social Work", 
                "Undergrad/undecided",
                "Political Science/International Affairs", 
                "Film",
                "Fine Arts/Arts Administration",
                "Languages",
                "Architecture",
                "Other"]),
        gr.Radio(["Lawyer",
                "Academic/Research",
                "Psychologist ",
                "Doctor/Medicine",
                "Engineer",
                "Creative Arts/Entertainment",
                "Banking/Consulting/Finance/Marketing/Business/CEO/Entrepreneur/Admin",
                "Real Estate",
                "International/Humanitarian Affairs",
                "Undecided",
                "Social Work",
                "Speech Pathology",
                "Politics",
                "Pro sports/Athletics",
                "Other",
                "Journalism",
                "Architecture"]),
        gr.Textbox(lines=5, placeholder="Your bio description here..."),
        gr.Radio(["Several times a week",
                  "Twice a week",
                  "Once a week",
                  "Twice a month",
                  "Once a month",
                  "Several times a year",
                  "Almost never",]),
        gr.Radio(["Several times a week",
                  "Twice a week",
                  "Once a week",
                  "Twice a month",
                  "Once a month",
                  "Several times a year",
                  "Almost never",]),
        gr.Radio(["Seemed like a fun night out",
                "To meet new people",
                "To get a date",
                "Looking for a serious relationship",
                "To say I did it",
                "Other"]),
        gr.Slider(0, 10),
        gr.Slider(0, 10)
    ],
    outputs = "text"    
)

demo.launch(share=True)

