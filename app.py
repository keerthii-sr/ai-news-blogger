import streamlit as st
import requests
from groq import Groq
import smtplib

# Load API keys securely
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
NEWS_API = st.secrets["NEWS_API_KEY"]

st.title("📰 AI News Auto Blogger")

if st.button("Generate AI Blog"):

    # Fetch news
    url = f"https://newsapi.org/v2/everything?q=AI&apiKey={NEWS_API}"
    response = requests.get(url).json()

    articles = response['articles'][:3]

    news_text = ""
    for i, art in enumerate(articles):
        news_text += f"{i+1}. {art['title']}\n"

    st.write("🗞️ News Headlines:")
    st.write(news_text)

    # Generate blog
    prompt = f"Write a blog article based on this news:\n{news_text}"

    ai_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    blog = ai_response.choices[0].message.content

    st.subheader("✍️ Generated Blog")
    st.write(blog)

    # ✅ EMAIL CODE INSIDE BUTTON (IMPORTANT)
    sender = st.secrets["EMAIL"]
    receiver = st.secrets["EMAIL"]
    password = st.secrets["EMAIL_PASSWORD"]

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)

        server.sendmail(sender, receiver, blog)
        server.quit()

        st.success("📩 Email sent successfully!")

    except Exception as e:
        st.error(e)
