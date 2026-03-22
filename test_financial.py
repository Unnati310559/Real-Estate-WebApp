from services.financial import calculate_noi, calculate_cap_rate, calculate_cashflow, calculate_roi, calculate_irr


def test_noi():
    assert calculate_noi(36000, 10000) == 26000


def test_cap_rate():
    noi = 26000
    price = 400000
    assert round(calculate_cap_rate(noi, price), 2) == round((26000/400000)*100, 2)


def test_cashflow():
    assert calculate_cashflow(36000, 10000, 15000) == 11000


def test_roi():
    cashflow = 11000
    years = 5
    price = 400000
    expected = (cashflow * years / price) * 100
    assert round(calculate_roi(cashflow * years, price), 2) == round(expected, 2)


def test_irr():
    irr = calculate_irr(400000, 11000, 5)
    assert irr is not None