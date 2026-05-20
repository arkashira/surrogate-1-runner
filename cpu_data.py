# Mock CPU data for demonstration purposes
cpus = [
    {"id": 1, "brand": "Intel", "model": "i7-12700K", "price": 409.99, "performance": 95},
    {"id": 2, "brand": "AMD", "model": "Ryzen 9 7950X", "price": 699.00, "performance": 98},
    {"id": 3, "brand": "Intel", "model": "Core i5-12600K", "price": 224.99, "performance": 85},
    # Add more CPUs as needed
]

def get_cpus():
    return cpus

def filter_cpus(cpus, brand=None, min_price=None, max_price=None, min_performance=None, max_performance=None):
    filtered_cpus = cpus

    if brand:
        filtered_cpus = [cpu for cpu in filtered_cpus if cpu['brand'] == brand]

    if min_price:
        filtered_cpus = [cpu for cpu in filtered_cpus if cpu['price'] >= min_price]

    if max_price:
        filtered_cpus = [cpu for cpu in filtered_cpus if cpu['price'] <= max_price]

    if min_performance:
        filtered_cpus = [cpu for cpu in filtered_cpus if cpu['performance'] >= min_performance]

    if max_performance:
        filtered_cpus = [cpu for cpu in filtered_cpus if cpu['performance'] <= max_performance]

    return filtered_cpus