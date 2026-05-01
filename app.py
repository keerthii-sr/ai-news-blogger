import streamlit as st
import requests
from groq import Groq
import smtplib

# API Keys
NEWS_API = "8390c1e44dcf43e9ab7f69ec5101aa07"
client = Groq(api_key="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")

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

    # AI blog generation
    prompt = f"Write a blog article based on this news:\n{news_text}"

    ai_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    blog = ai_response.choices[0].message.content

    st.subheader("✍️ Generated Blog")
    st.write(blog)

sender = "keerthigowda366@gmail.com"
receiver = "komalsingh2444@gmail.com"
password = "cvwlkrcriafrvurn"

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, password)

    server.sendmail(sender, receiver, blog)
    server.quit()

    st.success("📩 Email sent successfully!")

except Exception as e:
    st.error(e)