import streamlit as st
from langchain import PromptTemplate
from langchain import OpenAI
#import config

#openai_api_key = config.OPEN_AI_KEY
openai_api_key = st.secrets["API_KEY"]

#prompt template to pass to langchain
template = """
    Below is an example of a tweet. Your goal is to:
    -construct a thoughtful and engaging reply to the below tweet. The tone of the tweet should be {tone}
    -if the tweet is a question, craft a reply to the question being asked
    -if the tweet is a statement, craft a reply that carries on the conversation
    -make it relevant to the tweet that is being replied to
    -Address the main points of the tweet.
    -Use concise and clear language
    -do not include hashtags or the charactor #

    Here are some examples of tweets and replies in different tones:
    -Tweet #1: Happy monday! Mondays are the worst.
    -Funny reply #1: If only I could be as productive as I am when I'm avoiding work.
    -Formal reply #1: I recognize that I could improve my productivity, and I am actively seeking ways to do so.
    -Tweet #2: What are you grateful for today?
    -Funny reply #2: I'd like to thank my morning coffee for giving me the motivation to pretend like I know what I'm doing.
    -Formal reply #2: I am grateful for the caffeine boost provided by my morning coffee, which allows me to approach my work with confidence.

    Below is the tweet and tone:
    TONE: {tone}
    TWEET: {tweet}
"""
prompt = PromptTemplate(
    input_variables=["tone", "tweet"],
    template=template,
)

#define and load the model
def load_LLM():
    """Logic for loading the chain you want to use should go here"""
    llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.7, openai_api_key=openai_api_key)
    return llm

llm = load_LLM()

#page header
st.set_page_config(page_title="Tweet Replier", page_icon=":robot:")
st.header("Tweet Replier")

#columns for the content
col1, col2 = st.columns(2)

with col1:
    st.markdown("Do you ever struggle to know how to reply to a tweet? Tweet Replier takes care of it for you! Powered by ChatGPT 3.5 and            LangChain, Tweet Replier will help you craft the perfect response tweet.")

with col2:
    st.image(image="Asset 1.png", width=303)

#st.markdown("OpenAI API Key")

#def get_API():
#    u_key = st.text_input(label="", placeholder="Enter API Key...")
#    return u_key
#openai_api_key = get_API()


#tweet entry field
st.markdown("## Enter The Tweet You Would Like To Reply To")

#tone selector
col1, col2 = st.columns(2)
with col1:
    option_tone = st.selectbox(
        "Which tone do you want your tweet to have?",
        ("Formal", "Playful")
    )

#input function to pass to langchain
def get_text():
    input_text = st.text_area(label="", placeholder="The tweet to reply to...", key="tweet_input")
    return input_text

tweet_input = get_text()

#st.write(tweet_input)

st.markdown("## Your Tweet Response:")

if tweet_input:
    prompt_with_tweet = prompt.format(tone=option_tone, tweet=tweet_input)

    formatted_tweet = llm(prompt_with_tweet)

    st.write(formatted_tweet)
