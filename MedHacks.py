import streamlit as st
import streamlit.components.v1 as components
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Store session state variables for user registration and symptom tracking
if "registered" not in st.session_state:
    st.session_state.registered = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "chronic_illness" not in st.session_state:
    st.session_state.chronic_illness = ""
if "symptom_logs" not in st.session_state:
    st.session_state.symptom_logs = []

# Function to generate AI responses
def ai_support():
    st.header("AI Support")
    components.html("""
        <script> 
            window.chtlConfig = { chatbotId: "9312791544", display: "page_inline" }; 
        </script>
        <div id="chatling-inline-bot" style="width: 100%; height: 500px;"></div>
        <script async data-id="9312791544" id="chatling-embed-script" type="text/javascript" src="https://chatling.ai/js/embed.js"></script>
    """, height=550)

# Register new users
def register(username, password, chronic_illness):
    st.session_state.registered = True
    st.session_state.current_user = username
    st.session_state.chronic_illness = chronic_illness
    st.success(f"You have successfully created your portal, {username}! You have {chronic_illness}.")

# Log a new symptom entry
def log_symptom(symptom, severity, notes):
    st.session_state.symptom_logs.append({
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),  # Log only the date
        "symptom": symptom,
        "severity": severity,
        "notes": notes
    })
    st.success("Symptom entry logged successfully!")

# Display the symptom graph
def show_symptom_graph():
    if st.session_state.symptom_logs:
        df = pd.DataFrame(st.session_state.symptom_logs)
        df['severity'] = df['severity'].astype(int)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')

        plt.figure(figsize=(12, 6))  # Increase size of the graph
        plt.plot(df['date'], df['severity'], marker='o', linestyle='-')

        # Annotate each point with the symptom name
        for i, row in df.iterrows():
            plt.annotate(row['symptom'], (row['date'], row['severity']),
                         textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8)

        plt.xlabel('Date (Month/Date)', fontsize=10)
        plt.ylabel('Severity', fontsize=10)
        plt.title('Symptom Severity Over Time', fontsize=12)

        # Set smaller font for x-axis date labels
        plt.xticks(rotation=45, fontsize=8)

        st.pyplot(plt.gcf())
    else:
        st.warning("No symptom logs available to display.")

# Generate suggestions based on trend
def generate_suggestion():
    if len(st.session_state.symptom_logs) > 1:
        df = pd.DataFrame(st.session_state.symptom_logs)
        df['severity'] = df['severity'].astype(int)
        trend = df['severity'].diff().dropna()

        if trend.iloc[-1] > 2:  # Rapid increase
            return "It's a good idea to consult a doctor. You're symptoms are increasing rather rapidly."
            
        elif trend.iloc[-1] < 0:  # Decrease
            return "You're doing great! Keep maintaining your current routine."
        else:
            return "Your symptoms are stable. Continue to monitor and record."
    else:
        return "Insufficient data to generate suggestions."

# User interface for registration
st.title("Compassionate Chronic Care Community")
components.html("""
    <div style="display: flex; justify-content: center;">
        <script src="https://unpkg.com/@dotlottie/player-component@latest/dist/dotlottie-player.mjs" type="module"></script>
        <dotlottie-player 
            src="https://lottie.host/ae6d644f-f15a-44a7-9170-7449b21cd5b9/o1pT3ExXGB.json" 
            background="transparent" 
            speed="1" 
            style="width: 500px; height: 500px" 
            direction="1" 
            playMode="normal" 
            loop 
            autoplay>
        </dotlottie-player>
    </div>
""", height=400)
st.markdown("<hr>", unsafe_allow_html=True)

