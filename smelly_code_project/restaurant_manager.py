# restaurant_manager.py
"""
Restaurant Reservation and Menu Management System
"""

class RestaurantManager:
    """Manages restaurant operations including menu, reservations, and billing"""
    
    def __init__(self):
        self.menu_items = {}
        self.guests = {}
        self.reservations = {}
        self.reservation_counter = 0
        self.guest_counter = 0
        self.menu_counter = 0
        self.total_sales = 0
        self.total_reservations = 0
        self.seating_capacity = 100
        self.current_occupancy = 0
        
    # SMELL: Long Method - This method handles too many responsibilities from validation to updates
    def process_reservation_and_order(self, guest_id, party_size, menu_selections, reservation_time, special_requests):
        """Process a full reservation including seating, ordering, and payment calculation"""
        if guest_id not in self.guests:
            return {"success": False, "message": "Guest not registered"}
        
        guest = self.guests[guest_id]
        
        # Validate seating availability
        if self.current_occupancy + party_size > self.seating_capacity:
            return {"success": False, "message": "No available seating for party size"}
        
        # Calculate table assignment based on party size
        table_type = "small" if party_size <= 2 else "medium" if party_size <= 4 else "large"
        if table_type == "small" and len([r for r in self.reservations.values() if r['table_type'] == "small"]) >= 20:
            return {"success": False, "message": "Small tables fully booked"}
        elif table_type == "medium" and len([r for r in self.reservations.values() if r['table_type'] == "medium"]) >= 15:
            return {"success": False, "message": "Medium tables fully booked"}
        elif table_type == "large" and len([r for r in self.reservations.values() if r['table_type'] == "large"]) >= 10:
            return {"success": False, "message": "Large tables fully booked"}
        
        # Validate menu items and calculate subtotal
        subtotal = 0
        valid_selections = []
        for selection in menu_selections:
            item_id = selection['item_id']
            qty = selection['quantity']
            if item_id not in self.menu_items:
                return {"success": False, "message": f"Menu item {item_id} not available"}
            item = self.menu_items[item_id]
            if item['stock'] < qty:
                return {"success": False, "message": f"Out of stock for {item['name']}"}
            subtotal += item['price'] * qty
            valid_selections.append(selection)
            self.menu_items[item_id]['stock'] -= qty
            self.menu_items[item_id]['served'] += qty
        
        # Apply loyalty discount
        discount_rate = 0
        if guest['loyalty_level'] == 1:
            discount_rate = 0.03
        elif guest['loyalty_level'] == 2:
            discount_rate = 0.08
        elif guest['loyalty_level'] == 3:
            discount_rate = 0.12
        discount = subtotal * discount_rate
        subtotal_after_discount = subtotal - discount
        
        # Add service charge and tax
        service_charge = subtotal * 0.18
        tax = subtotal_after_discount * 0.10
        total_bill = subtotal_after_discount + service_charge + tax
        
        # Check if guest has sufficient balance
        if guest['balance'] < total_bill:
            return {"success": False, "message": "Insufficient funds"}
        
        # Assign table and update occupancy
        self.reservation_counter += 1
        res_id = f"RES{self.reservation_counter:04d}"
        self.reservations[res_id] = {
            'guest_id': guest_id,
            'party_size': party_size,
            'table_type': table_type,
            'time': reservation_time,
            'selections': valid_selections,
            'subtotal': subtotal,
            'discount': discount,
            'service_charge': service_charge,
            'tax': tax,
            'total_bill': total_bill,
            'status': 'active',
            'special_requests': special_requests
        }
        
        # Update guest and restaurant stats
        self.current_occupancy += party_size
        guest['balance'] -= total_bill
        guest['total_spent'] += total_bill
        guest['reservation_count'] += 1
        self.total_sales += total_bill
        self.total_reservations += 1
        
        return {"success": True, "res_id": res_id, "total_bill": total_bill}
    
    # SMELL: Large Parameter List - Method takes excessive arguments making calls cumbersome
    def add_menu_item(self, name, price, category, ingredients, prep_time, calories, allergens, portion_size, spice_level):
        """Add a new dish to the menu"""
        self.menu_counter += 1
        item_id = f"ITM{self.menu_counter:03d}"
        self.menu_items[item_id] = {
            'name': name,
            'price': price,
            'category': category,
            'ingredients': ingredients,
            'prep_time': prep_time,
            'calories': calories,
            'allergens': allergens,
            'portion_size': portion_size,
            'spice_level': spice_level,
            'stock': 50,
            'served': 0
        }
        return item_id
    
    # SMELL: Magic Numbers - Unexplained hard-coded thresholds and rates
    def estimate_prep_time(self, res_id):
        """Estimate total preparation time for a reservation's order"""
        if res_id not in self.reservations:
            return 0
        
        res = self.reservations[res_id]
        total_prep = 0
        for selection in res['selections']:
            item_id = selection['item_id']
            qty = selection['quantity']
            prep_per_item = self.menu_items[item_id]['prep_time']
            total_prep += prep_per_item * qty
        
        # Magic numbers for rush hour multipliers
        hour = int(res['time'].split(':')[0])
        if 11 <= hour < 14 or 18 <= hour < 21:
            return total_prep * 1.5  # Rush hour multiplier
        elif hour < 11 or hour >= 21:
            return total_prep * 0.8  # Off-peak discount
        else:
            return total_prep * 1.2  # Moderate time
        return total_prep  # Fallback
    
    def register_guest(self, name, email, loyalty_level):
        """Register a new guest"""
        self.guest_counter += 1
        guest_id = f"G{self.guest_counter:03d}"
        # SMELL: Magic Numbers
        self.guests[guest_id] = {
            'name': name,
            'email': email,
            'loyalty_level': loyalty_level,
            'balance': 500.0,  # Arbitrary initial balance
            'total_spent': 0,
            'reservation_count': 0
        }
        return guest_id
    
    # SMELL: Duplicated Code - Repeats loyalty discount logic
    def compute_loyalty_reward(self, guest_id):
        """Compute reward points based on spending"""
        if guest_id not in self.guests:
            return 0
        
        guest = self.guests[guest_id]
        spent = guest['total_spent']
        
        # Duplicated discount rate logic
        reward_rate = 0
        if guest['loyalty_level'] == 1:
            reward_rate = 0.03
        elif guest['loyalty_level'] == 2:
            reward_rate = 0.08
        elif guest['loyalty_level'] == 3:
            reward_rate = 0.12
        
        return spent * reward_rate
    
    def generate_menu_report(self):
        """Generate current menu availability report"""
        report = []
        for item_id, item in self.menu_items.items():
            report.append({
                'item_id': item_id,
                'name': item['name'],
                'stock': item['stock'],
                'revenue': item['served'] * item['price']
            })
        return report
    
    # SMELL: Duplicated Code - Similar loyalty logic again
    def apply_happy_hour_discount(self, guest_id, item_id):
        """Apply time-sensitive discount for a specific item"""
        if guest_id not in self.guests or item_id not in self.menu_items:
            return 0
        
        guest = self.guests[guest_id]
        item = self.menu_items[item_id]
        base_price = item['price']
        
        # Duplicated loyalty-based rate logic
        disc_rate = 0
        if guest['loyalty_level'] == 1:
            disc_rate = 0.03
        elif guest['loyalty_level'] == 2:
            disc_rate = 0.08
        elif guest['loyalty_level'] == 3:
            disc_rate = 0.12
        
        return base_price * disc_rate
    
    def update_stock(self, item_id, quantity):
        """Restock a menu item"""
        if item_id not in self.menu_items:
            return False
        self.menu_items[item_id]['stock'] += quantity
        return True
    
    def add_guest_funds(self, guest_id, amount):
        """Add funds to guest account"""
        if guest_id not in self.guests:
            return False
        self.guests[guest_id]['balance'] += amount
        return True


