import os
import streamlit as st
import requests

baseURL = os.environ.get("API_BASE_URL")

st.title("🦙 Llama Index doc search 🦙")
st.markdown(
        "This demo allows you to upload your own documents (local files, future: slack channel, docusaurus) \n\n" 
        "and index them, building a queryable knowledge base!\n\n"
        "Powered by [Llama Index](https://gpt-index.readthedocs.io/en/latest/index.html) and OpenAI \n\n"
)        

setup_tab, upload_tab, query_tab = st.tabs(
    ["Setup", "Upload Documents", "Query Documents"]
)

with setup_tab:
    st.subheader("LLM Setup")
    llm_name = st.selectbox(
        "Which LLM?", ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
    )
    model_temperature = st.slider(
        "LLM Temperature", min_value=0.0, max_value=1.0, step=0.1
    )

with upload_tab:
    st.subheader("Upload Documents")
    st.markdown(
        "Upload a document to index, and the LLM will extract terms and definitions from it. \n\n"
    )
    uploaded_file = st.file_uploader(
        "Upload a txt document:", type=["txt"]
    )

    # check if a file was uploaded
    if uploaded_file is not None:
        with st.spinner("Uploading and indexing the file ..."):
            # read the contents of the file
            file_contents = uploaded_file.getvalue()
            # do something with the file contents
            st.write("File contents:")
            st.write(file_contents[0:200])
            # Create a dictionary with the file data
            files = {"file": file_contents}
            # Send a POST request to the endpoint with the file data
            response = requests.post(baseURL+"/upload", files=files)
        # response = requests.post(url=url, body=body, headers=header)
            st.subheader("Request POST Header - just for debugging")
            st.json(dict(response.request.headers))
            st.subheader("Response Status Code - just for debugging")
            st.info(f'Status Code: {response.status_code}')
            st.subheader("Response Header - just for debugging")
            st.json(dict(response.headers))
            st.subheader("Response Content - just for debugging")
            st.write(response.content)
            if response.status_code == 200:
                # get the response data as a JSON object
                data = response
                st.markdown("success:" + str(response))
            else:
                # handle the error
                st.markdown("Error:" + str(response))


with query_tab:
    st.subheader("Query Documents")
    st.markdown(
            "The LLM will attempt to answer your query, and augment it's answers using the documents you've inserted. "
            "If a term is not in the index, it will not answer it. \n\n"
    )

    query_text = st.text_input("Ask about a term or definition:")
    if query_text:
        with st.spinner("Generating answer..."):
        #     response = (
        #         st.session_state["llama_index"]
        #         .as_query_engine(
        #             similarity_top_k=5,
        #             response_mode="compact",
        #             text_qa_template=TEXT_QA_TEMPLATE,
        #             refine_template=REFINE_TEMPLATE,
        #         )
        #         .query(query_text)
        #     )
        #     
            url = baseURL + "/query?text=" + query_text
            response = requests.get(url)
            if response.status_code == 200:
                # get the response data as a JSON object
                data = response.json()
                data
            else:
                # handle the error
                st.markdown("Error:", response.status_code)
            
