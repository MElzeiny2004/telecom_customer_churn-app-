import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="توقع مغادرة العملاء (Customer Churn)", page_icon="📊", layout="centered")

@st.cache_resource
def load_model():
    return joblib.load('churn_hgb_model.pkl')

model = load_model()

st.title("📊 نظام توقع مغادرة العملاء (Telecom Customer Churn)")
st.write("أدخل بيانات العميل في الأسفل للحصول على توقع ما إذا كان العميل سيغادر الشركة أم لا.")

st.subheader("بيانات العميل الأساسية")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input('Age (العمر)', min_value=18, max_value=100, value=30)
    married = st.selectbox('Married (متزوج؟)', ['Yes', 'No'])
    gender = st.selectbox('Gender (الجنس)', ['Male', 'Female'])
    number_of_dependents = st.number_input('Number of Dependents (عدد المعالين)', min_value=0, max_value=10, value=0)
    tenure_in_months = st.number_input('Tenure in Months (مدة الاشتراك بالشهور)', min_value=0, max_value=120, value=12)

with col2:
    monthly_charge = st.number_input('Monthly Charge (الرسوم الشهرية)', min_value=0.0, value=50.0)
    total_extra_data_charges = st.number_input('Total Extra Data Charges (رسوم البيانات الإضافية)', min_value=0.0, value=0.0)
    total_long_distance_charges = st.number_input('Total Long Distance Charges (رسوم المسافات الطويلة)', min_value=0.0, value=0.0)
    avg_monthly_long_distance_charges = st.number_input('Avg Monthly Long Distance Charges (متوسط رسوم المسافات الطويلة شهرياً)', min_value=0.0, value=0.0)
    avg_monthly_gb_download = st.number_input('Avg Monthly GB Download (متوسط التحميل بالجيجابايت شهرياً)', min_value=0.0, value=10.0)

st.subheader("الخدمات والعقود")
col3, col4 = st.columns(2)

with col3:
    internet_type = st.selectbox('Internet Type (نوع الإنترنت)', ['DSL', 'Fiber Optic', 'Cable', 'None'])
    contract = st.selectbox('Contract (نوع العقد)', ['Month-to-Month', 'One Year', 'Two Year'])
    payment_method = st.selectbox('Payment Method (طريقة الدفع)', ['Bank Withdrawal', 'Credit Card', 'Mailed Check'])
    paperless_billing = st.selectbox('Paperless Billing (الفاتورة الإلكترونية)', ['Yes', 'No'])
    phone_service = st.selectbox('Phone Service (خدمة الهاتف)', ['Yes', 'No'])
    multiple_lines = st.selectbox('Multiple Lines (خطوط متعددة)', ['Yes', 'No'])

with col4:
    internet_service = st.selectbox('Internet Service (خدمة الإنترنت)', ['Yes', 'No'])
    online_security = st.selectbox('Online Security (حماية الأنشطة على الإنترنت)', ['Yes', 'No'])
    online_backup = st.selectbox('Online Backup (النسخ الاحتياطي عبر الإنترنت)', ['Yes', 'No'])
    device_protection_plan = st.selectbox('Device Protection Plan (خطة حماية الأجهزة)', ['Yes', 'No'])
    premium_tech_support = st.selectbox('Premium Tech Support (الدعم الفني المميز)', ['Yes', 'No'])
    streaming_tv = st.selectbox('Streaming TV (بث التلفزيون)', ['Yes', 'No'])
    streaming_movies = st.selectbox('Streaming Movies (بث الأفلام)', ['Yes', 'No'])
    streaming_music = st.selectbox('Streaming Music (بث الموسيقى)', ['Yes', 'No'])
    unlimited_data = st.selectbox('Unlimited Data (بيانات غير محدودة)', ['Yes', 'No'])

st.subheader("معلومات اضافية")
col5, col6 = st.columns(2)
with col5:
    offer = st.selectbox('Offer (العرض المقدم)', ['None', 'Offer A', 'Offer B', 'Offer C', 'Offer D', 'Offer E'])
with col6:
    latitude = st.number_input('Latitude (خط العرض)', value=30.0)
    longitude = st.number_input('Longitude (خط الطول)', value=31.0)
    number_of_referrals = st.number_input('Number of Referrals (عدد الإحالات)', min_value=0, max_value=20, value=0)

if st.button('احصل على التوقع (Predict)'):
    try:
        input_data = pd.DataFrame({
            'Age': [age],
            'Married': [married],
            'Gender': [gender],
            'Number of Dependents': [number_of_dependents],
            'Tenure in Months': [tenure_in_months],
            'Monthly Charge': [monthly_charge],
            'Total Extra Data Charges': [total_extra_data_charges],
            'Total Long Distance Charges': [total_long_distance_charges],
            'Avg Monthly Long Distance Charges': [avg_monthly_long_distance_charges],
            'Avg Monthly GB Download': [avg_monthly_gb_download],
            'Internet Type': [internet_type],
            'Contract': [contract],
            'Payment Method': [payment_method],
            'Paperless Billing': [paperless_billing],
            'Phone Service': [phone_service],
            'Multiple Lines': [multiple_lines],
            'Internet Service': [internet_service],
            'Online Security': [online_security],
            'Online Backup': [online_backup],
            'Device Protection Plan': [device_protection_plan],
            'Premium Tech Support': [premium_tech_support],
            'Streaming TV': [streaming_tv],
            'Streaming Movies': [streaming_movies],
            'Streaming Music': [streaming_music],
            'Unlimited Data': [unlimited_data],
            'Offer': [offer],
            'Latitude': [latitude],
            'Longitude': [longitude],
            'Number of Referrals': [number_of_referrals]
        })

        prediction = model.predict(input_data)
        prediction_proba = model.predict_proba(input_data)

        st.markdown("---")
        st.subheader("نتيجة التنبؤ:")
        
        if prediction[0] == 1 or str(prediction[0]).lower() == 'yes':
            st.error(f"⚠️ **العميل عرضة لمغادرة الشركة (Churn = Yes)**")
            st.write(f"نسبة الاحتمالية: `{prediction_proba[0][1]*100:.2f}%`")
        else:
            st.success(f"✅ **العميل مستمر ولن يغادر (Churn = No)**")
            st.write(f"نسبة الاحتمالية: `{prediction_proba[0][0]*100:.2f}%`")

    except Exception as e:
        st.error(f"حدث خطأ أثناء التوقع: {e}")
