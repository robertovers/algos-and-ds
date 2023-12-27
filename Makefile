test:
	python -m pytest

test-sorting:
	python -m pytest sorting/test_sorting_correctness.py
	python -m sorting.test_sorting_performance
