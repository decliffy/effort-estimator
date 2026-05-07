from estimator.sizes import TShirtSize, SizeDefinition, SIZE_DEFINITIONS


def test_tshirt_size_has_exactly_six_values():
    assert set(TShirtSize) == {
        TShirtSize.XS,
        TShirtSize.S,
        TShirtSize.M,
        TShirtSize.L,
        TShirtSize.XL,
        TShirtSize.XXL,
    }


def test_tshirt_size_values_are_strings():
    for size in TShirtSize:
        assert isinstance(size.value, str)


def test_size_definitions_covers_all_sizes():
    defined = {sd.size for sd in SIZE_DEFINITIONS}
    assert defined == set(TShirtSize)


def test_size_definition_fields_populated():
    for sd in SIZE_DEFINITIONS:
        assert isinstance(sd, SizeDefinition)
        assert sd.size in TShirtSize
        assert sd.effort_range and isinstance(sd.effort_range, str)
        assert sd.description and isinstance(sd.description, str)
        assert isinstance(sd.indicators, list) and len(sd.indicators) >= 1
        for indicator in sd.indicators:
            assert isinstance(indicator, str) and indicator


def test_size_definitions_ordered():
    expected_order = [
        TShirtSize.XS,
        TShirtSize.S,
        TShirtSize.M,
        TShirtSize.L,
        TShirtSize.XL,
        TShirtSize.XXL,
    ]
    actual_order = [sd.size for sd in SIZE_DEFINITIONS]
    assert actual_order == expected_order
