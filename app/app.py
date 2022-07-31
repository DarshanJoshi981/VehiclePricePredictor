import streamlit as st
from PIL import Image
import json
import datetime

import pickle
model = pickle.load(open('model\\vehicle_price_predicting_model.pickle','rb'))

with open("model\columns.json",'r') as f:
    columns = json.load(f)['vehicle_brand'][1:]
current_year = datetime.datetime.now().year

def main():
    title = 'Vehicle Price Predictor'
    st.set_page_config(page_title=title, page_icon="🚗") 
    st.title("Vehicle Price Predictor 🚘🏍️")

    st.markdown("#### Wanna sell your used vehicle!?\n##### You are at the best place.. 🔮 ")
    img = Image.open('app\\4-2-car-png-hd.png')
    st.image(img, width=450)

    st.write('')
    st.write('')

    st.selectbox('Select the brand of your car', columns)

    years = st.number_input('In which year car was purchased ?',2000, current_year, step=1, key ='year')
    Years_old = current_year-years

    Present_Price = st.number_input('What is the current ex-showroom price of the car ?  (In ₹lakhs)',
    0.00, 50.00, step=0.5, key ='present_price')

    Kms_Driven = st.number_input('What is distance completed by the car in Kilometers ?',
    0.00, 500000.00, step=500.00, key ='drived')

    Owner = st.radio("The number of owners the car had previously ?", (0, 1, 3), key='owner')

    Fuel_Type_Petrol = st.selectbox('What is the fuel type of the car ?',('Petrol','Diesel', 'CNG'), key='fuel')
    if(Fuel_Type_Petrol=='Petrol'):
        Fuel_Type_Petrol=1
        Fuel_Type_Diesel=0
    elif(Fuel_Type_Petrol=='Diesel'):
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0

    Seller_Type_Individual = st.selectbox('Are you a dealer or an individual ?', ('Dealer','Individual'), key='dealer')
    if(Seller_Type_Individual=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0	

    Transmission_Manual = st.selectbox('What is the Transmission Type ?', ('Manual','Automatic'), key='manual')
    if(Transmission_Manual=='Manual'):
        Transmission_Manual=1
    else:
        Transmission_Manual=0

    if st.button("Estimate Price", key='predict'):
        try:
            Model = model
            prediction = Model.predict([[Present_Price, Kms_Driven, Owner, Years_old,
            Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
            output = round(prediction[0],2)
            if output<0:
                st.warning("You will be not able to sell this car !!")
            else:
                st.success("You can sell the car for {} lakhs 🙌".format(output))
        except:
            st.warning("Oops!! Something went wrong\nTry again")

if __name__ == '__main__':
    main()