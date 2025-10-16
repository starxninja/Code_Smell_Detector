# test_restaurant.py
"""
Unit tests for Restaurant Management System
"""

import pytest
from restaurant_manager import RestaurantManager, ReservationReporter
from datetime import datetime  # Not used but for potential time handling


class TestRestaurantManager:
    """Test suite for RestaurantManager"""
    
    def setup_method(self):
        """Initialize test instance"""
        self.restaurant = RestaurantManager()
        
    def test_add_menu_item(self):
        """Verify menu item addition"""
        item_id = self.restaurant.add_menu_item(
            "Test Dish",
            15.99,
            "Test Cat",
            ["ing1", "ing2"],
            10,
            300,
            ["nut"],
            "6oz",
            "hot"
        )
        
        assert item_id in self.restaurant.menu_items
        assert self.restaurant.menu_items[item_id]['name'] == "Test Dish"
        assert self.restaurant.menu_items[item_id]['price'] == 15.99
        assert self.restaurant.menu_items[item_id]['stock'] == 50
        
    def test_register_guest(self):
        """Verify guest registration"""
        guest_id = self.restaurant.register_guest("Test Guest", "test@email.com", 1)
        
        assert guest_id in self.restaurant.guests
        assert self.restaurant.guests[guest_id]['name'] == "Test Guest"
        assert self.restaurant.guests[guest_id]['email'] == "test@email.com"
        assert self.restaurant.guests[guest_id]['loyalty_level'] == 1
        assert self.restaurant.guests[guest_id]['balance'] == 500.0
        
    def test_process_reservation_success(self):
        """Test successful reservation processing"""
        item_id = self.restaurant.add_menu_item(
            "Appetizer", 12.00, "Starter", ["veg"], 5, 200, None, "4oz", "mild"
        )
        guest_id = self.restaurant.register_guest("Valid Guest", "valid@test.com", 1)
        
        result = self.restaurant.process_reservation_and_order(
            guest_id,
            2,
            [{'item_id': item_id, 'quantity': 1}],
            "13:00",
            "None"
        )
        
        assert result['success'] == True
        assert 'res_id' in result
        assert self.restaurant.menu_items[item_id]['stock'] == 49
        assert self.restaurant.guests[guest_id]['reservation_count'] == 1
        
    def test_process_reservation_no_seating(self):
        """Test reservation failure due to capacity"""
        # Fill capacity
        self.restaurant.current_occupancy = 99
        guest_id = self.restaurant.register_guest("Full House", "full@test.com", 1)
        
        result = self.restaurant.process_reservation_and_order(
            guest_id,
            2,
            [],
            "14:00",
            "None"
        )
        
        assert result['success'] == False
        assert "No available seating" in result['message']
        
    def test_process_reservation_low_balance(self):
        """Test reservation failure due to low funds"""
        item_id = self.restaurant.add_menu_item(
            "Expensive Dish", 600.00, "Main", ["meat"], 25, 1000, None, "16oz", "hot"
        )
        guest_id = self.restaurant.register_guest("Low Funds", "low@test.com", 1)
        
        result = self.restaurant.process_reservation_and_order(
            guest_id,
            1,
            [{'item_id': item_id, 'quantity': 1}],
            "15:00",
            "None"
        )
        
        assert result['success'] == False
        assert "Insufficient funds" in result['message']
        
    def test_estimate_prep_time(self):
        """Test preparation time estimation"""
        item_id = self.restaurant.add_menu_item(
            "Quick Item", 10.00, "Snack", ["fruit"], 5, 100, None, "2oz", "mild"
        )
        guest_id = self.restaurant.register_guest("Prep Test", "prep@test.com", 1)
        
        result = self.restaurant.process_reservation_and_order(
            guest_id,
            1,
            [{'item_id': item_id, 'quantity': 2}],
            "12:00",
            "None"
        )
        
        prep_time = self.restaurant.estimate_prep_time(result['res_id'])
        assert prep_time > 0
        assert isinstance(prep_time, float)
        
    def test_compute_loyalty_reward(self):
        """Test reward computation for levels"""
        guest_id = self.restaurant.register_guest("Reward Guest", "reward@test.com", 2)
        item_id = self.restaurant.add_menu_item(
            "Reward Item", 50.00, "Main", ["pasta"], 10, 400, None, "8oz", "mild"
        )
        
        self.restaurant.process_reservation_and_order(
            guest_id,
            1,
            [{'item_id': item_id, 'quantity': 1}],
            "16:00",
            "None"
        )
        
        reward = self.restaurant.compute_loyalty_reward(guest_id)
        assert reward > 0
        
    def test_generate_menu_report(self):
        """Test menu report generation"""
        self.restaurant.add_menu_item(
            "Report Item1", 20.00, "Cat1", ["ing"], 8, 250, None, "5oz", "mild"
        )
        self.restaurant.add_menu_item(
            "Report Item2", 30.00, "Cat2", ["ing2"], 12, 350, None, "7oz", "hot"
        )
        
        report = self.restaurant.generate_menu_report()
        assert len(report) == 2
        assert all('item_id' in item for item in report)
        assert all('name' in item for item in report)
        assert all('stock' in item for item in report)


class TestReservationReporter:
    """Test suite for ReservationReporter"""
    
    def setup_method(self):
        """Setup reporter with data"""
        self.restaurant = RestaurantManager()
        self.reporter = ReservationReporter(self.restaurant)
        
        # Add initial data
        self.i1 = self.restaurant.add_menu_item(
            "Reporter Item1", 25.00, "Cat1", ["ing1"], 10, 300, None, "6oz", "mild"
        )
        self.i2 = self.restaurant.add_menu_item(
            "Reporter Item2", 35.00, "Cat2", ["ing2"], 15, 400, None, "9oz", "hot"
        )
        self.g1 = self.restaurant.register_guest("Reporter Guest1", "g1@test.com", 2)
        self.g2 = self.restaurant.register_guest("Reporter Guest2", "g2@test.com", 1)
        
    def test_get_best_selling_items(self):
        """Test best sellers retrieval"""
        self.restaurant.process_reservation_and_order(self.g1, 1, [{'item_id': self.i1, 'quantity': 4}], "17:00", "None")
        self.restaurant.process_reservation_and_order(self.g2, 1, [{'item_id': self.i2, 'quantity': 1}], "18:00", "None")
        
        best_items = self.reporter.get_best_selling_items(2)
        assert len(best_items) <= 2
        assert best_items[0]['served'] >= best_items[1]['served']
        
    def test_get_guest_history(self):
        """Test guest history fetch"""
        self.restaurant.process_reservation_and_order(self.g1, 1, [{'item_id': self.i1, 'quantity': 1}], "19:00", "None")
        
        history = self.reporter.get_guest_history(self.g1)
        assert history is not None
        assert history['name'] == "Reporter Guest1"
        assert history['reservations_made'] == 1
        assert history['total_spent'] > 0
        
    def test_get_top_guests(self):
        """Test top guests identification"""
        self.restaurant.process_reservation_and_order(self.g1, 1, [{'item_id': self.i1, 'quantity': 3}], "20:00", "None")
        self.restaurant.process_reservation_and_order(self.g2, 1, [{'item_id': self.i2, 'quantity': 1}], "21:00", "None")
        
        top_guests = self.reporter.get_top_guests(2)
        assert len(top_guests) <= 2
        assert top_guests[0]['total_spent'] >= top_guests[1]['total_spent']