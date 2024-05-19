from django.db import models

class NodeChoices(models.TextChoices):
    ROUTER = "router", "Router"
    SWITCH = "switch", "Switch"
    ACCESS_POINT = "access_point", "Access Point"
    SERVER = "server", "Server"
    DESKTOP = "desktop", "Desktop"
    LAPTOP = "laptop", "Laptop"
    PRINTER = "printer", "Printer"
    PHONE = "phone", "Phone"
    TABLET = "tablet", "Tablet"
    BASE_STATION = "base_station", "Base Station"
    MSC = "msc", "Mobile Switching Center"
    FIREWALL = "firewall", "Firewall"
    GATEWAY = "gateway", "Gateway"
    RAN = "ran", "Radio Access Network"

class StatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    MAINTENANCE = "maintenance", "Maintenance"
    DECOMMISSIONED = "decommissioned", "Decommissioned"
