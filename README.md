# web
<!-- https://inansco-laundary.onrender.com -->

users
│
├── id
├── name
├── email
├── phone
├── password_hash
├── role
├── created_at
└── updated_at


orders
│
├── id
├── user_id
├── pickup_address
├── pickup_date
├── pickup_time
├── delivery_date
├── service
├── special_instructions
├── status
├── total_price
├── created_at
└── updated_at


order_items
│
├── id
├── order_id
├── item_name
├── quantity
├── notes
└── price


order_status_history
│
├── id
├── order_id
├── status
├── message
├── changed_by
└── created_at


notifications
│
├── id
├── user_id
├── order_id
├── title
├── message
├── is_read
└── created_at


reviews
├── id
├── user_id
├── order_id
├── rating
├── comment
├── created_at
└── status

USER
 │
 └── ORDERS
       │
       ├── ITEMS
       │
       ├── STATUS HISTORY
       │
       └── NOTIFICATIONS


So the overall system becomes:

CUSTOMER
│
├── Account
├── Book Pickup
├── Track Order
├── Notifications
├── Order History
├── Reviews ⭐
└── Private Feedback 💬
       │
       ▼
     ADMIN
       │
       ├── Customers
       ├── Orders
       ├── Item quantities
       ├── Processing stages
       ├── Notifications
       ├── Reviews
       └── Feedback