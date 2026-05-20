import unittest
import platform
import sys
import pytest

SUPPORTED_DISTROS = {"ubuntu", "debian", "fedora"}

def get_distro_name():
    """
    Return a lowercase distro name from platform.linux_distribution()
    (deprecated) or distro module if available.
    """
    try:
        # Python 3.8+ removed platform.linux_distribution
        import distro  # type: ignore
        return distro.id().lower()
    except Exception:
        # Fallback to platform.linux_distribution if available
        try:
            dist = platform.linux_distribution()  # type: ignore
            return dist[0].lower()
        except Exception:
            return ""

@pytest.mark.skipif(sys.platform != "linux", reason="Non-Linux platform")
def test_linux_distribution_supported():
    """
    Ensure the current Linux distribution is one of the supported ones.
    """
    distro_name = get_distro_name()
    assert distro_name in SUPPORTED_DISTROS, (
        f"Unsupported Linux distribution '{distro_name}'. "
        f"Supported: {', '.join(SUPPORTED_DISTROS)}"
    )

@pytest.mark.skipif(sys.platform != "linux", reason="Non-Linux platform")
def test_python_version():
    """
    Ensure the Python version is 3.8 or newer, which is required for this project.
    """
    major, minor = sys.version_info[:2]
    assert (major, minor) >= (3, 8), (
        f"Python {major}.{minor} is not supported. "
        "Python 3.8 or newer is required."
    )

class TestCompatibility(unittest.TestCase):

    def test_ubuntu(self):
        # Test on Ubuntu
        self.assertTrue(self.check_distribution('Ubuntu'))

    def test_fedora(self):
        # Test on Fedora
        self.assertTrue(self.check_distribution('Fedora'))

    def test_debian(self):
        # Test on Debian
        self.assertTrue(self.check_distribution('Debian'))

    def check_distribution(self, distribution):
        # Check if the current distribution is the one being tested
        distro_name = get_distro_name()
        return distro_name == distribution

if __name__ == '__main__':
    pytest.main()