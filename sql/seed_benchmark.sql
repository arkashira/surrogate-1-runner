-- Component price data for recommendation testing
INSERT INTO components (type, name, price, compatibility_profile) VALUES
('cpu', 'Intel i5-12600K', 299, '{"socket": "LGA1700", "power": 125}'),
('cpu', 'AMD Ryzen 5 7600X', 249, '{"socket": "AM5", "power": 105}'),
('gpu', 'NVIDIA RTX 4060', 299, '{"pci": "PCIe 5.0", "power": 150}'),
('gpu', 'AMD RX 7600 XT', 279, '{"pci": "PCIe 4.0", "power": 170}'),
('ram', 'Corsair Vengeance 16GB', 79, '{"speed": "3200MHz", "type": "DDR4"}'),
('storage', 'Samsung 970 EVO', 129, '{"interface": "NVMe", "capacity": "1TB"}');

-- Predefined compatible bundles
INSERT INTO bundles (name, component_ids) VALUES
('Budget Upgrade Bundle', '[1,3,5,6]'),
('High Efficiency Bundle', '[2,4,5,6]');