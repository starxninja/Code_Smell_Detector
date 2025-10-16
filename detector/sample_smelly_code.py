"""
Sample smelly code for testing the detector
This file contains all 6 code smells intentionally
"""

class RestaurantManager:
    """God Class - Too many responsibilities and fields"""
    
    def __init__(self):
        # Too many fields (God Class smell)
        self.menu_items = {}
        self.guests = {}
        self.reservations = {}
        self.orders = {}
        self.payments = {}
        self.inventory = {}
        self.staff = {}
        self.tables = {}
        self.sections = {}
        self.promotions = {}
        self.reports = {}
        self.settings = {}
        self.notifications = {}
        self.audit_logs = {}
        self.financial_records = {}
        self.customer_feedback = {}
        self.suppliers = {}
        self.equipment = {}
        self.maintenance = {}
        self.schedules = {}
        self.counter = 0
    
    def process_reservation_and_order(self, guest_id, table_id, reservation_time, 
                                    party_size, special_requests, menu_items, 
                                    dietary_restrictions, payment_method, 
                                    loyalty_tier, discount_code, 
                                    celebration_type, arrival_time, 
                                    contact_phone, email_address, 
                                    emergency_contact, special_instructions, 
                                    group_name, corporate_account, 
                                    vip_status, accessibility_needs, 
                                    language_preference, communication_method, 
                                    marketing_consent, data_sharing_consent, 
                                    terms_accepted, id_verified):
        """Long Method - 50+ lines with multiple responsibilities"""
        # Magic Numbers throughout (Magic Numbers smell)
        if guest_id not in self.guests:
            return {"success": False, "message": "Guest not found"}
        
        guest = self.guests[guest_id]
        
        # Check table availability
        if table_id not in self.tables:
            return {"success": False, "message": "Table not found"}
        
        table = self.tables[table_id]
        if not table['available']:
            return {"success": False, "message": "Table not available"}
        
        # Calculate total cost
        total_cost = 0
        for item in menu_items:
            item_id = item['item_id']
            quantity = item['quantity']
            if item_id not in self.menu_items:
                return {"success": False, "message": f"Menu item {item_id} not found"}
            
            menu_item = self.menu_items[item_id]
            item_cost = menu_item['price'] * quantity
            total_cost += item_cost
        
        # Apply loyalty discount
        discount = 0
        if loyalty_tier == 1:
            discount = total_cost * 0.03
        elif loyalty_tier == 2:
            discount = total_cost * 0.08
        elif loyalty_tier == 3:
            discount = total_cost * 0.12
        
        # Apply promotional discount
        if discount_code:
            if discount_code == "WELCOME10":
                discount += total_cost * 0.10
            elif discount_code == "STUDENT15":
                discount += total_cost * 0.15
            elif discount_code == "SENIOR20":
                discount += total_cost * 0.20
        
        final_cost = total_cost - discount
        
        # Check payment method
        if payment_method not in ["cash", "credit_card", "debit_card", "mobile_pay"]:
            return {"success": False, "message": "Invalid payment method"}
        
        # Update inventory
        for item in menu_items:
            item_id = item['item_id']
            quantity = item['quantity']
            if item_id in self.inventory:
                self.inventory[item_id]['stock'] -= quantity
                self.inventory[item_id]['sold'] += quantity
        
        # Update guest information
        guest['total_visits'] += 1
        guest['total_spent'] += final_cost
        guest['last_visit'] = reservation_time
        
        # Create reservation
        self.counter += 1
        reservation_id = f"RES{self.counter:04d}"
        self.reservations[reservation_id] = {
            'guest_id': guest_id,
            'table_id': table_id,
            'reservation_time': reservation_time,
            'party_size': party_size,
            'special_requests': special_requests,
            'menu_items': menu_items,
            'dietary_restrictions': dietary_restrictions,
            'payment_method': payment_method,
            'loyalty_tier': loyalty_tier,
            'discount_code': discount_code,
            'celebration_type': celebration_type,
            'arrival_time': arrival_time,
            'contact_phone': contact_phone,
            'email_address': email_address,
            'emergency_contact': emergency_contact,
            'special_instructions': special_instructions,
            'group_name': group_name,
            'corporate_account': corporate_account,
            'vip_status': vip_status,
            'accessibility_needs': accessibility_needs,
            'language_preference': language_preference,
            'communication_method': communication_method,
            'marketing_consent': marketing_consent,
            'data_sharing_consent': data_sharing_consent,
            'terms_accepted': terms_accepted,
            'id_verified': id_verified,
            'total_cost': total_cost,
            'discount': discount,
            'final_cost': final_cost,
            'status': 'confirmed'
        }
        
        # Update table status
        table['available'] = False
        table['reservation_id'] = reservation_id
        
        return {"success": True, "reservation_id": reservation_id, "final_cost": final_cost}
    
    def add_menu_item(self, name, price, category, ingredients, prep_time, 
                     calories, allergens, portion_size, spice_level):
        """Large Parameter List - 9 parameters (way more than 5)"""
        self.counter += 1
        item_id = f"ITEM{self.counter:04d}"
        self.menu_items[item_id] = {
            'name': name,
            'price': price,
            'category': category,
            'ingredients': ingredients,
            'prep_time': prep_time,
            'calories': calories,
            'allergens': allergens,
            'portion_size': portion_size,
            'spice_level': spice_level
        }
        return item_id
    
    def calculate_loyalty_reward(self, guest_id):
        """Duplicated Code - Similar logic to process_reservation_and_order"""
        if guest_id not in self.guests:
            return 0
        
        guest = self.guests[guest_id]
        total_spent = guest['total_spent']
        
        # Duplicated discount logic
        reward = 0
        if guest['loyalty_tier'] == 1:
            reward = total_spent * 0.03
        elif guest['loyalty_tier'] == 2:
            reward = total_spent * 0.08
        elif guest['loyalty_tier'] == 3:
            reward = total_spent * 0.12
        
        return reward
    
    def apply_happy_hour_discount(self, order_id):
        """Duplicated Code - Similar logic to calculate_loyalty_reward"""
        if order_id not in self.orders:
            return 0
        
        order = self.orders[order_id]
        guest_id = order['guest_id']
        
        if guest_id not in self.guests:
            return 0
        
        guest = self.guests[guest_id]
        base_cost = order['total_cost']
        
        # Duplicated tier-based discount logic
        discount = 0
        if guest['loyalty_tier'] == 1:
            discount = base_cost * 0.03
        elif guest['loyalty_tier'] == 2:
            discount = base_cost * 0.08
        elif guest['loyalty_tier'] == 3:
            discount = base_cost * 0.12
        
        return discount


