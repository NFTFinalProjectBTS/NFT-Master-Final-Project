import streamlit as st

st.header('We are NiFTy.1')

st.title('Our Mission')
st.write('''The team’s mission is to make NFTs accessible to everyone and help
them make investment decisions that suit their goals.''')

st.write('-' * 30)

st.title('Our Vision')
st.write('The team’s vision is to ')

st.write('-' * 30)

st.title('Our Team')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.subheader('CEO')
    st.write('Baptiste Brunet')
with col2:
    st.subheader('CMO')
    st.write('Andrea Galvan')
with col3:
    st.subheader('CFO')
    st.write('Timo Manhart')
with col4:
    st.subheader('CTO')
    st.write('Vladislav Kaleev')
with col5:
    st.subheader('COO')
    st.write('Polina Ponomareva')

st.write('-' * 30)

st.title('Our Contact')

st.write('contact@nifty1.com')
