# Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama

# Mission 1

# Q1
import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.colors as colors



st.set_page_config(page_title="İstanbul Barajları Doluluk Oranı Tahminleme Modeli", page_icon="🖖")
# st.title("Rule Based Classification of Customer's Data")
st.markdown("<h2 style='text-align: center; color: grey;'>İstanbul Barajları Doluluk Oranı Tahminleme Modeli </h2>", unsafe_allow_html=True)
"""

Bu tahmin modeli, İBB Açık Veri Portalı'nda sunulan, İstanbul Baraj Doluluk oranlarına ait verisetleri kullanılarak, gelecek dönemdeki 
toplam baraj doluluk oranlarının tahmini için tasarlanmıştır. 

Uygulamanın kullanımı için, kullanıcı tarafından belirli bir gün, ay ve yıl tercihi yapması yeterli olacaktır. Ardından ilgili model,
İstanbul'daki barajların toplam doluluk oranı sunacaktır.


Çalışma; Alper Umut Keskin, Hakan Keskin, Oğuz Çalışkan ve Uğur Sarıçam tarafından yapılmış ve kullanıma sunulmuştur.

"""

pd.set_option("display.width", 500)
pd.set_option("display.max_columns", None)

# main_file_name = (r'C:\Users\hakan\OneDrive\Masaüstü\DSMLBC 11\07_Donem_Projesı\01_Models\SARIMAX_DAM_DAILY_3.xlsx') # change it to the name of your excel file
# #
# predicted_name = (r'C:\Users\hakan\OneDrive\Masaüstü\DSMLBC 11\07_Donem_Projesı\01_Models\predicted_data.xlsx') # change it to the name of your excel file

main_file_name = "SARIMAX_DAM_DAILY_3.xlsx"
predicted_name = "predicted_data.xlsx"

main_df = pd.read_excel(main_file_name)
pred_df = pd.read_excel(predicted_name)

# # Mission 8
#

st.sidebar.header("Görselleştirme:")

visual_method = st.sidebar.selectbox("Ana Veri: ", {"Geçmiş Veri", "Gelecek Veri"}, index=0)

if visual_method == "Geçmiş Veri":
    data_type = st.sidebar.selectbox("Veri Tipi: ", {"Nüfus", "Barajlar"}, index = 1)
    if data_type == "Barajlar":
        dam_name = st.sidebar.selectbox("Baraj: ",
                                        {"Hepsi","Omerli", "Alibey", "Darlik", "Elmali", "Terkos", "Buyukcekmece", "Sazlidere","Kazandere", "Pabucdere", "Istrancalar"}, index = 0)
elif visual_method == "Gelecek Veri":
    full_data = st.sidebar.selectbox("Veri Tipi: ", {"Baraj Doluluk"})


st.sidebar.header("Tahmin Edilecek Tarih Bilgileri:")

if visual_method == "Gelecek Veri":
    month = st.sidebar.number_input("Ay", value=2, step=1, min_value=1, max_value=12)
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day = st.sidebar.number_input("Gün", value=1, step=1, min_value=1, max_value=31)
    elif month == 2:
        day = st.sidebar.number_input("Gün", value=1, step=1, min_value=1, max_value=28)
    else:
        day = st.sidebar.number_input("Gün", value=22, step=1, min_value=1, max_value=30)

    year = st.sidebar.number_input("Yıl",value=2021, step=1, min_value=2021, max_value = 2025)

elif visual_method == "Geçmiş Veri":
    month = st.sidebar.number_input("Ay", value=1, step=1, min_value=1, max_value=12)
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        day = st.sidebar.number_input("Gün", value=1, step=1, min_value=1, max_value=31)
    elif month == 2:
        day = st.sidebar.number_input("Gün", value=1, step=1, min_value=1, max_value=28)
    else:
        day = st.sidebar.number_input("Gün", value=1, step=1, min_value=1, max_value=30)

    year = st.sidebar.number_input("Yıl",value=2021, step=1, min_value=2012, max_value = 2021)


