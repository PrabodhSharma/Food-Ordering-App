import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import requests
import io

# Static food data with image URLs
FOOD_ITEMS = [
    {
        "title": "Pizza",
        "price": 12.99,
        "image_url": "https://img.icons8.com/ios/50/000000/pizza.png",  # Icons8 pizza image
        "base_ingredients": ["Dough", "Tomato Sauce", "Cheese", "Pepperoni"],
        "custom_ingredients": ["Extra Cheese", "Olives", "Mushrooms", "Peppers", "Chicken", "Beef"],
        "meat_options": ["Chicken", "Beef"]
    },
    {
        "title": "Burger",
        "price": 8.99,
        "image_url": "https://img.icons8.com/ios/50/000000/hamburger.png",  # Icons8 burger image
        "base_ingredients": ["Bun", "Beef Patty", "Lettuce", "Cheese"],
        "custom_ingredients": ["Bacon", "Tomato", "Pickles", "Avocado", "Chicken", "Cheese"],
        "meat_options": ["Beef", "Chicken"]
    },
    {
        "title": "Pasta",
        "price": 10.49,
        "image_url": "https://img.icons8.com/ios/50/000000/spaghetti.png",  # Icons8 pasta image
        "base_ingredients": ["Pasta", "Tomato Sauce", "Garlic", "Basil"],
        "custom_ingredients": ["Parmesan", "Mushrooms", "Spinach", "Olives"]
    },
    {
        "title": "Sushi",
        "price": 15.99,
        "image_url": "https://img.icons8.com/ios/50/000000/sushi.png",  # Icons8 sushi image
        "base_ingredients": ["Rice", "Seaweed", "Salmon", "Avocado"],
        "custom_ingredients": ["Cucumber", "Carrot", "Tuna", "Wasabi"]
    },
    {
        "title": "Salad",
        "price": 7.49,
        "image_url": "https://img.icons8.com/ios/50/000000/salad.png",  # Icons8 salad image
        "base_ingredients": ["Lettuce", "Tomatoes", "Cucumber", "Olive Oil"],
        "custom_ingredients": ["Croutons", "Feta Cheese", "Avocado", "Olives"]
    },
    {
        "title": "Ice Cream",
        "price": 5.99,
        "image_url": "https://img.icons8.com/?size=100&id=13316&format=png&color=000000",  # Icons8 ice cream image
        "base_ingredients": ["Vanilla Ice Cream", "Chocolate Sauce", "Sprinkles"],
        "custom_ingredients": ["Strawberries", "Banana", "Nuts", "Cherries"]
    },
    {
        "title": "Tacos",
        "price": 6.99,
        "image_url": "https://img.icons8.com/ios/50/000000/taco.png",  # Icons8 taco image
        "base_ingredients": ["Taco Shell", "Ground Beef", "Lettuce", "Cheese"],
        "custom_ingredients": ["Sour Cream", "Guacamole", "Pico de Gallo", "Jalapenos"]
    }
]

class FoodOrderingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Ordering App")
        self.root.geometry("800x600")
        self.root.configure(bg="#f9f4ef")
        self.cart = []
        self.order_history = []
        self.users = {}  # Store user accounts
        self.current_user = None
        self.create_home_page()

    def create_home_page(self):
        """Create the home page."""
        self.clear_frame()

        title = tk.Label(
            self.root,
            text="Welcome to the Food Ordering App",
            font=("Arial", 24, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        title.pack(pady=20)

        # Create a frame for buttons
        button_frame = tk.Frame(self.root, bg="#f9f4ef")
        button_frame.pack(pady=20)

        sign_in_button = tk.Button(
            button_frame,
            text="Sign In",
            command=self.sign_in,
            font=("Arial", 16),
            bg="#007acc",
            fg="#fff",
            activebackground="#005b9c",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        sign_in_button.pack(side="left", padx=10)

        sign_up_button = tk.Button(
            button_frame,
            text="Sign Up",
            command=self.sign_up,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="#fff",
            activebackground="#45a049",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        sign_up_button.pack(side="left", padx=10)

    def sign_up(self):
        """Sign up page."""
        self.clear_frame()

        sign_up_title = tk.Label(
            self.root,
            text="Create Account",
            font=("Arial", 20, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        sign_up_title.pack(pady=10)

        # Create input fields
        fields = [
            ("Username:", "username"),
            ("Password:", "password"),
            ("Email:", "email"),
            ("Full Name:", "full_name"),
            ("Phone:", "phone"),
            ("Address:", "address")
        ]

        entries = {}
        for label_text, field_name in fields:
            label = tk.Label(self.root, text=label_text, font=("Arial", 14), bg="#f9f4ef")
            label.pack(pady=5)
            
            # Use show="*" for password
            entry = tk.Entry(self.root, font=("Arial", 14), 
                             show="*" if field_name == "password" else "")
            entry.pack(pady=5, fill="x", padx=50)
            entries[field_name] = entry

        def create_account():
            """Process account creation."""
            username = entries["username"].get().strip()
            password = entries["password"].get().strip()

            # Basic validation
            if not username or not password:
                messagebox.showerror("Error", "Username and password are required!")
                return

            if username in self.users:
                messagebox.showerror("Error", "Username already exists!")
                return

            # Create user profile
            user_profile = {
                "username": username,
                "password": password,
                "email": entries["email"].get(),
                "full_name": entries["full_name"].get(),
                "phone": entries["phone"].get(),
                "address": entries["address"].get()
            }

            # Store user
            self.users[username] = user_profile
            messagebox.showinfo("Success", "Account created successfully!")
            self.sign_in()

        create_button = tk.Button(
            self.root,
            text="Create Account",
            command=create_account,
            font=("Arial", 16),
            bg="#ff6f61",
            fg="#fff",
            activebackground="#e55b4e",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        create_button.pack(pady=20)

        back_button = tk.Button(
            self.root,
            text="Back to Home",
            command=self.create_home_page,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="#fff",
            activebackground="#45a049",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        back_button.pack(pady=10)

    def sign_in(self):
        """Sign in page."""
        self.clear_frame()

        sign_in_title = tk.Label(
            self.root,
            text="Sign In",
            font=("Arial", 20, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        sign_in_title.pack(pady=10)

        username_label = tk.Label(self.root, text="Username:", font=("Arial", 14), bg="#f9f4ef")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5, fill="x", padx=50)

        password_label = tk.Label(self.root, text="Password:", font=("Arial", 14), bg="#f9f4ef")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5, fill="x", padx=50)

        def validate_login():
            """Validate login credentials."""
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()

            # Check if user exists and password is correct
            if username in self.users and self.users[username]['password'] == password:
                self.current_user = self.users[username]
                messagebox.showinfo("Sign In", "Sign-in successful!")
                self.create_menu_page()
            else:
                messagebox.showerror("Error", "Invalid username or password!")

        sign_in_button = tk.Button(
            self.root,
            text="Sign In",
            command=validate_login,
            font=("Arial", 16),
            bg="#ff6f61",
            fg="#fff",
            activebackground="#e55b4e",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        sign_in_button.pack(pady=20)

        back_button = tk.Button(
            self.root,
            text="Back to Home",
            command=self.create_home_page,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="#fff",
            activebackground="#45a049",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        back_button.pack(pady=10)

    def create_menu_page(self):
        """Create the menu page with scroll feature and logout option."""
        self.clear_frame()

        menu_title = tk.Label(
            self.root,
            text="Menu",
            font=("Arial", 20, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        menu_title.pack(pady=10)

        # Add welcome message with username
        welcome_label = tk.Label(
            self.root,
            text=f"Welcome, {self.current_user['username']}!",
            font=("Arial", 14),
            bg="#f9f4ef",
            fg="#333",
        )
        welcome_label.pack(pady=5)

        # Create a canvas widget for scrolling
        canvas = tk.Canvas(self.root, bg="#f9f4ef")
        canvas.pack(fill="both", expand=True)

        # Create a vertical scrollbar linked to the canvas
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the menu items
        menu_frame = tk.Frame(canvas, bg="#f9f4ef")
        canvas.create_window((0, 0), window=menu_frame, anchor="nw")

        # Add menu items to the frame
        for item in FOOD_ITEMS:
            self.create_menu_item(item, menu_frame)

        # Update the canvas scroll region to accommodate all menu items
        menu_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Create a frame for buttons
        button_frame = tk.Frame(self.root, bg="#f9f4ef")
        button_frame.pack(pady=10)

        # Add the View Cart button
        cart_button = tk.Button(
            button_frame,
            text="View Cart",
            command=self.view_cart,
            font=("Arial", 16),
            bg="#007acc",
            fg="#fff",
            activebackground="#005b9c",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        cart_button.pack(side="left", padx=10)

        # Add the Order History button
        history_button = tk.Button(
            button_frame,
            text="Order History",
            command=self.view_order_history,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="#fff",
            activebackground="#45a049",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        history_button.pack(side="left", padx=10)

        # Add the Profile button
        profile_button = tk.Button(
            button_frame,
            text="My Profile",
            command=self.view_profile,
            font=("Arial", 16),
            bg="#FF9800",
            fg="#fff",
            activebackground="#F57C00",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        profile_button.pack(side="left", padx=10)

        # Add the Logout button
        logout_button = tk.Button(
            button_frame,
            text="Logout",
            command=self.logout,
            font=("Arial", 16),
            bg="#ff6f61",
            fg="#fff",
            activebackground="#e55b4e",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        logout_button.pack(side="left", padx=10)

    def logout(self):
        """Logout the current user and return to home page."""
        self.current_user = None
        self.cart.clear()
        self.create_home_page()

    

    

    def create_menu_item(self, item, parent_frame):
        """Create a menu item display with an image, price, and ingredients."""
        frame = tk.Frame(parent_frame, bg="#f9f4ef", pady=10)
        frame.pack(fill="x", padx=20, pady=10)

        # Left-side content frame
        content_frame = tk.Frame(frame, bg="#f9f4ef")
        content_frame.pack(side="left", fill="x", expand=True)

        # Load the image
        try:
            response = requests.get(item["image_url"])
            response.raise_for_status()  # Check for successful status code (200)
            img_data = io.BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((100, 100))  # Resize the image to fit the layout
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(content_frame, image=img)
            img_label.image = img  # keep a reference!
            img_label.pack(side="left", padx=10)
        except requests.exceptions.RequestException as e:
            print(f"Image load failed for {item['title']} with error: {e}")
            img_label = tk.Label(content_frame, text="No Image Available", bg="#f9f4ef")
            img_label.pack(side="left", padx=10)

        # Text information frame
        text_frame = tk.Frame(content_frame, bg="#f9f4ef")
        text_frame.pack(side="left", fill="x", expand=True)

        title_label = tk.Label(
            text_frame, 
            text=item["title"], 
            font=("Arial", 16, "bold"), 
            bg="#f9f4ef", 
            anchor="w"
        )
        title_label.pack(fill="x")

        price_label = tk.Label(
            text_frame, 
            text=f"${item['price']:.2f}", 
            font=("Arial", 14), 
            bg="#f9f4ef", 
            anchor="w"
        )
        price_label.pack(fill="x")

        base_ingredients_label = tk.Label(
            text_frame, 
            text="Base Ingredients: " + ", ".join(item["base_ingredients"]), 
            font=("Arial", 12), 
            bg="#f9f4ef", 
            anchor="w"
        )
        base_ingredients_label.pack(fill="x")

        # Add to Cart button frame
        button_frame = tk.Frame(frame, bg="#f9f4ef")
        button_frame.pack(side="right", padx=10)

        add_to_cart_button = tk.Button(
            button_frame,
            text="Add to Cart",
            command=lambda item=item: self.add_to_cart(item),
            font=("Arial", 12),
            bg="#ff6f61",
            fg="#fff",
            activebackground="#e55b4e",
            activeforeground="#fff",
            padx=10,
            pady=5,
        )
        add_to_cart_button.pack(side="right")




    def add_to_cart(self, item):
        """Handle adding item to cart."""
        # Get base ingredients
        base_ingredients = item["base_ingredients"]
        
        # Get available custom ingredients
        available_custom_ingredients = item.get("custom_ingredients", [])
        
        # Prepare custom ingredients selection dialog
        custom_ingredients_text = "Available Custom Ingredients: " + ", ".join(available_custom_ingredients)
        custom_ingredients = simpledialog.askstring(
            "Custom Ingredients",
            f"Select custom ingredients for {item['title']}\n{custom_ingredients_text}",
            parent=self.root,
        )
        
        # Process custom ingredients
        if not custom_ingredients:
            custom_ingredients_list = base_ingredients
            custom_ingredients_message = "Custom Ingredients: None"
        else:
            # Split and clean custom ingredients
            custom_ingredients_list = [ing.strip() for ing in custom_ingredients.split(",")]
            custom_ingredients_message = "Custom Ingredients: " + ", ".join(custom_ingredients_list)

        cart_item = {
            "title": item["title"],
            "price": item["price"],
            "custom_ingredients": custom_ingredients_message,
        }
        self.cart.append(cart_item)
        messagebox.showinfo("Added to Cart", f"{item['title']} added to your cart!")


    def view_cart(self):
        """View items in the cart."""
        self.clear_frame()

        cart_title = tk.Label(self.root, text="Your Cart", font=("Arial", 20, "bold"), bg="#f9f4ef", fg="#333")
        cart_title.pack(pady=10)

        # Check if cart is empty
        if not self.cart:
            empty_cart_label = tk.Label(
                self.root, 
                text="No items in the cart", 
                font=("Arial", 16), 
                bg="#f9f4ef", 
                fg="#333"
            )
            empty_cart_label.pack(pady=20)
        else:
            for index, item in enumerate(self.cart):
                item_frame = tk.Frame(self.root, bg="#f9f4ef")
                item_frame.pack(pady=5, fill="x", padx=20)

                item_label = tk.Label(
                    item_frame, 
                    text=f"{item['title']} - ${item['price']:.2f}\n{item['custom_ingredients']}", 
                    font=("Arial", 14), 
                    bg="#f9f4ef", 

                    justify=tk.LEFT,  
                    anchor="w"
                )
                item_label.pack(side="left", padx=10)

                delete_button = tk.Button(
                    item_frame,
                    text="Delete",
                    command=lambda idx=index: self.delete_cart_item(idx),
                    font=("Arial", 12),
                    bg="#ff6f61",
                    fg="#fff",
                    activebackground="#e55b4e",
                    activeforeground="#fff",
                    padx=10,
                    pady=5,
                )
                delete_button.pack(side="right", padx=10)

        # Create a frame for buttons
        button_frame = tk.Frame(self.root, bg="#f9f4ef")
        button_frame.pack(pady=10)

        checkout_button = tk.Button(
            button_frame,
            text="Checkout",
            command=self.checkout,
            font=("Arial", 16),
            bg="#007acc",
            fg="#fff",
            activebackground="#005b9c",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        checkout_button.pack(side="left", padx=10)

        back_to_menu_button = tk.Button(
            button_frame,
            text="Back to Menu",
            command=self.create_menu_page,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="#fff",
            activebackground="#45a049",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        back_to_menu_button.pack(side="left", padx=10)

    
    def delete_cart_item(self, index):
        """Delete a specific item from the cart."""
        if 0 <= index < len(self.cart):
            del self.cart[index]
            self.view_cart()
        

    def checkout(self):
        """Checkout page with payment methods."""
        # Check if cart is empty
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Please add items to your cart before checking out.")
            return

        total_price = sum(item['price'] for item in self.cart)
        
        # Create payment method window
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Payment")
        payment_window.geometry("400x500")
        payment_window.configure(bg="#f9f4ef")

        title = tk.Label(
            payment_window,
            text="Payment Details",
            font=("Arial", 20, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        title.pack(pady=10)

        total_label = tk.Label(
            payment_window,
            text=f"Total Price: ${total_price:.2f}",
            font=("Arial", 16),
            bg="#f9f4ef",
            fg="#333",
        )
        total_label.pack(pady=10)

        # Payment Method Selection
        method_label = tk.Label(
            payment_window,
            text="Select Payment Method",
            font=("Arial", 14),
            bg="#f9f4ef",
            fg="#333",
        )
        method_label.pack(pady=10)

        # Payment Method Radiobuttons
        payment_method = tk.StringVar(value="Credit Card")
        credit_radio = tk.Radiobutton(
            payment_window, 
            text="Credit Card", 
            variable=payment_method, 
            value="Credit Card", 
            font=("Arial", 12),
            bg="#f9f4ef"
        )
        credit_radio.pack(pady=5)

        debit_radio = tk.Radiobutton(
            payment_window, 
            text="Debit Card", 
            variable=payment_method, 
            value="Debit Card", 
            font=("Arial", 12),
            bg="#f9f4ef"
        )
        debit_radio.pack(pady=5)

        # Card Number Entry
        card_number_label = tk.Label(
            payment_window,
            text="Card Number:",
            font=("Arial", 12),
            bg="#f9f4ef"
        )
        card_number_label.pack(pady=5)
        card_number_entry = tk.Entry(payment_window, font=("Arial", 12), width=30)
        card_number_entry.pack(pady=5)

        # Expiry Date Entry
        expiry_label = tk.Label(
            payment_window,
            text="Expiry Date (MM/YY):",
            font=("Arial", 12),
            bg="#f9f4ef"
        )
        expiry_label.pack(pady=5)
        expiry_entry = tk.Entry(payment_window, font=("Arial", 12), width=30)
        expiry_entry.pack(pady=5)

        # CVV Entry
        cvv_label = tk.Label(
            payment_window,
            text="CVV:",
            font=("Arial", 12),
            bg="#f9f4ef"
        )
        cvv_label.pack(pady=5)
        cvv_entry = tk.Entry(payment_window, font=("Arial", 12), width=10, show="*")
        cvv_entry.pack(pady=5)

        def process_payment():
            """Process the payment and complete the order."""
            # Validate payment details
            card_number = card_number_entry.get()
            expiry = expiry_entry.get()
            cvv = cvv_entry.get()

            if not (card_number and expiry and cvv):
                messagebox.showerror("Error", "Please fill in all payment details.")
                return

            # Create order record
            order = {
                "items": self.cart.copy(),
                "total_price": total_price,
                "payment_method": payment_method.get(),
                # "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.order_history.append(order)

            # Show successful payment message
            messagebox.showinfo("Payment Successful", f"Total paid: ${total_price:.2f}")
            
            # Clear cart 
            self.cart.clear()
            payment_window.destroy()
            
            # Return to menu page
            self.create_menu_page()

        # Confirm Payment Button
        confirm_payment_button = tk.Button(
            payment_window,
            text="Confirm Payment",
            command=process_payment,
            font=("Arial", 16),
            bg="#007acc",
            fg="#fff",
            activebackground="#005b9c",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        confirm_payment_button.pack(pady=20)

    def view_profile(self):
        """View and edit user profile."""
        self.clear_frame()

        profile_title = tk.Label(
            self.root,
            text="My Profile",
            font=("Arial", 20, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        profile_title.pack(pady=10)

        # Profile Details Frame
        profile_frame = tk.Frame(self.root, bg="#f9f4ef")
        profile_frame.pack(pady=20)

        # Profile Fields
        fields = [
            ("Username", "username"),
            ("Email", "email"),
            ("Full Name", "full_name"),
            ("Phone", "phone"),
            ("Address", "address")
        ]

        # Create entry fields for profile information
        self.profile_entries = {}
        for label_text, field_name in fields:
            label = tk.Label(
                profile_frame, 
                text=f"{label_text}:", 
                font=("Arial", 14), 
                bg="#f9f4ef"
            )
            label.pack(pady=5)
            
            entry = tk.Entry(
                profile_frame, 
                font=("Arial", 14), 
                width=40
            )
            entry.pack(pady=5)
            
            # Populate existing profile data
            entry.insert(0, self.current_user.get(field_name, ""))
            
            # Store reference to entry
            self.profile_entries[field_name] = entry

        # Save Profile Button
        save_button = tk.Button(
            self.root,
            text="Save Profile",
            command=self.save_profile,
            font=("Arial", 16),
            bg="#007acc",
            fg="#fff",
            activebackground="#005b9c",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        save_button.pack(pady=20)

        # Back to Menu Button
        back_button = tk.Button(
            self.root,
            text="Back to Menu",
            command=self.create_menu_page,
            font=("Arial", 16),
            bg="#4CAF50",
            fg="#fff",
            activebackground="#45a049",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        back_button.pack(pady=10)

    def save_profile(self):
        """Save profile information."""
        # Update user profile with entry values
        for field_name, entry in self.profile_entries.items():
            self.current_user[field_name] = entry.get()

        # Also update the users dictionary
        self.users[self.current_user['username']] = self.current_user

        # Show success message
        messagebox.showinfo("Profile Updated", "Your profile has been successfully updated!")

    def validate_sign_in(self):
        """Validate the sign-in credentials."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both username and password are required!")
            return

        # Create a user profile using the sign-in details
        self.user_profile["username"] = username
        self.user_profile["email"] = f"{username}@example.com"
        messagebox.showinfo("Sign In", "Sign-in successful!")

        # Proceed to the menu page
        self.create_menu_page()

    def view_order_history(self):
        """View the order history."""
        self.clear_frame()

        history_title = tk.Label(
            self.root,
            text="Order History",
            font=("Arial", 20, "bold"),
            bg="#f9f4ef",
            fg="#333",
        )
        history_title.pack(pady=10)

        if not self.order_history:
            no_history_label = tk.Label(
                self.root,
                text="No order history found.",
                font=("Arial", 14),
                bg="#f9f4ef",
                fg="#333",
            )
            no_history_label.pack(pady=20)
        else:
            # Create a canvas widget for scrolling
            canvas = tk.Canvas(self.root, bg="#f9f4ef")
            canvas.pack(fill="both", expand=True)

            # Create a vertical scrollbar linked to the canvas
            scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
            scrollbar.pack(side="right", fill="y")

            canvas.configure(yscrollcommand=scrollbar.set)

            # Create a frame inside the canvas to hold the order history
            history_frame = tk.Frame(canvas, bg="#f9f4ef")
            canvas.create_window((0, 0), window=history_frame, anchor="nw")

            # Display order history
            for order in self.order_history:
                order_frame = tk.Frame(history_frame, bg="#f9f4ef", bd=1, relief=tk.RAISED)
                order_frame.pack(fill="x", padx=20, pady=10)

                # Order details
                total_label = tk.Label(
                    order_frame, 
                    text=f"Total: ${order['total_price']:.2f} | Payment: {order['payment_method']}", 
                    font=("Arial", 14), 
                    bg="#f9f4ef"
                )
                total_label.pack(pady=5)

                # Items in the order
                for item in order['items']:
                    item_label = tk.Label(
                        order_frame, 
                        text=f"{item['title']} - ${item['price']:.2f}\n{item['custom_ingredients']}", 
                        font=("Arial", 12), 
                        bg="#f9f4ef"
                    )
                    item_label.pack(pady=2)

            # Update the canvas scroll region
            history_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        # Back to Menu button
        back_button = tk.Button(
            self.root,
            text="Back to Menu",
            command=self.create_menu_page,
            font=("Arial", 16),
            bg="#007acc",
            fg="#fff",
            activebackground="#005b9c",
            activeforeground="#fff",
            padx=30,
            pady=10,
        )
        back_button.pack(pady=20)

    def clear_frame(self):
        """Clear the current frame."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FoodOrderingApp(root)
    root.mainloop()