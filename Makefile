# install the library into system python
install:
	# find the most recent wheel to install
	poetry build && pip install `ls -tr dist/*.whl | tail -1` --upgrade

force_install:
	# find the most recent wheel to install
	poetry build && pip install `ls -tr dist/*.whl | tail -1` --upgrade --force-install

publish:
	# poetry publish
	twine upload dist/*

.PHONY: install force_install
