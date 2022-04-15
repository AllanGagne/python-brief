import pytest
from flask import Flask

import app


@pytest.mark.home
@pytest.mark.httpRequest
def test_http_hello_world(fullapp: Flask):
    rep = fullapp.test_client().get("/")
    assert rep.status_code == 200
    assert b"Hello, World!" in rep.data


@pytest.mark.other
@pytest.mark.httpRequest
def test_http_other(fullapp: Flask):
    rep = fullapp.test_client().get("/other")
    assert rep.status_code == 200
    assert b"Hello, " in rep.data


@pytest.mark.exp
@pytest.mark.httpRequest
def test_http_exp(fullapp: Flask):
    with pytest.raises(TypeError):
        fullapp.test_client().get("/exp")


@pytest.mark.other
@pytest.mark.paramSuccess
@pytest.mark.parametrize("arg", [1, 10, 200])
def test_other_param(fullapp: Flask, arg):
    arg = str(arg)
    rep = fullapp.test_client().get("/other?page=" + arg)
    expect = "Page : " + arg
    assert expect.encode() in rep.data


@pytest.mark.other
@pytest.mark.paramFail
@pytest.mark.parametrize("arg", [6.8, "bonjour"])
def test_other_param_fail(fullapp: Flask, arg):
    arg = str(arg)
    rep = fullapp.test_client().get("/other?page=" + arg)
    expect = "Page : " + arg
    assert not expect.encode() in rep.data


@pytest.mark.exp
@pytest.mark.paramSuccess
@pytest.mark.parametrize("arg", [1, 2, 5])
def test_exp_param(fullapp: Flask, arg):
    arg = str(arg)
    rep = fullapp.test_client().get("/exp?value=" + arg)
    assert rep.status_code == 200


@pytest.mark.exp
@pytest.mark.paramFail
@pytest.mark.parametrize("arg", ["fail", 6.8])
def test_exp_param_fail(fullapp: Flask, arg):
    arg = str(arg)
    with pytest.raises(ValueError):
        fullapp.test_client().get("/exp?value=" + arg)


@pytest.mark.mockhome
def test_mock_home(mocker):
    def mock_data():
        return "<p>Bonjour, Monde!</p>"

    mocker.patch('app.hello_world', mock_data)
    assert app.hello_world() == mock_data()
