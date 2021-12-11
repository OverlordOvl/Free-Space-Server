PYTHONPATH=.:../

revision:
ifdef message
	cd .. && . ./venv/Scripts/activate && cd schema && PYTHONPATH=${PYTHONPATH} alembic revision --autogenerate -m "${message}"
else
	cd .. && . ./venv/Scripts/activate && cd schema && PYTHONPATH=${PYTHONPATH} alembic revision --autogenerate
endif

upgrade:
	cd .. && . ./venv/Scripts/activate && cd schema && PYTHONPATH=${PYTHONPATH} alembic upgrade head

downgrade:
	cd .. && . ./venv/Scripts/activate && cd schema && PYTHONPATH=${PYTHONPATH} alembic downgrade -1
