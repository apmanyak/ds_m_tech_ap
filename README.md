# M.TECH (Тестовое задание)

Руководство компании обратило внимание на то, что сотрудники старше 35 лет болеют чаще, чем более молодые сотрудники. Кроме этого, среди мужчин количество пропусков рабочих дней в связи с больничным выше, чем среди женщин. В связи с этой ситуацией, руководство организации планирует ввести дополнительные медицинские осмотры среди групп риска.

Необходимо проверить следующие гипотезы:
1) Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.
2) Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.

Все необходимые данные содержатся в файле «М.Тех_Данные_к_ТЗ_DS.csv» [ссылка](https://github.com/apmanyak/ds_m_tech_ap/tree/main/data).

Стэк:Python, Pandas, Matplotlib, Seaborn, Scipy, Streamlit, Git, Docker.

Решение необходимо было предоставить:
1) В виде jupyter notebook. [тетрадка](https://github.com/apmanyak/ds_m_tech_ap/tree/main/ipynb)
2) В виде дашборда на Streamlit с простым функционалом (должна быть возможность загрузить .csv, в формате аналогично файлу «М.Тех_Данные_к_ТЗ_DS.csv») [код проекта](https://github.com/apmanyak/ds_m_tech_ap/tree/main/app)

Код проекта должен быть обернут в docker.


## Запуск проекта 

1. Запускаем терминал и скачиваем репозиторий
   
```bash

git clone https://github.com/apmanyak/ds_m_tech_ap.git

```

2. В терминале переходим в папку проекта
   
```bash

cd ds_m_tech_ap

```

3. Запускаем приложение docker и коамандой в терминале запускаем проект
   
```bash

docker-compose up

```

После создания контейнеров и образов в терминале отобразятся ссылки:
- на работу в Streamlit [localhost:8501](http://localhost:8501). 
- на работу в JupiterLab к примеру, [http://localhost:8888](http://localhost:8888) (с указанным токеном для входа) 

В приложении docker также отобразятя контейнеры и образы.


Внешний вид стартовой страницы проекта в Streamlit

<p align="center">
  <img width="1539" alt="Снимок экрана 2023-12-17 в 16 50 21" src="https://github.com/apmanyak/ds_m_tech_ap/assets/132745728/704e1e0d-454c-4eeb-88fe-d2ce51e453c4">
</p>

После изучения проекта для его остановки необходимо ввести:

```bash
docker-compose stop
```

Если необходимо остановить и удалить при этом контейнеры и образы:

```bash
docker-compose down --rmi all
```

Или вручную через приложение docker