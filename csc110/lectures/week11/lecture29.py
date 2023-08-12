from __future__ import annotations

from dataclasses import dataclass
import datetime
from typing import Optional


@dataclass
class Vendor:
    """A vendor that sells groceries or meals.

    This could be a grocery store or restaurant.

    Instance Attributes:
      - name: the name of the vendor
      - address: the address of the vendor
      - menu: the menu of the vendor with the name of the food item mapping to
              its price
      - location: the location of the vendor as (latitude, longitude)

    Representation Invariants:
      - self.name != ''
      - self.address != ''
      - all(self.menu[item] >= 0 for item in self.menu)
      - -90.0 <= self.location[0] <= 90.0
      - -180.0 <= self.location[1] <= 180.0
    """
    name: str
    address: str
    menu: dict[str, float]
    location: tuple[float, float]  # (lat, lon) coordinates


@dataclass
class Customer:
    """A person who orders food.

    Instance Attributes:
      - name: the name of the customer
      - location: the location of the customer as (latitude, longitude)

    Representation Invariants:
      - self.name != ''
      - -90 <= self.location[0] <= 90
      - -180 <= self.location[1] <= 180
    """
    name: str
    location: tuple[float, float]


@dataclass
class Order:
    """A food order from a customer.

    Instance Attributes:
      - customer: the customer who placed this order
      - vendor: the vendor that the order is placed for
      - food_items: a mapping from names of food to the quantity being ordered
      - start_time: the time the order was placed
      - courier: the courier assigned to this order (initially None)
      - end_time: the time the order was completed by the courier (initially None)

    Representation Invariants:
      - all(self.food_items[item] >= 1 for item in self.food_items)
    """
    customer: Customer
    vendor: Vendor
    food_items: dict[str, int]
    start_time: datetime.datetime
    courier: Optional[Courier] = None
    end_time: Optional[datetime.datetime] = None


@dataclass
class Courier:
    """A person who delivers food orders from vendors to customers.

    Instance Attributes:
        - location: the location of the couriers as ...
        - orderL the order that the courier is currently ...



    Representation Invariants:
        - self.name != ''
        - -90 <= self.location[0] <= 90
        - -180 <= self.location[1] <= 180


    >>> courier = Courier('Courier 1', (44.639, -79215))
    >>> courier.order is None
    True
    """
    name: str
    location: tuple[float, float]
    order: Optional[Order] = None




class FoodDeliverySystem:
    """A system that maintains all entities (vendors, customers, couriers, and orders).

    Representation Invariants:
        - self.name != ''
        - all(vendor == self._vendors[vendor].name for vendor in self._vendors)
        - all(customer == self._customers[customer].name for customer in self._customers)
        - all(courier == self._couriers[courier].name for courier in self._couriers)
    """
    # Private Instance Attributes:
    #   - _vendors: a mapping from vendor name to Vendor object.
    #       This represents all the vendors in the system.
    #   - _customers: a mapping from customer name to Customer object.
    #       This represents all the customers in the system.
    #   - _couriers: a mapping from courier name to Courier object.
    #       This represents all the couriers in the system.
    #   - _orders: a list of all orders (both open and completed orders).

    _vendors: dict[str, Vendor]
    _customers: dict[str, Customer]
    _couriers: dict[str, Courier]
    _orders: list[Order]



    def __init__(self) -> None:
        """Initialize a new food delivery system.

        The system starts with no entities.
        """
        self.vendors = {}
        self.customers = {}
        self.couriers = {}
        self.orders = []



    def add_vendor(self, vendor: Vendor) -> bool:
        """Add the given vendor to this system.

        Do NOT add the vendor if one with the same name already exists.

        Return whether the vendor was successfully added to this system.
        """
        if vendor.name in self.vendors:
            return False
        else:
            self.vendors[vendor.name] = vendor
            return True
