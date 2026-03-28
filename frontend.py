import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Food Delivery App", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}
.card {
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- HEADER ----------------
st.title("🍔 Food Delivery System")

menu = ["Login", "Register", "Dashboard"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password
        })
        st.success(res.json())

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })

        data = res.json()

        if "access_token" in data:
            st.session_state.token = data["access_token"]
            st.session_state.role = data.get("role", "user")
            st.success("Logged in!")
        else:
            st.error(data)

# ---------------- DASHBOARD ----------------
elif choice == "Dashboard":

    if not st.session_state.token:
        st.warning("Login first")
        st.stop()

    headers = {"Authorization": f"Bearer {st.session_state.token}"}

    # ---------------- ADMIN DASHBOARD ----------------
    if st.session_state.role == "admin":
        st.sidebar.success("Admin Panel")

        tab1, tab2 = st.tabs(["➕ Add Food", "📦 Manage Orders"])

        # -------- ADD FOOD --------
        with tab1:
            st.subheader("Add New Food Item")

            name = st.text_input("Food Name")
            desc = st.text_area("Description")
            price = st.number_input("Price", min_value=1)
            image = st.file_uploader("Upload Image", type=["jpg", "png"])

            if st.button("Add Food"):
                if image:
                    files = {"image": image.getvalue()}
                    data = {
                        "name": name,
                        "description": desc,
                        "price": price
                    }

                    res = requests.post(
                        f"{BASE_URL}/food/add",
                        headers=headers,
                        data=data,
                        files=files
                    )

                    st.success(res.json())
                else:
                    st.warning("Upload image")

        # -------- MANAGE ORDERS --------
        with tab2:
            st.subheader("All Orders")

            res = requests.get(f"{BASE_URL}/order/all", headers=headers)
            orders = res.json()

            for order in orders:
                st.write(f"Order ID: {order['_id']}")
                st.write(f"User: {order['user_id']}")
                st.write(f"Status: {order['status']}")

                new_status = st.selectbox(
                    "Update Status",
                    ["placed", "preparing", "out_for_delivery", "delivered"],
                    key=order["_id"]
                )

                if st.button(f"Update {order['_id']}"):
                    requests.put(
                        f"{BASE_URL}/order/update-status",
                        json={
                            "order_id": order["_id"],
                            "status": new_status
                        },
                        headers=headers
                    )
                    st.success("Updated")

                st.divider()

    # ---------------- USER DASHBOARD ----------------
    else:
        tab1, tab2, tab3 = st.tabs(["🍽 Food", "🛒 Cart", "📦 Orders"])

        # -------- FOOD --------
        with tab1:
            res = requests.get(f"{BASE_URL}/food")
            foods = res.json()

            cols = st.columns(3)

            for idx, food in enumerate(foods):
                with cols[idx % 3]:
                    st.image(f"{BASE_URL}/{food['image']}", width=200)
                    st.markdown(f"### {food['name']}")
                    st.write(f"₹{food['price']}")

                    qty = st.number_input(
                        "Qty", 1, key=f"qty{food['_id']}"
                    )

                    if st.button(f"Add {food['_id']}"):
                        requests.post(
                            f"{BASE_URL}/cart/add",
                            json={
                                "food_id": food["_id"],
                                "quantity": qty
                            },
                            headers=headers
                        )
                        st.success("Added!")

        # -------- CART --------
        with tab2:
            res = requests.get(f"{BASE_URL}/cart", headers=headers)
            cart = res.json()

            total = 0

            for item in cart.get("items", []):
                st.write(f"{item['name']} x {item['quantity']}")
                total += item["price"] * item["quantity"]

            st.write(f"### Total: ₹{total}")

            if st.button("Place Order"):
                res = requests.post(
                    f"{BASE_URL}/order/create",
                    headers=headers
                )
                st.success(res.json())

        # -------- ORDERS --------
        with tab3:
            res = requests.get(f"{BASE_URL}/order/my-orders", headers=headers)
            orders = res.json()

            for order in orders:
                st.markdown(f"### Order {order['_id']}")
                st.write(f"Status: {order['status']}")
                st.write(f"Total: ₹{order['total']}")

                if st.button(f"Track {order['_id']}"):
                    track = requests.get(
                        f"{BASE_URL}/order/track/{order['_id']}"
                    ).json()

                    st.write("📍", track)

                st.divider()