import streamlit as st
import pandas as pd

# Sample cutoff data — based on 1250 marks
DATA = {
    'College': [
        'Hindu College', 'Zakir Husain College', 'SRCC', 'JMI',
        'Kirori Mal College', 'Ramjas College', 'Miranda House', 'Hansraj College'
    ],
    'Course': [
        'BSc Physics Hons', 'BSc Physics Hons', 'BSc Math Hons', 'BSc Computer Science',
        'BSc Chemistry Hons', 'BSc Computer Science', 'BSc Chemistry Hons', 'BSc Math Hons'
    ],
    'Gen_Cutoff': [1100, 980, 1150, 1080, 1050, 1060, 1075, 1130],
    'Muslim_Cutoff': [1070, 950, 1120, 1050, 1020, 1030, 1045, 1100],
    'Defence_Cutoff': [1085, 960, 1135, 1065, 1035, 1045, 1060, 1115]
}
df = pd.DataFrame(DATA)

st.title("🎓 DU College Predictor (CUET-Based)")

# Sidebar inputs
st.sidebar.header("Enter Your CUET Marks (out of 250 each)")
phy = st.sidebar.number_input("Physics", min_value=0, max_value=250, value=125)
math = st.sidebar.number_input("Mathematics", min_value=0, max_value=250, value=125)
eng = st.sidebar.number_input("English", min_value=0, max_value=250, value=125)
cs = st.sidebar.number_input("Computer Science", min_value=0, max_value=250, value=125)
chem = st.sidebar.number_input("Chemistry", min_value=0, max_value=250, value=125)

category = st.sidebar.selectbox("Reservation Category", ["General", "Muslim", "Defence"])
course = st.sidebar.selectbox("Course", sorted(df['Course'].unique()))

# Total marks calculation
total_marks = phy + math + eng + cs + chem
st.write(f"### 📊 Your Total CUET Score: **{total_marks}/1250**")

# Filter data by course and category
cutoff_col = "Gen_Cutoff" if category == "General" else f"{category}_Cutoff"
filtered_df = df[df['Course'] == course][['College', cutoff_col]].copy()
filtered_df = filtered_df.rename(columns={cutoff_col: 'Cutoff'})

# Admission chance logic
filtered_df['Chance'] = filtered_df['Cutoff'].apply(
    lambda x: '✅ High' if total_marks >= x else (
        '⚠️ Moderate' if total_marks >= x - 30 else '❌ Low'
    )
)

st.write(f"### 🏫 Predicted Colleges for **{course}**")
st.table(filtered_df.reset_index(drop=True))