class ReservationReporter:
    """Helper class for reporting"""
    
    def __init__(self, restaurant):
        self.restaurant = restaurant
    
    def get_best_selling_items(self):
        """Feature Envy - Uses more data from RestaurantManager than its own"""
        # More operations on restaurant data than own data
        items = []
        for item_id, item in self.restaurant.menu_items.items():
            sold_count = self.restaurant.inventory.get(item_id, {}).get('sold', 0)
            items.append({
                'item_id': item_id,
                'name': item['name'],
                'sold_count': sold_count,
                'revenue': sold_count * item['price']
            })
        
        # Sort by sold count
        items.sort(key=lambda x: x['sold_count'], reverse=True)
        return items[:10]
    
    def get_guest_history(self, guest_id):
        """Feature Envy - Accesses restaurant data extensively"""
        if guest_id not in self.restaurant.guests:
            return None
        
        guest = self.restaurant.guests[guest_id]
        reservations = []
        
        for res_id, reservation in self.restaurant.reservations.items():
            if reservation['guest_id'] == guest_id:
                reservations.append(reservation)
        
        return {
            'guest_name': guest['name'],
            'total_visits': guest['total_visits'],
            'total_spent': guest['total_spent'],
            'reservations': reservations
        }
    
    def get_top_guests(self):
        """Feature Envy - Uses restaurant data more than own"""
        guests = []
        for guest_id, guest in self.restaurant.guests.items():
            guests.append({
                'guest_id': guest_id,
                'name': guest['name'],
                'total_spent': guest['total_spent'],
                'total_visits': guest['total_visits']
            })
        
        # Sort by total spent
        guests.sort(key=lambda x: x['total_spent'], reverse=True)
        return guests[:10]


def main():
    """Main function to demonstrate the smelly code"""
    restaurant = RestaurantManager()
    reporter = ReservationReporter(restaurant)
    
    # Add some menu items
    item1 = restaurant.add_menu_item(
        "Pizza Margherita", 15.99, "Main Course", 
        ["dough", "tomato", "mozzarella", "basil"], 20, 
        350, ["gluten", "dairy"], "Large", 2
    )
    
    item2 = restaurant.add_menu_item(
        "Caesar Salad", 12.99, "Appetizer",
        ["lettuce", "croutons", "parmesan", "dressing"],
        10, 200, ["gluten", "dairy"], "Regular", 1
    )
    
    # Add a guest
    restaurant.guests["G001"] = {
        'name': 'John Doe',
        'loyalty_tier': 2,
        'total_visits': 0,
        'total_spent': 0
    }
    
    # Add a table
    restaurant.tables["T001"] = {
        'available': True,
        'capacity': 4,
        'location': 'Window'
    }
    
    print("Restaurant Management System Demo")
    print("This code contains all 6 code smells for testing")


if __name__ == "__main__":
    main()
