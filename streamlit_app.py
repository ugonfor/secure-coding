import streamlit as st
import requests

def main():
    st.title('Welcome to Simple Shopping Mall')
    st.write('This is a simple shopping mall where you can buy a variety of products.')

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Login')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            if st.button('Login'):
                response = requests.get('http://localhost:8000/login', params={"username": username, "password": password})
                if response.status_code == 200:
                    st.session_state.logged_in = True
                    st.session_state.user = response.json()["user"]
                    st.success(response.json()["message"])
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        with col2:
            st.subheader('Sign Up')
            new_username = st.text_input('New Username')
            new_password = st.text_input('New Password', type='password')
            full_name = st.text_input('Full Name')
            address = st.text_input('Address')
            payment_info = st.text_input('Payment Info')
            if st.button('Sign Up'):
                response = requests.get('http://localhost:8000/register', params={"username": new_username, "password": new_password, "role": "user", "full_name": full_name, "address": address, "payment_info": payment_info})
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error("Failed to sign up.")

    if st.session_state.logged_in:
        if st.session_state.user["role"] == 'admin':
            st.sidebar.subheader('Admin Menu')
            menu = ['Home', 'Add Product']
            choice = st.sidebar.selectbox('Menu', menu)

            if choice == 'Home':
                st.subheader('All Products')
                response = requests.get('http://localhost:8000/products')
                products = response.json()
                for product in products:
                    st.write(f"Name: {product['name']}, Category: {product['category']}, Price: ${product['price']}")
                    if 'thumbnail_url' in product and product['thumbnail_url'] != '':
                        st.image(product['thumbnail_url'], width=200)

            elif choice == 'Add Product':
                st.subheader('Add a New Product')
                with st.form(key='add_product_form'):
                    name = st.text_input('Product Name')
                    category = st.text_input('Category')
                    price = st.number_input('Price', min_value=0.0)
                    thumbnail_url = st.text_input('Thumbnail URL')
                    submit_button = st.form_submit_button(label='Add')
                    
                    if submit_button:
                        add_product_response = requests.get('http://localhost:8000/add_product', params={"name": name, "category": category, "price": price, "thumbnail_url": thumbnail_url})
                        if add_product_response.status_code == 200:
                            st.success(add_product_response.json()["message"])
                        else:
                            st.error("Failed to add product.")
            if st.sidebar.button('Logout'):
                st.session_state.logged_in = False
                st.success('You have been logged out.')
                st.rerun()

        else:
            st.sidebar.subheader('User Menu')
            menu = ['Home', 'Buy Products', 'My Page']
            choice = st.sidebar.selectbox('Menu', menu)

            if choice == 'Home':
                st.subheader('All Products')
                response = requests.get('http://localhost:8000/products')
                products = response.json()
                for product in products:
                    st.write(f"Name: {product['name']}, Category: {product['category']}, Price: ${product['price']}")
                    if 'thumbnail_url' in product and product['thumbnail_url'] != '':
                        st.image(product['thumbnail_url'], width=200)

            elif choice == 'Buy Products':
                st.subheader('Buy Products')
                response = requests.get('http://localhost:8000/products')
                products = response.json()
                selected_product = st.selectbox('Select a product', [product['name'] for product in products])
                user_address = st.text_input('Home Address')
                user_payment_info = st.text_input('Payment Info')
                if st.button('Buy'):
                    # You can integrate with a payment gateway API here
                    st.success(f'You have successfully purchased {selected_product}! Address: {user_address}, Payment Info: {user_payment_info}')

            elif choice == 'My Page':
                st.subheader('My Page')
                st.write(f'Username: {st.session_state.user["username"]}')
                st.write(f'Full Name: {st.session_state.user["full_name"]}')
                st.write(f'Address: {st.session_state.user["address"]}')
                st.write(f'Payment Info: {st.session_state.user["payment_info"]}')
                
                with st.form(key='edit_user_info_form'):
                    new_username = st.text_input('New Username', value=st.session_state.user["username"])
                    new_full_name = st.text_input('Full Name', value=st.session_state.user["full_name"])
                    new_address = st.text_input('Address', value=st.session_state.user["address"])
                    new_payment_info = st.text_input('Payment Info', value=st.session_state.user["payment_info"])
                    submit_button = st.form_submit_button(label='Update Info')

                    if submit_button:
                        response = requests.get('http://localhost:8000/update_user_info', params={"username": new_username, "full_name": new_full_name, "address": new_address, "payment_info": new_payment_info})
                        if response.status_code == 200:
                            st.success('User information updated successfully!')
                            st.session_state.user["username"] = new_username
                            st.session_state.user["full_name"] = new_full_name
                            st.session_state.user["address"] = new_address
                            st.session_state.user["payment_info"] = new_payment_info
                            st.rerun()
                        else:
                            st.error("Failed to update user information.")

                if st.button('Logout'):
                    st.session_state.logged_in = False
                    st.success('You have been logged out.')
                    st.rerun()

            
            if st.sidebar.button('Logout'):
                st.session_state.logged_in = False
                st.success('You have been logged out.')
                st.rerun()

if __name__ == '__main__':
    main()
