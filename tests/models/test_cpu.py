import unittest
from models.cpu import CPU, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class TestCPUModel(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def test_cpu_model_creation(self):
        cpu = CPU(
            brand="Intel",
            model="i9-13900K",
            cores=24,
            threads=32,
            base_clock=3.0,
            boost_clock=5.8,
            cache=36,
            tdp=150,
            price=589.99,
            performance_score=12000
        )
        session = self.Session()
        session.add(cpu)
        session.commit()
        
        result = session.query(CPU).first()
        self.assertEqual(result.brand, "Intel")
        self.assertEqual(result.model, "i9-13900K")
        self.assertEqual(result.cores, 24)
        self.assertEqual(result.threads, 32)
        self.assertEqual(result.base_clock, 3.0)
        self.assertEqual(result.boost_clock, 5.8)
        self.assertEqual(result.cache, 36)
        self.assertEqual(result.tdp, 150)
        self.assertEqual(str(result.price), "589.99")
        self.assertEqual(result.performance_score, 12000)

if __name__ == '__main__':
    unittest.main()