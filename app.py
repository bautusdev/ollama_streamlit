import ollama
import streamlit as st

st.title("Asistente de IA local")
st.caption("Qwen2.5:1.5B & Ollama")

# Initialize chat history in session state
if "messages" not in st.session_state:
  st.session_state.messages = []

# Display prior chat messages
for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Hola, ecribe aqui la pregunta?"):
  # Add user message to state and display it
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Generate response from local Qwen2.5:1.5b model via Ollama
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    try:
      # Stream response from Ollama
      stream = ollama.chat(
          model="qwen2.5:1.5b",
          messages=[
              {"role": m["role"], "content": m["content"]}
              for m in st.session_state.messages
          ],
          stream=True,
      )

      for chunk in stream:
        full_response += chunk["message"]["content"]
        message_placeholder.markdown(full_response + "▌")

      message_placeholder.markdown(full_response)
    except Exception as e:
      full_response = f"Error connecting to Ollama: {e}"
      message_placeholder.markdown(full_response)

  # Save assistant response to state
  st.session_state.messages.append(
      {"role": "assistant", "content": full_response}
  )


