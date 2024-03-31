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

# System prompt as 'Jobgraph', guiding on CEO-related inquiries - this is a preamble to include in every API request
jobgraph_preamble = """
I am Jobgraph, your advisor on the role of Chief Executive Officer (CEO). I provide insights into what tasks a CEO does, how they're exposed to Large Language Models (LLMs), how the role might evolve with AI integration, and policies for future organizational efficiencies. My advice is focused on jobs and organizational strategy. For other topics, please consult ChatGPT.
"""

# Input from user
if prompt := st.chat_input("How can I assist you today?"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user's input as a chat message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Prepare the full prompt with preamble + user's input
    full_prompt = jobgraph_preamble + "\n\n" + prompt

    # Generate response from the assistant based on the full prompt
    with st.chat_message("assistant"):
        # Create the chat completion request including the preamble
        response = client.chat.create(
            model=st.session_state["openai_model"],
            messages=[
                # Here, the full_prompt includes the preamble for context
                {"role": "system", "content": jobgraph_preamble},
                {"role": "user", "content": prompt}
            ],
        )
        # Stream or display the response to the user
        # Note: Adjust st.write_stream(stream) to fit how you plan to display the API response
        st.write(response.choices[0].message['content'])  # Adjust based on how you handle API responses
    
    # Append the assistant's response to session state for continuity
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message['content']})