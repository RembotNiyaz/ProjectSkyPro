import pytest
from decorator.decorators import log


# Тесты
def test_success_logging(success_function):
    result = success_function(2, 3)
    assert result == 5

    with open("test_success.log", "r") as f:
        logs = f.readlines()
        assert "add начало\n" in logs
        assert "add ok\n" in logs


def test_error_logging(error_function):
    with pytest.raises(TypeError):
        error_function(1)

    with open("test_error.log", "r") as f:
        logs = f.readlines()
        assert "faulty_func error: TypeError. Inputs: (1,), {}\n" in logs


def test_console_logging(console_function, capsys):
    result = console_function(2, 3)
    assert result == 6

    captured = capsys.readouterr()
    assert "multiply начало" in captured.out
    assert "multiply ok" in captured.out


def test_empty_args():
    @log()
    def empty_func():
        return "test"

    result = empty_func()
    assert result == "test"


def test_kwargs():
    @log()
    def kwargs_func(x, y=2):
        return x + y

    result = kwargs_func(1, y=3)
    assert result == 4