if not st.session_state.registered:
    st.subheader("Register to Access Your Health Portal", anchor="register")
    
    # Input fields 
    username = st.text_input("Username: ",key="username_input", placeholder="Enter your username")
    password = st.text_input("Password: ", type="password", key="password_input", placeholder="Enter your password")
    
    # Dropdown for chronic illness selection
    chronic_conditions = [
        "Diabetes", "PCOS", "Celiac", "Hypertension", "Asthma",
        "Arthritis", "Migraines", "IBS", "Chronic Fatigue Syndrome",
        "Heart Disease", "Multiple Sclerosis", "Epilepsy", "Cancer", "Other"
    ]
    chronic_illness = st.selectbox("Select Your Chronic Illness", chronic_conditions)

    if chronic_illness == "Other":
        chronic_illness_other = st.text_input("Please specify your condition (if other):")
        chronic_illness = chronic_illness_other if chronic_illness_other else ""

    if st.button("Register", key="register_button"):
        register(username, password, chronic_illness)
else:
    st.title(f"{st.session_state.current_user}'s Health Portal")  # User's title

    # Tabs for different sections of the app
    ai_tab, symptom_tracker_tab, find_doctors_tab, expert_resources_tab, logout_tab = st.tabs([
        "AI Support", "Symptom Tracker", "Find Doctors", "Expert Resources", "Logout"
    ])

    with symptom_tracker_tab:
        st.subheader("Log a New Symptom")
        symptom_date = st.date_input("Date of Symptom Entry")
        symptom = st.text_input("Symptom")
        severity = st.slider("Severity (1-10)", min_value=1, max_value=10)
        notes = st.text_area("Additional Notes")
        if st.button("Submit Symptom", key="submit_symptom"):
            log_symptom(symptom, severity, notes)

        # Display the symptom log
        if st.session_state.symptom_logs:
            st.subheader("Symptom Log")
            log_df = pd.DataFrame(st.session_state.symptom_logs)
            st.dataframe(log_df[['date', 'symptom', 'severity', 'notes']])

        if st.button("Generate Graph", key="generate_graph"):
            show_symptom_graph()
            suggestion = generate_suggestion()
            st.write(suggestion)

    with ai_tab:
        ai_support()


    with find_doctors_tab:
    # Replace spaces in chronic illness with '%20' for the URL to handle spaces correctly
        illness = st.session_state.chronic_illness.replace(" ", "%20")
    
        urlpt1 = f"https://doctor.webmd.com/results?entity=all&q={illness}&pagenumber=1&pt=34.71,-86.7517&d=40&city=Madison&state=AL"
    
        st.subheader("Find Doctors Near You")
        st.markdown(f"""
        <iframe src="{urlpt1}" width="800" height="600" style="border:none;"></iframe>
        """, unsafe_allow_html=True)



    with expert_resources_tab:
        st.subheader("Expert Resources")
        st.write(f"Resources for {st.session_state.chronic_illness}")
        cdc_query = st.session_state.chronic_illness.replace(" ", "%20")  # Handle spaces in chronic illness name
        cdc_url = f"https://www.cdc.gov/search/index.html?query={cdc_query}"
        st.markdown(f"""
        <iframe src="{cdc_url}" width="800" height="600" style="border:none;"></iframe>
        """, unsafe_allow_html=True)
        # Hinge Health embedded search URL
        hinge_health_url = f"https://hingehealth.com/?query={illness}"
    
        st.subheader("Learn More from Hinge Health")
        st.markdown(f"""
        <iframe src="{hinge_health_url}" width="800" height="600" style="border:none;"></iframe>
        """, unsafe_allow_html=True)

        # YouTube search embed for diabetes
        youtube_search_url = "https://www.youtube.com/results?search_query=diabetes"
        youtube_embed_url = "https://www.youtube.com/embed/videoseries?search_query=diabetes"
    
        st.subheader("Explore Videos on YouTube")
        st.markdown(f"""
        <iframe width="800" height="600" src="{youtube_embed_url}" frameborder="0" allowfullscreen></iframe>
        """, unsafe_allow_html=True)
    

    with logout_tab:
        st.subheader("Logout")
        st.write("You can log out from your account here.")
        if st.button("Logout", key="logout_button"):
            st.session_state.registered = False
            st.session_state.current_user = ""
            st.session_state.chronic_illness = ""
            st.session_state.symptom_logs = []
            st.success("You have successfully logged out.")
