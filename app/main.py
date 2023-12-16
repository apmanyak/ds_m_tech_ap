import streamlit as st
import pandas as pd
import scipy.stats
import matplotlib.pyplot as plt
import seaborn as sns

#функция чтения файла и предварительной обработки
def read_file(file):
    df = pd.read_csv(file, encoding="cp1251", sep=",")
    list_columns = [
        df.columns.str.split(",")[0][i].replace('"', "")
        for i in range(len(df.columns.str.split(",")[0]))
    ]
    df[list_columns] = df[df.columns[0]].str.split(",", expand=True)
    df = df.drop(['Количество больничных дней,"Возраст","Пол"'], axis=1)
    df["Пол"] = [df.loc[i, "Пол"].replace('"', "") for i in range(len(df))]
    df["Количество больничных дней"] = df["Количество больничных дней"].astype("int")
    df["Возраст"] = df["Возраст"].astype("int")
    return df

#функция построения распределния значений для числовых столбцов
def info_plot(data, value):
    print()
    sns.set()
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(15, 8))
    axes[0].hist(data[value], bins=100)
    axes[0].set_title(f"Гистограмма для столбца {value}")
    axes[0].set_ylabel("Кол-во")
    sns.boxplot(x=data[value], ax=axes[1])
    axes[1].set_title(f'График "ящика с усами" для столбца {value}')
    return fig

#функция построения распределния значений для категораьных столбцов
def info_plot_category(data, value):
    group_gender = pd.DataFrame(data[value].value_counts().reset_index())
    group_gender['count,%'] = group_gender['count']/len(df) * 100
    fig = plt.figure(figsize=(8,4))
    plt.title('Столбец = Пол')
    plt.bar(group_gender[f'{group_gender.columns[0]}'],group_gender[f'{group_gender.columns[1]}']);
    plt.xlabel('Пол')
    plt.ylabel('Количество')
    return fig

#функция построения распределния значений для гипотезы 1
def info_plot_hypotize_1(df, work_days_1):
    df_work_days_1 = df[df['Количество больничных дней'] > work_days_1].reset_index(drop=True)
    st_gender = (
        df_work_days_1.pivot_table(
            index=["Пол", "Количество больничных дней"],
            values=["Количество больничных дней"],
            aggfunc=["count"],
        )
        .round(2)
        .reset_index()
    )
    
    st_gender.columns = [
        "gender",
        "work_days",
        "work_days_count"
    ]
    
    st_gender.loc[
        st_gender["gender"] == "Ж", "frequency"
    ] = (
        st_gender.loc[
            st_gender["gender"] == "Ж", "work_days_count"
        ]
        / st_gender[st_gender["gender"] == "Ж"]["work_days_count"].sum()
    ).round(
        4
    )
    
    st_gender.loc[
        st_gender["gender"] == "М", "frequency"
    ] = (
        st_gender.loc[
            st_gender["gender"] == "М", "work_days_count"
        ]
        / st_gender[st_gender["gender"] == "М"]["work_days_count"].sum()
    ).round(
        4
    )
    
    fig = plt.figure(figsize=(15, 8))
    ax = sns.barplot(x='work_days',
            y='work_days_count',
            hue="gender",
            data=st_gender,
            palette=['lightblue', 'blue'])

    ax.set_title('Распределение количества пропусков сотрудниками по кол-ву пропущенных дней')
    ax.set(xlabel='Кол-во пропущенных дней', ylabel='Кол-во сотрудников');
    fig_1 = plt.figure(figsize=(15, 8))
    ax_1 = sns.barplot(x='work_days',
            y='frequency',
            hue="gender",
            data=st_gender,
            palette=['lightblue', 'blue'])

    ax_1.set_title('Распределение относительной частоты пропусков сотрудников по кол-ву пропущенных дней')
    ax_1.set(xlabel='Кол-во пропущенных дней', ylabel='Относительная частота');
    
    return fig,fig_1


