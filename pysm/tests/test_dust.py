import pytest
import numpy as np
import pysm
import pysm.component_models.galactic.dust as dust
import astropy.units as units
from astropy.units import UnitsError


def test_blackbody_ratio():
    nu_from = 100.
    nu_to = 400.
    temp = np.array([20.])

    np.testing.assert_allclose(dust.blackbody_ratio(nu_to, nu_from, temp), np.array([10.77195547]))


@pytest.mark.parametrize("freq", [30, 100, 353])
@pytest.mark.parametrize("model_tag", ["d1"])
# @pytest.mark.parametrize("model_tag", ["d1", "d2", "d3"]) # FIXME activate testing for other models
def test_dust_model(model_tag, freq):

    model = pysm.preset_models(model_tag, nside=64)

    model_number = {"d1": 1, "d2": 6, "d3": 9}[model_tag]
    expected_output = pysm.read_map(
        "pysm_2_test_data/check{}therm_{}p0_64.fits".format(model_number, freq),
        64,
        field=(0, 1, 2),
    )

    np.testing.assert_allclose(
        expected_output.value, model.get_emission(freq * units.GHz).value, rtol=1e-4, atol=0
    )
