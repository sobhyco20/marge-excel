import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="دمج ملفات Excel", layout="wide")

st.title("📂 دمج عدة ملفات Excel في صفحة واحدة")
st.write("ارفع أكثر من ملف Excel وسيتم دمجهم تحت بعض في جدول واحد، مع إمكانيّة تحميل الملف المدموج.")

uploaded_files = st.file_uploader(
    "اختر ملفات Excel (يمكن اختيار أكثر من ملف)",
    type=["xlsx", "xls"],
    accept_multiple_files=True
)

def to_excel(df: pd.DataFrame) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Merged")
    output.seek(0)
    return output.getvalue()

if uploaded_files:
    st.success(f"تم رفع {len(uploaded_files)} ملف.")

    frames = []

    for file in uploaded_files:
        df = pd.read_excel(file)
        df["اسم_الملف"] = file.name
        frames.append(df)

    merged_df = pd.concat(frames, ignore_index=True)

    st.subheader("📊 البيانات المدمجة (كل الملفات تحت بعض)")
    st.dataframe(merged_df, use_container_width=True)

    excel_data = to_excel(merged_df)

    st.download_button(
        label="📥 تحميل الملف المدمج (Excel)",
        data=excel_data,
        file_name="merged_output.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    with st.expander("عرض كل ملف على حدة"):
        for i, file in enumerate(uploaded_files):
            st.write(f"### ملف {i+1}: {file.name}")
            df = pd.read_excel(file)
            st.dataframe(df, use_container_width=True)

else:
    st.info("⬆ ارفع ملفين أو أكثر لبدء عملية الدمج.")
