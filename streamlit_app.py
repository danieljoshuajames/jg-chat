from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo-0125"

# Display an introductory message without adding it to the session state messages
st.info("""
    **Welcome to Jobgraph!** I specialize in advising about the role of Chief Executive Officer (CEO). What would you like to know?
""")

# Define the Jobgraph system prompt
jobgraph_system_prompt = """
I am Jobgraph, your advisor on the role of Chief Executive Officer (CEO). I provide insights into what tasks a CEO does, how they're exposed to Large Language Models (LLMs), how the role might evolve with AI integration, and policies for future organizational efficiencies. My advice is focused on jobs and organizational strategy. For other topics, please consult ChatGPT.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    # Ensure system prompts are not displayed in the GUI
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input from user
if prompt := st.chat_input("How can I assist you today?"):
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Include the system prompt for context when generating the response, but do not display it
    combined_messages = [{"role": "system", "content": jobgraph_system_prompt}] + \
                        [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"] != "system"]

    # Generate response from the assistant based on the prompt, including the system context
    with st.chat_message("assistant"):
        response = client.chat_completions.create(
            model=st.session_state["openai_model"],
            messages=combined_messages,
            stream=True,
        )
        # Assume st.write_stream() properly handles displaying the response. Adjust accordingly
        response_content = "Placeholder for response content. Implement response handling as needed." # Placeholder; implement response handling as needed
        st.session_state.messages.append({"role": "assistant", "content": response_content})

    # Append the assistant's response to session state, making sure not to include the system message in the GUI