#функция построения распределния значений для гипотезы 2
def info_plot_hypotize_2(df, work_days_2,age):
    df_work_days_2 = df[df['Количество больничных дней'] > work_days_2].reset_index(drop=True)
    for i in range(len(df_work_days_2)):
        if df_work_days_2.loc[i,'Возраст'] > age:
            df_work_days_2.loc[i,'Возрастная группа'] = 'old'
        else:
            df_work_days_2.loc[i,'Возрастная группа'] = 'young'

    df_work_days_2.groupby('Возрастная группа').count().reset_index(col_level=True)
    df_work_days_2 = df_work_days_2.drop(columns=['Возраст'])
    
    st_group_age = (
        df_work_days_2.pivot_table(
            index=[ "Возрастная группа","Количество больничных дней"],
            values=["Количество больничных дней"],
            aggfunc=["count"],
        )
        .round(2)
        .reset_index()
)

    st_group_age.columns = [
        "group_age",
        "work_days",
        "work_days_count"
    ]
    
    st_group_age.loc[
        st_group_age["group_age"] == "old", "frequency"
    ] = (
        st_group_age.loc[
            st_group_age["group_age"] == "old", "work_days_count"
        ]
        / st_group_age[st_group_age["group_age"] == "old"]["work_days_count"].sum()
    ).round(
        4
    )
    
    st_group_age.loc[
        st_group_age["group_age"] == "young", "frequency"
    ] = (
        st_group_age.loc[
            st_group_age["group_age"] == "young", "work_days_count"
        ]
        / st_group_age[st_group_age["group_age"] == "young"]["work_days_count"].sum()
    ).round(
        4
    )
    
    fig = plt.figure(figsize=(15, 8))
    ax = sns.barplot(x='work_days',
                y='work_days_count',
                hue="group_age",
                data=st_group_age,
                palette=['lightblue', 'blue'])

    ax.set_title('Распределение количества пропусков сотрудниками по кол-ву пропущенных дней')
    ax.set(xlabel='Кол-во пропущенных дней', ylabel='Кол-во сотрудников');
    
    fig_1 = plt.figure(figsize=(15, 8))
    ax = sns.barplot(x='work_days',
                y='frequency',
                hue="group_age",
                data=st_group_age,
                palette=['lightblue', 'blue'])

    ax.set_title('Распределение относительной частоты пропусков сотрудников по кол-ву пропущенных дней')
    ax.set(xlabel='Кол-во пропущенных дней', ylabel='Относительная частота');
    
    return fig,fig_1

#функция расчета для гипотезы 1
def hypotize_1(df, work_days_1, alpha_1):
    df_work_days_1 = df[df["Количество больничных дней"] > work_days_1].reset_index(
        drop=True
    )
    st_male = df_work_days_1.loc[df_work_days_1["Пол"] == "М"][
        "Количество больничных дней"
    ]
    st_female = df_work_days_1.loc[df_work_days_1["Пол"] == "Ж"][
        "Количество больничных дней"
    ]
    results = scipy.stats.ttest_ind(st_male, st_female, equal_var=False)

    if results.pvalue < alpha_1:
        value = "Отвергаем нулевую гипотезу"
    else:
        value = "Не получилось отвергнуть нулевую гипотезу"
    return results.pvalue, value

#функция расчета для гипотезы 2
def hypotize_2(df, work_days_2, age, alpha_2):
    df_work_days_2 = df[df["Количество больничных дней"] > work_days_2].reset_index(
        drop=True
    )
    for i in range(len(df_work_days_2)):
        if df_work_days_2.loc[i, "Возраст"] > age:
            df_work_days_2.loc[i, "Возрастная группа"] = "old"
        else:
            df_work_days_2.loc[i, "Возрастная группа"] = "young"
    df_work_days_2 = df_work_days_2.drop(columns=["Возраст"])

    st_old = df_work_days_2.loc[df_work_days_2["Возрастная группа"] == "old"][
        "Количество больничных дней"
    ]
    st_young = df_work_days_2.loc[df_work_days_2["Возрастная группа"] == "young"][
        "Количество больничных дней"
    ]

    results = scipy.stats.ttest_ind(st_old, st_young, equal_var=False)

    if results.pvalue < alpha_2:
        value = "Отвергаем нулевую гипотезу"
    else:
        value = "Не получилось отвергнуть нулевую гипотезу"
    return results.pvalue, value



# Настройка заголовка и текста 
st.title("M.TECH.Тестовое задание")
st.markdown("---")
st.write(
    """Руководство компании обратило внимание на то, что сотрудники старше 35 лет болеют чаще, чем более молодые сотрудники. Кроме этого, среди мужчин количество пропусков рабочих дней в связи с больничным выше, чем среди женщин. В связи с этой ситуацией, руководство организации планирует ввести дополнительные медицинские осмотры среди групп риска.

Необходимо проверить следующие гипотезы:
1) Мужчины пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще женщин.
2) Работники старше 35 лет (age) пропускают в течение года более 2 рабочих дней (work_days) по болезни значимо чаще своих более молодых коллег.

Все необходимые данные содержатся в файле «М.Тех_Данные_к_ТЗ_DS.csv»."""
)


file = st.file_uploader("Загрузите файл", type="csv")