# Tarih filtresi
selected_date = pd.to_datetime(str(year)+"-"+str(month)+"-"+str(day))

# filtered_df = main_df[main_df['DATE_'] == selected_date]

# Filtrelenmiş veri serisi

# dam_name = "Hepsi"

if visual_method == "Geçmiş Veri":
    if data_type == "Barajlar":
        if dam_name == "Hepsi":

            #####################################
            # Tüm Barajların ilgili güne ait baraj doluluk değerlerinin dağılımı
            #####################################

            first_day = main_df["DATE_"][0]
            first_day_new = first_day.strftime("%d-%m-%Y")
            selected = selected_date.strftime("%d-%m-%Y")

            st.markdown(
                f"""
                <h2 style="text-align: center; font-size: 20px;">{selected} Tarihindeki Baraj Doluluk Oranları Dağılımı</h2>
                """,
                unsafe_allow_html=True
            )

            filtered_data = main_df[main_df['DATE_'] == selected_date]
            values = filtered_data[['Omerli', 'Darlik', 'Elmali', 'Terkos', 'Alibey', 'Buyukcekmece', 'Sazlidere', 'Kazandere', 'Pabucdere', 'Istrancalar']]

            # İlk satırı seçme
            row = values.iloc[0]

            # Değişkenler ve değerler
            labels = row.index
            values = row.values

            # Pasta grafiği oluşturma
            fig = go.Figure(data=go.Pie(labels=labels, values=values))

            # Layout ayarları
            fig.update_layout(
                title='Veri Dağılımı',
                height=500,  # Pasta grafiğinin yüksekliğini buradan ayarlayabilirsiniz
                width=700,  # Pasta grafiğinin genişliğini buradan ayarlayabilirsiniz
                margin=dict(l=50, r=50, t=100, b=50),  # Grafik kenar boşluklarını ayarlayabilirsiniz
            )

            st.plotly_chart(fig)

            #####################################
            # Baraj doluluk değerleri 2 haftalık
            #####################################

            # labels = filtered_df['DATE_']
            new_date = selected_date - pd.DateOffset(weeks=2)
            filtered_data = main_df[(main_df['DATE_'] >= new_date) & (main_df['DATE_'] <= selected_date)]

            first_day_new = new_date.strftime("%d-%m-%Y")
            selected = selected_date.strftime("%d-%m-%Y")

            st.markdown(
                f"""
                <h2 style="text-align: center; font-size: 20px;">{first_day_new} - {selected} Tarihleri Arasındaki Baraj Doluluk Seviyeleri</h2>
                """,
                unsafe_allow_html=True
            )

            # Renk paleti

            # Veriye uygun bir başlangıç noktası belirleme
            start_index = filtered_data["BARAJ_DOLULUK"].idxmax()

            # Bar chart oluşturma
            fig = go.Figure(
                data=[go.Bar(x=filtered_data['DATE_'], y=filtered_data["BARAJ_DOLULUK"])])

            # X ve Y ekseni etiketleri
            fig.update_layout(xaxis_title='Tarih', yaxis_title='Değer')

            # # Grafiği görselleştirme
            # fig.show()

            # Grafiği görselleştirme
            # fig.show(renderer="browser")

            st.plotly_chart(fig)

        elif dam_name != "Hepsi":
            # labels = filtered_df['DATE_']
            new_date = selected_date - pd.DateOffset(weeks=2)
            filtered_data = main_df[(main_df['DATE_'] >= new_date) & (main_df['DATE_'] <= selected_date)]


            first_day_new = new_date.strftime("%d-%m-%Y")
            selected = selected_date.strftime("%d-%m-%Y")

            st.markdown(
                f"""
                <h2 style="text-align: center; font-size: 20px;">{first_day_new} - {selected} Tarihleri Arasındaki {dam_name} Barajı Doluluk Seviyeleri</h2>
                """,
                unsafe_allow_html=True
            )

            # # Renk paleti
            # colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)',
            #           'rgb(140, 86, 75)', 'rgb(227, 119, 194)', 'rgb(127, 127, 127)', 'rgb(188, 189, 34)', 'rgb(23, 190, 207)']

            # Veriye uygun bir başlangıç noktası belirleme
            start_index = filtered_data[dam_name].idxmax()

            # Renk paletini oluşturma
            color_palette = colors.qualitative.Plotly

            # Renk paleti ton sayısı
            num_tones = 15

            # Renk tonları listesi
            tone_colors = [color_palette[i % len(color_palette)] for i in range(num_tones)]

            # # Bar chart oluşturma
            # fig = go.Figure(data=[go.Bar(x=filtered_data['DATE_'], y=filtered_data[dam_name], marker=dict(color=colors))])

            # Çubukları renklendirme
            fig = go.Figure(data=[go.Bar(
                x=filtered_data['DATE_'],
                y=filtered_data[dam_name],
                marker=dict(
                    color=tone_colors
                )
            )])

            # X ve Y ekseni etiketleri
            fig.update_layout(xaxis_title='Tarih', yaxis_title='Doluluk [m3]')

            # # Grafiği görselleştirme
            # fig.show()

            # Grafiği görselleştirme
            # fig.show(renderer="browser")

            st.plotly_chart(fig)

            #####################################
            # SEÇİLİ BARAJIN SON BİR YILDAKİ AY SONLARI DOLULUK DEĞERLERİ (%)
            #####################################

            filtered_data = main_df[main_df['DATE_'] <= selected_date]
            selected_date = pd.to_datetime(str(year)+"-"+str(month)+"-"+str(day))

            # Son bir yıldaki aylık veriye denk gelen ayın son günlerini seçmek
            son_bir_yil_once = selected_date - timedelta(days=365)

            secilen_gunler = []
            for i in range(12):
                ay_basi = selected_date.replace(day=1) - timedelta(days=(i + 1) * 30)
                ay_sonu = ay_basi + pd.offsets.MonthEnd()
                if ay_basi >= son_bir_yil_once:
                    secilen_gunler.append(ay_sonu)

            secilen_gunler = pd.DataFrame(secilen_gunler)

            first_day_new = secilen_gunler.iloc[0][0].date().strftime("%d-%m-%Y")
            last_day_new = secilen_gunler.iloc[-1][0].date().strftime("%d-%m-%Y")

            st.markdown(
                f"""
                <h2 style="text-align: center; font-size: 20px;">{first_day_new} - {last_day_new} Tarihleri Arasındaki {dam_name} Barajı Doluluk Seviyeleri</h2>
                """,
                unsafe_allow_html=True
            )


            # "dam_name" e göre filtreleme yapma
            filtered_data = main_df[["DATE_", dam_name]]

            # Seçilen günlere göre filtreleme yapma
            filtered_data = filtered_data[filtered_data["DATE_"].isin(secilen_gunler[0])]

            # Bar grafiği oluşturma
            fig = go.Figure(data=[
                go.Bar(x=filtered_data["DATE_"], y=filtered_data[dam_name], marker_color='rgb(0, 128, 128)')
            ])

            # Grafik düzenlemeleri
            fig.update_layout(
                title=f"{dam_name} Verileri",
                xaxis_title="Tarih",
                yaxis_title=f"{dam_name} Değeri",
                barmode="group",
                showlegend=False
            )

            st.plotly_chart(fig)


    elif data_type == "Nüfus":
        filtered_data = main_df[main_df['DATE_'] <= selected_date]
        values = filtered_data[["DATE_", 'Toplam_Pop']]

        st.markdown(
            f"""
            <h2 style="text-align: center; font-size: 20px;">2011 - 2021 Tarihleri Arasındaki Nüfus Değişimi</h2>
            """,
            unsafe_allow_html=True
        )

        fig = go.Figure(data=go.Scatter(x=filtered_data['DATE_'], y=filtered_data['Toplam_Pop'],
                                        mode='lines', line=dict(color='#FFA07A'),
                                        name='Toplam Popülasyon'))

        fig.update_layout(
            xaxis_title='Tarih',
            yaxis_title='Toplam Popülasyon',
            plot_bgcolor='rgba(25, 25, 50, 0.2)',  # Arka plan rengini buradan değiştirebilirsiniz
            paper_bgcolor='black',  # Kağıt arka plan rengini buradan değiştirebilirsiniz
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(100, 100, 100, 0.7)',
                bordercolor='rgba(20, 20,20, 0.5)',
                borderwidth=1
            )
        )

        # # Grafiği görselleştirme
        # fig.show(renderer="browser")

        st.plotly_chart(fig)