class ReservationReporter:
    """Reporter for reservation and sales analytics"""
    
    def __init__(self, restaurant_manager):
        self.restaurant = restaurant_manager
    
    # SMELL: Feature Envy - Heavily relies on RestaurantManager's internal data
    def get_best_selling_items(self, top_n):
        """Retrieve top menu items by servings"""
        items_list = []
        for item_id, item in self.restaurant.menu_items.items():
            items_list.append({
                'id': item_id,
                'name': item['name'],
                'served': item['served'],
                'total_revenue': item['served'] * item['price']
            })
        
        # Sort descending by servings
        items_list.sort(key=lambda x: x['served'], reverse=True)
        return items_list[:top_n]
    
    # SMELL: Feature Envy - Extensive access to restaurant's guest and reservation data
    def get_guest_history(self, guest_id):
        """Fetch detailed history for a guest"""
        if guest_id not in self.restaurant.guests:
            return None
        
        guest = self.restaurant.guests[guest_id]
        guest_res = [r for rid, r in self.restaurant.reservations.items() if r['guest_id'] == guest_id]
        
        return {
            'name': guest['name'],
            'reservations_made': guest['reservation_count'],
            'total_spent': guest['total_spent'],
            'avg_bill': guest['total_spent'] / guest['reservation_count'] if guest['reservation_count'] > 0 else 0,
            'current_balance': guest['balance']
        }
    
    # SMELL: Duplicated Code - Reuses sorting pattern from get_best_selling_items
    def get_top_guests(self, top_n):
        """Identify top spending guests"""
        guests_list = []
        for g_id, guest in self.restaurant.guests.items():
            guests_list.append({
                'id': g_id,
                'name': guest['name'],
                'total_spent': guest['total_spent'],
                'res_count': guest['reservation_count']
            })
        
        # Duplicated sorting logic
        guests_list.sort(key=lambda x: x['total_spent'], reverse=True)
        return guests_list[:top_n]


def main():
    """Demo function for the restaurant management system"""
    restaurant = RestaurantManager()
    reporter = ReservationReporter(restaurant)
    
    # Register menu items
    i1 = restaurant.add_menu_item("Grilled Salmon", 28.99, "Seafood", ["salmon", "herbs"], 20, 450, ["fish"], "8oz", "mild")
    i2 = restaurant.add_menu_item("Veggie Pasta", 18.99, "Pasta", ["pasta", "veggies"], 15, 600, ["gluten"], "12oz", "mild")
    i3 = restaurant.add_menu_item("Steak", 42.99, "Meat", ["steak", "potatoes"], 30, 800, None, "10oz", "medium")
    
    # Register guests
    g1 = restaurant.register_guest("Charlie Brown", "charlie@email.com", 2)
    g2 = restaurant.register_guest("Lucy Van", "lucy@email.com", 1)
    
    # Process reservations
    res1 = restaurant.process_reservation_and_order(g1, 2, [{'item_id': i1, 'quantity': 1}], "12:00", "Window seat")
    res2 = restaurant.process_reservation_and_order(g2, 3, [{'item_id': i2, 'quantity': 2}, {'item_id': i3, 'quantity': 1}], "19:00", None)
    
    print("Restaurant Management System Demo")
    print(f"Reservation 1: {res1}")
    print(f"Reservation 2: {res2}")
    print(f"Top Items: {reporter.get_best_selling_items(3)}")
    print(f"Guest History: {reporter.get_guest_history(g1)}")


if __name__ == "__main__":
    main()