if file is not None:
    
    # чтение файла и его обработка
    df = read_file(file)
    st.markdown("---")
    
    # Настройка боковой панели
    st.sidebar.title("Параметры")
    st.sidebar.info("""Графики исходного загруженного датасета """)
    show_data = st.sidebar.checkbox('Показать таблицу')
    show_data_1 = st.sidebar.checkbox('График распределния данных по столбцу "Количество больничных дней"') 
    show_data_2 = st.sidebar.checkbox('График распределния данных по столбцу "Возраст"') 
    show_data_3 = st.sidebar.checkbox('График распределния данных по столбцу "Пол"') 
  
    
    st.sidebar.info(
        """
        Исходные параметры для гипотез
        """
        )
    
    alpha = st.sidebar.select_slider("Выбор порогоа alpha", options=[0.01, 0.05])
    work_days = st.sidebar.slider(
        "Выбор worker_day",
        min_value=df["Количество больничных дней"].min(),
        max_value=df["Количество больничных дней"].max(),
        value=2,
    )
    age = st.sidebar.slider(
        "Выбор age", min_value=df["Возраст"].min(), max_value=df["Возраст"].max(), value=35
        )
    
    st.sidebar.info("Графики распредления данных для гипотез")
    show_data_4 = st.sidebar.checkbox('График распределния данных для Гипотезы 1')
    show_data_5 = st.sidebar.checkbox('График распределния данных для Гипотезы 2')
    
    # Настройка основной части дашборда
    ## Вывод графиков щагруженного датасета
    
    if show_data == True:
        st.subheader('Загруженная таблиця')
        st.write(df)
        st.markdown("---")
    
    if show_data_1 == True:
        st.subheader('График распределния данных по столбцу "Количество больничных дней"')
        st.write(info_plot(df,'Количество больничных дней'))
        st.markdown("---")
    
    if show_data_2 == True:
        st.subheader('График распределния данных по столбцу "Возраст"')
        st.write(info_plot(df,'Возраст'))
        st.markdown("---")
    
    if show_data_3 == True:
        st.subheader('График распределния данных по столбцу "Возраст"')
        st.write(info_plot_category(df,'Пол'))
        st.markdown("---") 
    
    ## Расчет Гипотезы 1 и 2 
    st.write("Результаты")   
    p_value_1, value_1 = hypotize_1(df,work_days,alpha)
    p_value_2, value_2 = hypotize_2(df, work_days, age, alpha)
    st.write("Проверяем гипотезу с помощью scipy.stats.ttest_ind, так как с его помощью можно сравнить средние двух совокупностей. ")
    value_3 = 'Не рассматривается параметр'

    dd_1 = pd.DataFrame([alpha, work_days, value_3, p_value_1, value_1],
                        index=["alpha", "work_days", "age","p-значение","Ответ"], 
                        columns=["Гипотеза 1"])
    dd_2 = pd.DataFrame([alpha, work_days, age ,p_value_2, value_2],
                        index=["alpha", "work_days", "age","p-значение","Ответ"], 
                        columns=["Гипотеза 2"])

    st.write(pd.concat([dd_1,dd_2], axis=1))
    st.markdown("---")

    ## Гипотеза 1
    st.subheader('Гипотеза 1')
    st.write(f"""H_0: Кол-во больничных дней мужчин пропустивших в течение года более work_days = {work_days} рабочих дней по болезни  = Кол-во больничных дней женщин пропустивших в течение года более work_days = {work_days} рабочих дней по болезни

H_a: Кол-во больничных дней мужчин пропустивших в течение года более work_days = {work_days} рабочих дней  по болезни  ≠  Кол-во больничных дней женщин пропустивших в течение года более work_days = {work_days} рабочих дней  по болезни""")

    ## Вывод графиков Гипотезы 1
    if show_data_4 == True:
        st.subheader('График распределния данных для Гипотезы 1')
        plot_1, plot_2 = info_plot_hypotize_1(df, work_days)
        st.write(plot_1)
        st.write(plot_2)
        st.markdown("---")


## Гипотеза 2
    st.subheader('Гипотеза 2')
    st.write(f""" 
    H_0: Кол-во пропущенных дней сотрудниками старше age = {age} лет пропустивших в течение года более work_days = {work_days} рабочих дней  = Кол-во пропущенных дней сотрудниками age = {age} лет и младше пропустивших в течение года более work_days = {work_days} рабочих дней 
H_a: Кол-во пропущенных дней сотрудниками старше age = {age} лет пропустивших в течение года более work_days = {work_days} рабочих дней  ≠ Кол-во пропущенных дней сотрудниками age = {age} лет и младше пропустивших в течение года более work_days = {work_days} рабочих дней          
             """)


    ## Вывод графиков Гипотезы 2
    if show_data_5 == True:
        st.subheader('График распределния данных для Гипотезы 2')
        plot_1, plot_2 = info_plot_hypotize_2(df, work_days,age)
        st.write(plot_1)
        st.write(plot_2)
        st.markdown("---")
    