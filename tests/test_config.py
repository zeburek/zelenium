from zelenium import expected_conditions as EC
from zelenium.base.config import _Config
from zelenium.base.config import Config


def test_access_default_attributes(driver):
    conf = _Config(
        driver=driver,
        default_expected_condition=EC.visibility_of_element_located,
        default_wait_time=2,
        default_poll_frequency=0.5,
    )
    assert conf.d == conf.driver == driver
    assert (
        conf.dec
        == conf.default_expected_condition
        == EC.visibility_of_element_located
    )
    assert conf.dwt == conf.default_wait_time == 2
    assert conf.dpf == conf.default_poll_frequency == 0.5


def test_config_is_singleton(driver):
    conf1 = Config.get_instance()
    conf2 = Config.get_instance()
    conf1.driver = driver
    assert conf1 is conf2
    assert conf1.driver is conf2.driver
