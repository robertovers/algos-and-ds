test:
	pytest

test-sorting:
	pytest sorting/test_sorting_correctness.py
	python3 sorting/test_sorting_performance.py
