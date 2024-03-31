from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

jobgraph_preamble = """
I am Jobgraph, your advisor on the role of Chief Executive Officer (CEO). I provide insights into what tasks a CEO does, how they're exposed to Large Language Models (LLMs), how the role might evolve with AI integration, and policies for future organizational efficiencies. My advice is focused on jobs and organizational strategy. For other topics, please consult ChatGPT.
"""

# System prompt as 'Jobgraph', guiding on CEO-related inquiries
st.info("""
    **Welcome to Jobgraph!** I specialize in advising about the role of Chief Executive Officer (CEO). 
    I can help you understand:
    - What tasks a CEO typically handles.
    - How CEOs are likely exposed to Large Language Models (LLMs) and artificial intelligence.
    - How organizations might think about the CEO role changing in the future.
    - What kind of policies could be implemented to bring about positive changes and efficiencies.
    
    **Please note:** I am here to guide on matters related to jobs and organizations. For questions outside this scope, consider using ChatGPT for more general inquiries.
""")

# Input from user
if prompt := st.chat_input("How can I assist you today?"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user's input as a chat message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from the assistant based on the prompt
    with st.chat_message("assistant"):
        # Ensure conversation flow by including all prior messages
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{
                {
                    "role": "system", "content": jobgraph_preamble},
                    "role": m["role"],
                    "content": m["content"]
                } for m in st.session_state.messages],
            stream=True,
        )
        # Stream the response to the user
        response = st.write_stream(stream)
    
    # Append the assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": response})