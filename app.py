import time
import streamlit as st
import os
import uuid
import re
from pathlib import Path
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama, OllamaEmbeddings

# --- CONFIG ---
MODEL_TAG = "qwen2.5-coder:7b-instruct"
EMBED_MODEL = "nomic-embed-text"
CONTEXT_WINDOW = 8192

# Supported extensions
SUPPORTED_EXTENSIONS = [
    ".py", ".js", ".jsx", ".ts", ".tsx", ".java",
    ".md", ".mdx", ".html", ".css", ".toml", ".yaml"
]

# Folders to explicitly ignore
IGNORE_FOLDERS = ["**/node_modules/**", "**/.venv/**", "**/venv/**", "**/.git/**", "**/public/**", "**/resources/**", "**/db/**"]

st.set_page_config(page_title="Universal Dev Agent", page_icon="🌐", layout="wide")
st.title("🌐 Local Coding Agent")


@st.cache_resource
def init_components():
    llm = ChatOllama(model=MODEL_TAG, temperature=0.1, num_ctx=CONTEXT_WINDOW)
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    prompt = ChatPromptTemplate.from_template("""
    You are an expert Senior Full-Stack Developer. Use the codebase context below to assist the user.
    Analyze the provided project context (which may include Java, JS, Hugo/Markdown, or Python).
    If the user asks for code, provide clean, efficient, and documented snippets.
    If you are summarizing, explain the architecture and data flow. 
    

    CONTEXT: {context}
    USER REQUEST: {input}
    ASSISTANT RESPONSE:""")
    return llm, embeddings, prompt

llm, embeddings, code_prompt = init_components()


# --- PATH HANDLING ---
def get_valid_path(path_str):
    if not path_str: return None
    clean_path = os.path.expanduser(path_str.strip().replace('"', '').replace("'", ""))
    abs_path = os.path.abspath(clean_path)
    if not os.path.isdir(abs_path):
        st.error(f"Invalid Path: {abs_path} is not a directory.")
        return None
    return abs_path


# --- Summary Regex Logic ---
def is_summary_request(query):
    # Matches patterns like: "Give me an overview", "summarize the project",
    # "how is it structured", "architectural breakdown"
    patterns = [
        r"(?i)\b(summarize|summary|overview|architecture|structure|flow)\b",
        r"(?i)how (does|is) (this|it|the project) (work|organized|structured)",
        r"(?i)architectural (overview|design)"
    ]
    return any(re.search(p, query) for p in patterns)

# --- GENERIC INDEXING LOGIC ---
def process_folder(folder_path):
    all_docs = []

    # Progress feedback for the user
    status_text = st.empty()

    for ext in SUPPORTED_EXTENSIONS:
        status_text.text(f"Scanning for {ext} files...")
        loader = DirectoryLoader(
            folder_path,
            glob=f"**/*{ext}",
            exclude=IGNORE_FOLDERS,  # This tells LangChain to skip the .venv folder
            loader_cls=TextLoader,
            silent_errors=True,
            show_progress=False
        )
        try:
            all_docs.extend(loader.load())
        except Exception as e:
            st.error(f"Error loading files: {e}")
            return None

    if not all_docs:
        st.warning("No supported source files found in this directory.")
        return None

    # Using RecursiveCharacterTextSplitter with common code separators
    # This handles Java, JS, and Markdown effectively without needing a specific language toggle
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=150,
        separators=["\nclass ", "\nfunction ", "\nexport ", "\n## ", "\n\n", "\n", " "]
    )
    chunks = splitter.split_documents(all_docs)

    db_path = f"./db_{uuid.uuid4().hex[:6]}"
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )

    st.session_state.full_code_context = "\n\n".join(
        [f"FILE: {doc.metadata.get('source')}\n{doc.page_content}" for doc in all_docs]
    )
    return vectorstore.as_retriever(search_kwargs={"k": 5})


# --- 4. UI SIDEBAR ---
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📂 Codebase Input")

    # TIP FOR USER
    st.info("💡 **Mac Tip:** Drag a folder into the terminal or use `Option + Command + C` in Finder to copy the path.")

    user_path = st.text_input(
        "Enter Full Path:",
        placeholder="/Users/karan/Downloads/coding_agent",
        value=st.session_state.get("last_path", "")
    )

    # SIMPLE BROWSER SIMULATOR: List subdirectories of current input to help navigate
    if user_path and os.path.isdir(os.path.expanduser(user_path)):
        st.write("---")
        st.caption(f"Contents of {user_path}:")
        try:
            subs = [f.name for f in Path(os.path.expanduser(user_path)).iterdir() if
                    f.is_dir() and not f.name.startswith('.')]
            if subs:
                st.selectbox("Subfolders found:", ["Browse subfolders..."] + subs)
        except:
            pass

    if st.button("🚀 Index Code"):
        final_path = get_valid_path(user_path)
        if final_path:
            st.session_state.last_path = final_path
            with st.spinner("Building local vector database..."):
                st.session_state.retriever = process_folder(final_path)
                if st.session_state.retriever:
                    st.success(f"✅ Indexed {len(st.session_state.full_code_context.split('FILE:')) - 1} files!")
        else:
            st.error("🚨 Invalid Path. Ensure it is a folder, not a file, and you have permissions.")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query := st.chat_input("Ask about the architecture, logic, or docs..."):
    if "retriever" not in st.session_state:
        st.error("Please index a folder first.")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            resp_start_time = time.time()
            resp_area = st.empty()
            full_resp = ""

            with st.spinner("Agent..."):
                # Context Selection logic (Summary vs Search)
                if is_summary_request(query) and "full_code_context" in st.session_state:
                    context = st.session_state.full_code_context[:15000]
                else:
                    docs = st.session_state.retriever.invoke(query)
                    context = "\n\n".join([f"Path: {d.metadata['source']}\n{d.page_content}" for d in docs])

                chain = code_prompt | llm | StrOutputParser()
                for chunk in chain.stream({"context": context, "input": query}):
                    full_resp += chunk
                    resp_area.markdown(full_resp + "▌")
                resp_area.markdown(full_resp)

            total_resp_time = time.time() - resp_start_time
            st.caption(f"🏁 Done in {total_resp_time:.2f}s")

        st.session_state.messages.append({"role": "assistant", "content": full_resp})