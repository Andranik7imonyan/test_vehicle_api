# Условия: должен быть установлен docker, Virtualization(Hyper V) должен быть включён

# Шаги
# 1) Скачать образ docker pull polarbearjngl/test-vehicle-api
# 2) Создать и запустить контейнер из образа docker run -p 8099 :8099 polarbearjngl/test-vehicle-api
#    Сервер работает по адресу - http://localhost:8099/ 
# 3) Создать virtual environment
# 4) Установить все зависимости python -m pip install -r requirements.txt
# 5) Запустить тесты с помощью команды python -B -m pytest -s --basehost={Ввести сюда url сервиса без эндпоинтов} Например:  http://localhost:8099/
# 6) Вывести allure-репорты в браузере allure serve allure-results

# The tests are stored in the tests_vehicle branch
# TOTAL 57 tests
