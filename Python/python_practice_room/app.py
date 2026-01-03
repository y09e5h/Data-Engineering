import streamlit as st
import pandas as pd
import importlib
from streamlit_ace import st_ace
from assests import cb_logo
from questions import _env

# ----------------------------
# ⚙️ Page Config
# ----------------------------
page_title = "Codebasics Data Practice Platform"
page_heading = "Python Practice Room"
cb_logo = cb_logo

st.set_page_config(
    page_title=page_title,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# 🎨 Custom CSS
# ----------------------------
st.markdown("""
<style>
body {
    background-color: #f8f9fb;
    color: #222;
    font-family: 'Inter', sans-serif;
}
.question-box {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.editor-box {
    background-color: #ffffff;
    padding: 1rem 1.5rem;
    border-radius: 15px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.run-btn {
    background-color: #0072ff;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    cursor: pointer;
}
.block-container { padding-top: 0.3rem !important; }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 🧭 Header (Sticky)
# ----------------------------
st.markdown(f"""
    <div style="
        position: sticky;
        top: 0;
        z-index: 999;
        background-color: #0e1117;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 15px;
        padding: 0.8rem 1rem;
        border-bottom: 1px solid #2b2b2b;
    ">
        <img src="{cb_logo}" alt="Codebasics Logo" style="width:85px;">
        <h1 style="
            color: white;
            font-size: 2.6rem;
            font-weight: 700;
            margin: 0;
        ">{page_heading}</h1>
    </div>
""", unsafe_allow_html=True)

# ----------------------------
# 📘 Load Master Question List
# ----------------------------
try:
    questions_meta = pd.read_csv("questions/master_question_list.csv")
    questions_meta = questions_meta[questions_meta["active"] == True]
except FileNotFoundError:
    st.error("❌ master_question_list.csv not found in /questions directory.")
    st.stop()

# ----------------------------
# 🧭 Sidebar Filters
# ----------------------------
st.sidebar.header("🔍 Question Selector")

selected_difficulty = st.sidebar.selectbox(
    "🎯 Difficulty", ["All"] + sorted(questions_meta["difficulty"].unique())
)
selected_topic = st.sidebar.selectbox(
    "📘 Topic", ["All"] + sorted(questions_meta["topic"].unique())
)

filtered = questions_meta[
    ((questions_meta["difficulty"] == selected_difficulty) | (selected_difficulty == "All")) &
    ((questions_meta["topic"] == selected_topic) | (selected_topic == "All"))
]

if not filtered.empty:
    selected_title = st.sidebar.selectbox(
        "🧩 Select a Question", filtered["title"].tolist(), index=0
    )
    selected_folder = filtered.loc[
        filtered["title"] == selected_title, "folder_name"
    ].iloc[0]
else:
    st.sidebar.warning("⚠️ No questions available for the selected filters.")
    selected_title, selected_folder = None, None

# ----------------------------
# 🧠 Load Question Module
# ----------------------------
if selected_folder:
    try:
        # Load data and validator dynamically
        data = pd.read_csv(f"questions/{selected_folder}/data.csv")
        expected_path = f"questions/{selected_folder}/expected.csv"

        q_module = importlib.import_module(f"questions.{selected_folder}.question")
        v_module = importlib.import_module(f"questions.{selected_folder}.validator")

        # Inject env objects
        for name in _env.__all__:
            setattr(q_module, name, getattr(_env, name))
        setattr(q_module, "data", data)

        desc = q_module.get_description()
        hint = q_module.get_hint()
        sample_code = q_module.get_inital_sample_code()

    except Exception as e:
        st.error(f"❌ Failed to load question module: {e}")
        st.stop()

    # ----------------------------
    # 🧩 Layout Split
    # ----------------------------
    col1, col2 = st.columns([1.2, 1.8], gap="medium")

    # ----------------------------
    # 📗 LEFT PANEL – Question & Dataset
    # ----------------------------
    with col1:
        st.markdown(f"### 🧠 {selected_title}")
        st.markdown(desc, unsafe_allow_html=True)

        with st.expander("💡 Hint"):
            st.write(hint)

        st.markdown("### 📊 Dataset Preview")
        st.dataframe(data.head(), use_container_width=True)

        # Preview Expected Output
        try:
            expected_df = pd.read_csv(expected_path)
            preview_df = expected_df.sample(frac=0.7, random_state=42).head(5)
            for col in preview_df.select_dtypes(include="number").columns:
                preview_df[col] = preview_df[col] * 1.05
                preview_df[col] = preview_df[col].apply(
                    lambda x: int(x) if float(x).is_integer() else round(x, 0)
                )
            for col in preview_df.select_dtypes(include="object").columns:
                preview_df[col] = preview_df[col].astype(str).str.replace("e", "E", case=False)

            st.markdown("### 🔍 Sample Output Preview (for reference)")
            st.caption("⚠️ Note: This is only an illustrative preview — actual output may differ.")
            st.dataframe(preview_df, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load output preview: {str(e)}")

    # ----------------------------
    # 💻 RIGHT PANEL – Editor & Output
    # ----------------------------
    with col2:
        st.markdown("### 💻 Your Code")
        st.markdown("""
        💡 **Tip:** Use any one of these variable names for your final output → `df` or `result`.
        """)
        user_code = st_ace(
            value=sample_code,
            language="python",
            theme="github_light",
            keybinding="vscode",
            font_size=14,
            tab_size=4,
            height=350,
            auto_update=True,
            wrap=True,
        )
        
        btn_col1, btn_col2 = st.columns([1, 1])
        run_clicked = btn_col1.button("▶️ Run Code", use_container_width=True, key="run")
        submit_clicked = btn_col2.button("✅ Submit Code", use_container_width=True, key="submit")

        # ⚡ Run Code Logic
        if run_clicked:
            try:
                sandbox_env = vars(_env).copy()
                sandbox_env.update({
                    "__name__": "__main__",
                    "__builtins__": __builtins__,
                    "data": data.copy(),
                })

                exec(user_code, sandbox_env)
                def is_tabular(x):
                    # Accept pandas DataFrame or Series without relying on exact module identity
                    t = getattr(x, "__class__", None)
                    n = getattr(t, "__name__", "")
                    return n in ("DataFrame", "Series")

                user_output = None

                # 1) Explicit 'result'
                if "result" in sandbox_env and is_tabular(sandbox_env["result"]):
                    user_output = sandbox_env["result"]

                # 2) Modified 'data'
                if user_output is None and "data" in sandbox_env and is_tabular(sandbox_env["data"]):
                    try:
                        if not data.equals(sandbox_env["data"]):
                            user_output = sandbox_env["data"]
                    except Exception:
                        # If equals() fails (e.g., dtype/shape mismatch), treat it as modified
                        user_output = sandbox_env["data"]

                # 3) Any other tabular variable created by the user
                if user_output is None:
                    for var_name, val in sandbox_env.items():
                        if (
                            is_tabular(val)
                            and var_name not in ["data", "expected", "result"]
                            and not var_name.startswith("_")
                        ):
                            user_output = val
                            break

                # Normalize Series -> DataFrame
                if user_output is not None and getattr(user_output.__class__, "__name__", "") == "Series":
                    user_output = user_output.to_frame(name=user_output.name or "value").reset_index(drop=True)



                if user_output is not None:
                    st.markdown("### 🧾 Your Output")
                    st.dataframe(user_output, use_container_width=True)
                else:
                    st.warning("⚠️ No DataFrame found in your output.")

            except Exception as e:
                st.error(f"Execution error: {str(e)}")

        # 🏁 Submit Code Logic
        if submit_clicked:
            try:
                sandbox_env = vars(_env).copy()
                sandbox_env.update({
                    "__name__": "__main__",
                    "__builtins__": __builtins__,
                    "data": data.copy(),
                })

                try:
                    expected = pd.read_csv(expected_path)
                    sandbox_env["expected"] = expected
                except FileNotFoundError:
                    sandbox_env["expected"] = None

                exec(user_code, sandbox_env)

                user_output = None
                if "result" in sandbox_env and isinstance(sandbox_env["result"], pd.DataFrame):
                    user_output = sandbox_env["result"]
                else:
                    for var_name, val in sandbox_env.items():
                        if (
                            isinstance(val, pd.DataFrame)
                            and var_name not in ["data", "expected"]
                            and not var_name.startswith("_")
                        ):
                            user_output = val
                            break

                if user_output is None:
                    st.warning("⚠️ No DataFrame found in your output.")
                else:
                    result = v_module.validate(user_output, expected_path)

                    if "✅" in result:
                        st.balloons()
                        st.success("🎉 Great job! Your final submission passed all tests.")
                        st.dataframe(user_output, use_container_width=True)
                    else:
                        st.error("❌ Not quite right yet. Try again.")
                        st.dataframe(user_output, use_container_width=True)
                        st.caption("Validator feedback:")
                        st.code(result)
            except Exception as e:
                st.error(f"Execution error: {str(e)}")

# ----------------------------
# 🚦 If no question selected
# ----------------------------
else:
    st.info("👈 Use the sidebar to select a question and start practicing!")