elif visual_method == "Gelecek Veri":

    #####################################
    # 1 aylık baraj doluluk oranı tahmini.
    #####################################

    # labels = filtered_df['DATE_']
    new_date = selected_date + pd.DateOffset(weeks=4)
    filtered_data = pred_df[(pred_df['DATE_'] <= new_date) & (pred_df['DATE_'] >= selected_date)]

    first_day_new = selected_date.strftime("%d-%m-%Y")
    last_day = new_date.strftime("%d-%m-%Y")

    st.markdown(
        f"""
        <h2 style="text-align: center; font-size: 20px;">{first_day_new} - {last_day} Tarihleri Arasındaki Baraj Doluluk Seviyeleri</h2>
        """,
        unsafe_allow_html=True
    )

    # Renk paleti

    # Veriye uygun bir başlangıç noktası belirleme
    start_index = filtered_data["BARAJ_DOLULUK"].idxmax()

    # Renk paletini oluşturma
    color_palette = colors.qualitative.Plotly

    # Renk paleti ton sayısı
    num_tones = 30

    # Renk tonları listesi
    tone_colors = [color_palette[i % len(color_palette)] for i in range(num_tones)]

    # Çubukları renklendirme
    fig = go.Figure(data=[go.Bar(
        x=filtered_data['DATE_'],
        y=filtered_data["BARAJ_DOLULUK"],
        marker=dict(
            color=tone_colors
        )
    )])

    # X ve Y ekseni etiketleri
    fig.update_layout(xaxis_title='Tarih', yaxis_title='Baraj Doluluk [m3]')

    # # Grafiği görselleştirme
    # fig.show()

    # Grafiği görselleştirme
    # fig.show(renderer="browser")

    st.plotly_chart(fig)

    #####################################
    # Main_df ile pred_df'i birleştireceğiz.
    #####################################


    # labels = filtered_df['DATE_']

    st.markdown(
        f"""
        <h2 style="text-align: center; font-size: 20px;">Baraj Doluluk Değerleri 2011-2026</h2>
        """,
        unsafe_allow_html=True
    )

    # Renk paleti

    # Veriye uygun bir başlangıç noktası belirleme
    main_data = main_df[["DATE_","BARAJ_DOLULUK"]]
    pred_data = pred_df[["DATE_", "BARAJ_DOLULUK"]]
    trace1 = go.Scatter(x=main_data["DATE_"], y=main_data["BARAJ_DOLULUK"], name="Orijinal Veri")
    trace2 = go.Scatter(x=pred_data["DATE_"], y=pred_data["BARAJ_DOLULUK"], name="Tahmin Edilen Veri")

    data = [trace1, trace2]

    layout = go.Layout(
        xaxis=dict(title="Tarih"),
        yaxis=dict(title="Baraj Doluluk [m3]"),
        width=800,  # Genişlik değerini istediğiniz gibi ayarlayın
        height=500  # Yükseklik değerini istediğiniz gibi ayarlayın
    )

    fig = go.Figure(data=data, layout=layout)

    # Grafiği görselleştirme
    # fig.show(renderer="browser")

    st.plotly_chart(fig)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
