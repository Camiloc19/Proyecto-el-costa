from Controlador.controlador import puede_modificar_ordenes


def test_super_admin_puede_modificar_ordenes():
    assert puede_modificar_ordenes(1) is True


def test_admin_no_puede_modificar_ordenes():
    assert puede_modificar_ordenes(2) is False
    assert puede_modificar_ordenes(None) is False
