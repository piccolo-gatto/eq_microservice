help:
	@echo "Make project with following instructions"
	@cat Makefile
dev:
	pip install -e .

test: dev
	pytest

build: clean
	pip install wheel
	python setup.py bdist_wheel

clean:
	@if exist .pytest_cache (rmdir /s /q .pytest_cache)
	@if exist .mypy_cache (rmdir /s /q .mypy_cache)
	@if exist junit (rmdir /s /q junit)
	@if exist build (rmdir /s /q build)
	@if exist dist (rmdir /s /q dist)
	@if exist turkey_eq/pycache (rmdir /s /q turkey_eq/pycache)
	@if exist tests/pycache (rmdir /s /q tests/pycache)
	@if exist turkey_eq.egg-info (rmdir /s /q turkey_eq.egg-info)
	@for /r %%i in (pycache) do @if exist "%%i" del /s /q "%%i"
	@for /r %%i in (__pycache__) do @if exist "%%i" rmdir /s /q "%%i"
