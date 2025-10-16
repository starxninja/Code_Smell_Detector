# docs/smells.md
## Code Smells Documentation

1. Long Method
File: restaurant_manager.py
Lines: 14-70
Method: process_reservation_and_order()
Why it's a smell:
This method spans over 55 lines and juggles multiple responsibilities like validating availability, calculating bills and discounts, updating stocks and balances, and managing reservations all in one go. It violates the single responsibility principle and would be much easier to maintain if broken down into focused helper methods for validation, billing, and updates.

2. God Class (Blob)
File: restaurant_manager.py
Lines: 8-143
Class: RestaurantManager
Why it's a smell:
The RestaurantManager class overloads itself by handling menu management, guest registration, reservation processing, billing calculations, stock updates, and even basic reporting—complete with over 10 instance variables and numerous methods. This creates tight coupling and fragility; it should be refactored into specialized classes such as MenuHandler, GuestService, and ReservationService to improve modularity.

3. Duplicated Code
File: restaurant_manager.py
Lines where it appears:

Lines 50-59 (in process_reservation_and_order)
Lines 111-119 (in compute_loyalty_reward)
Lines 126-134 (in apply_happy_hour_discount)

Why it's a smell:
The identical logic for determining loyalty discount rates based on levels (0.03 for level 1, 0.08 for level 2, 0.12 for level 3) is repeated verbatim across three methods without abstraction. This duplication risks inconsistencies during maintenance, like forgetting to update one instance if rates change, and could be eliminated with a shared utility function.

4. Large Parameter List
File: restaurant_manager.py
Lines: 73-80
Method: add_menu_item()
Why it's a smell:
This method requires 9 parameters (name, price, category, ingredients, prep_time, calories, allergens, portion_size, spice_level), which overwhelms callers and increases the chance of errors in argument order. A better approach would be to pass a single MenuItem data object or dictionary to encapsulate these details cleanly.

5. Magic Numbers
File: restaurant_manager.py
Where they appear:

Lines 34-39: Discount rates (0.03, 0.08, 0.12)
Lines 94-99: Prep time multipliers (1.5, 0.8, 1.2) and rush hours (11, 14, 18, 21)
Line 105: Initial guest balance (500.0)
Lines 127-133: Repeated discount rates (0.03, 0.08, 0.12)

Why it's a smell:
These unexplained numeric literals, such as multipliers for rush-hour prep times or arbitrary initial balances, obscure the code's intent and make it hard for others to understand or modify without deep dives. They should be replaced with descriptive constants like RUSH_HOUR_MULTIPLIER = 1.5 or DEFAULT_GUEST_BALANCE = 500.0 to enhance readability and configurability.

6. Feature Envy
File: restaurant_manager.py
Lines: 147-155, 159-167, 170-180
Class: ReservationReporter
Methods: get_best_selling_items(), get_guest_history(), get_top_guests()
Why it's a smell:
Methods in the ReservationReporter class excessively reach into the RestaurantManager's private data (e.g., self.restaurant.menu_items, self.restaurant.guests, self.restaurant.reservations) far more than using any of their own attributes, showing poor cohesion. These analytics functions would fit better as part of the RestaurantManager to keep data access localized and reduce dependency.