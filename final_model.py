import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.colors as colors


st.set_page_config(page_title="İstanbul Barajları Doluluk [m3] Tahminleme Modeli", page_icon="🖖")

st.markdown("""
    <style>
    .background {
        background-color: rgba(0, 0, 0, 0.30); /* Arka plan rengi ve transparanlık seviyesi */
        padding: 20px; /* İçeriği kenarlardan ayırmak için padding eklendi */
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .background_bilgilendirme {
        background-color: rgba(0, 0, 0, 0.90); /* Arka plan rengi ve transparanlık seviyesi */
        padding: 20px; /* İçeriği kenarlardan ayırmak için padding eklendi */
    }
    </style>
    """, unsafe_allow_html=True)

# # Set white background color and page width
st.markdown(
    f"""
     <style>
     .stApp {{
         background-image: url("https://images.unsplash.com/photo-1518887668165-8fa91a9178be?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80");
         background-attachment: fixed;
         background-size: cover;
         opacity: 1; /* Transparanlık seviyesi */
     }}
     </style>
     """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<h2 style='text-align: center;'>İstanbul Barajları Doluluk Oranı Tahminleme Modeli</h2>",
                    unsafe_allow_html=True)

# Gif dosyasının URL'si
gif_url = "https://media.tenor.com/47z7lWE2rC8AAAAC/hydro-dam.gif"

# Yan çubuğa GIF'i ekleme
st.sidebar.markdown(
    f'<img src="{gif_url}" alt="GIF" width="300">',
    unsafe_allow_html=True
)

# Yan çubuk içeriği

visual_method = st.sidebar.selectbox("Model Seçenekleri: ", {"Bilgilendirme","Geçmiş Veriler", "Tahmin Sonuçları"}, index=0)

if visual_method == "Bilgilendirme":
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.write("")

    with col2:
        st.image("https://md.teyit.org/img/istanbul-barajlar.jpg")

    with col3:
        st.write("")

    st.markdown(
        f"""
        <div class='background_bilgilendirme'><h2font-size: 20px;">    
        
    Bu tahmin modeli, [İBB Açık Veri Portalı'nda](https://data.ibb.gov.tr/dataset) sunulan, İstanbul Baraj Doluluk verileri, şehir
    popülasyonu, baraj yağış oranları gibi verisetlerine ek olarak harici bir kaynak üzerinden elde edilen güncel ve geçmiş;
    
    - Yağmur,
    - Rüzgar,
    - Sıcaklık,
    - Günlük hava verileri
    - Pandemi
    
    gibi doğrudan baraj doluluk oranını etkileyecek değişkenlerin yer aldığı verisetinin de yardımı ile, gelecek dönemdeki 
    toplam baraj doluluk oranlarının tahmini için tasarlanmıştır. Hava durumu ile ilgili tüm geçmiş veriler [Meteomatics](https://www.meteomatics.com/en/weather-api/?ppc_keyword=meteomatics&gclid=Cj0KCQjwqNqkBhDlARIsAFaxvwxT0hTWeoRH55FmndtCGL37WwIIFoCJE5wiTPZvphOiWvVX2Ew3gN4aAmwoEALw_wcB) sitesi üzerinden Weather API kullanılarak çekilmiştir.
    
    Uygulamanın kullanımı için, kullanıcı tarafından belirli bir gün, ay ve yıl tercihi yapması yeterli olacaktır. Ardından ilgili model,
    İstanbul'daki barajların toplam doluluk oranı sunacaktır.
    
    
    Çalışma; 
    - Alper Umut Keskin - [Linkedin](https://www.linkedin.com/in/alper-umut-keskin-10b25b77/), [Github](https://github.com/alperumut)
    - Hakan Keskin - [Linkedin](https://www.linkedin.com/in/hakan-keskin-/), [Github](https://github.com/KeskinHakan)
    - Oğuz Çalışkan - [Linkedin](https://www.linkedin.com/in/oğuz-çalışkan-71477939/), [Github](https://github.com/uzcaliskan)
    - Uğur Sarıçam - [Linkedin](https://www.linkedin.com/in/ugursaricam/), [Github](https://github.com/ugursaricam)
    tarafından yapılmış ve kullanıma sunulmuştur.
    
    Çalışmada "LSTM Layer - Keras" modeli kullanılarak, baraj doluluğunu etkileme potansiyeli olan tüm değişkenler dikkate alınacak şekilde
    modellenerek ileriye dönük tahmin modeli kurulmuştur. Tahmin modeli üzerinden elde edilen sonuçlara göre kullanıcılar, ileriye dönük İstanbul Baraj Doluluk değerlerini kontrol edebilecektir.</h2></div>
        """,
        unsafe_allow_html=True)


pd.set_option("display.width", 500)
pd.set_option("display.max_columns", None)

main_file_name = (r'C:\Users\hakan\OneDrive\Masaüstü\DSMLBC 11\07_Donem_Projesı\final_set.xlsx') # change it to the name of your excel file
#
predicted_name = (r'C:\Users\hakan\OneDrive\Masaüstü\DSMLBC 11\07_Donem_Projesı\predict_dataset.xlsx') # change it to the name of your excel file

# main_file_name = "final_set.xlsx"
# predicted_name = "predict_dataset.xlsx"

main_df = pd.read_excel(main_file_name)
pred_df = pd.read_excel(predicted_name)

if visual_method == "Geçmiş Veriler":

    st.sidebar.markdown("<h2 style='text-align: center; color: white;'>Geçmiş Veri Seçenekleri: </h2>",
                unsafe_allow_html=True)

    data_type = st.sidebar.selectbox("Veri Tipi: ", {"Barajlar"}, index = 0)
    if data_type == "Barajlar":
        dam_name = st.sidebar.selectbox("Baraj: ",
                                        {"Hepsi","Ömerli", "Alibey", "Darlik", "Elmali", "Terkos", "Büyükçekmece", "Sazlidere","Kazandere", "Pabuçdere", "Istrancalar"}, index = 0)

    # Minimum ve maksimum tarihleri belirle
    min_date = pd.to_datetime("2011-01-01")  # Bugünden bir yıl önce
    max_date = pd.to_datetime("2023-03-31")  # Bugünden bir yıl sonra
    default_date = datetime(2022, 3, 31)  # Varsayılan tarih

    # Tarih girdisini alın
    selected_date = st.sidebar.date_input("Tarih Seçin", value=default_date, min_value=min_date, max_value=max_date)

    # Seçilen tarihi formatlayın
    # selected_date = selected_date.strftime("%d-%m-%Y")
    selected_date = datetime.combine(selected_date, datetime.min.time())


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
                <div class='background'><h2 style="text-align: center; font-size: 20px;">{selected} Tarihindeki Baraj Doluluk Oranları Dağılımı</h2></div>
                """,
                unsafe_allow_html=True)

            filtered_data = main_df[main_df['DATE_'] == selected_date]
            values = filtered_data[['Ömerli', 'Darlik', 'Elmali', 'Terkos', 'Alibey', 'Büyükçekmece', 'Sazlidere', 'Kazandere', 'Pabuçdere', 'Istrancalar']]

            # İlk satırı seçme
            row = values.iloc[0]

            # Değişkenler ve değerler
            labels = row.index
            values = row.values

            # Pasta grafiği oluşturma
            fig = go.Figure(data=go.Pie(labels=labels, values=values))

            # Layout ayarları
            fig.update_layout(
                height=500,  # Pasta grafiğinin yüksekliğini buradan ayarlayabilirsiniz
                width=704,  # Pasta grafiğinin genişliğini buradan ayarlayabilirsiniz
                margin=dict(l=50, r=50, t=100, b=50),  # Grafik kenar boşluklarını ayarlayabilirsiniz
                plot_bgcolor="rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
                paper_bgcolor="rgba(180, 180, 180, 0.8)",  # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
                xaxis=dict(
                    title=dict(
                        text="Tarih",
                        font=dict(
                            color="black"  # X ekseni yazı rengi
                        )
                    ),
                    tickfont=dict(
                        color="black"  # X ekseni işaretçi yazı rengi
                    )
                ),
                yaxis=dict(
                    title=dict(
                        text="Baraj Doluluk [m3]",
                        font=dict(
                            color="black"  # Y ekseni yazı rengi
                        )
                    ),
                    tickfont=dict(
                        color="black"  # Y ekseni işaretçi yazı rengi
                    )
                )
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
                <div class='background'><h2 style="text-align: center; font-size: 20px;">{first_day_new} - {selected} Tarihleri Arasındaki Baraj Doluluk Seviyeleri</h2></div>
                """,
                unsafe_allow_html=True)

            # Renk paleti

            # Veriye uygun bir başlangıç noktası belirleme
            start_index = filtered_data["BARAJ_DOLULUK"].idxmax()

            # Bar chart oluşturma
            fig = go.Figure(
                data=[go.Bar(x=filtered_data['DATE_'], y=filtered_data["BARAJ_DOLULUK"])])

            # X ve Y ekseni etiketleri
            fig.update_layout(xaxis_title='Tarih', yaxis_title='Değer',
                              width=704,
                              height=500,
                              plot_bgcolor="rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
                              paper_bgcolor="rgba(180, 180, 180, 0.8)",
                              # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
                              xaxis=dict(
                                  title=dict(
                                      text="Tarih",
                                      font=dict(
                                          color="black"  # X ekseni yazı rengi
                                      )
                                  ),
                                  tickfont=dict(
                                      color="black"  # X ekseni işaretçi yazı rengi
                                  )
                              ),
                              yaxis=dict(
                                  title=dict(
                                      text="Baraj Doluluk [m3]",
                                      font=dict(
                                          color="black"  # Y ekseni yazı rengi
                                      )
                                  ),
                                  tickfont=dict(
                                      color="black"  # Y ekseni işaretçi yazı rengi
                                  )
                              )
                              )


            st.plotly_chart(fig)

        elif dam_name != "Hepsi":
            # labels = filtered_df['DATE_']
            new_date = selected_date - timedelta(weeks=4)
            filtered_data = main_df[(main_df['DATE_'] >= new_date) & (main_df['DATE_'] <= selected_date)]


            first_day_new = new_date.strftime("%d-%m-%Y")
            selected = selected_date.strftime("%d-%m-%Y")

            st.markdown(
                f"""
                <div class='background'><h2 style="text-align: center; color: white; font-size: 20px;">{first_day_new} - {selected} Tarihleri Arasındaki {dam_name} Barajı Doluluk Seviyeleri</h2></div>
                """,
                unsafe_allow_html=True)

            # Veriye uygun bir başlangıç noktası belirleme
            start_index = filtered_data[dam_name].idxmax()

            # Renk paletini oluşturma
            color_palette = colors.qualitative.Plotly

            # Renk paleti ton sayısı
            num_tones = 30

            # Renk tonları listesi
            tone_colors = [color_palette[i % len(color_palette)] for i in range(num_tones)]

            # Çubukları renklendirme
            fig = go.Figure(data=[go.Bar(
                x=filtered_data['DATE_'],
                y=filtered_data[dam_name],
                marker=dict(
                    color=tone_colors
                )
            )])

            # X ve Y ekseni etiketleri
            fig.update_layout(xaxis_title='Tarih',
                              yaxis_title='Doluluk [m3]',
                              width=704,
                              height=500,
                              plot_bgcolor="rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
                              paper_bgcolor="rgba(180, 180, 180, 0.8)",
                              # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
                              xaxis=dict(
                                  title=dict(
                                      text="Tarih",
                                      font=dict(
                                          color="black"  # X ekseni yazı rengi
                                      )
                                  ),
                                  tickfont=dict(
                                      color="black"  # X ekseni işaretçi yazı rengi
                                  )
                              ),
                              yaxis=dict(
                                  title=dict(
                                      text="Baraj Doluluk [m3]",
                                      font=dict(
                                          color="black"  # Y ekseni yazı rengi
                                      )
                                  ),
                                  tickfont=dict(
                                      color="black"  # Y ekseni işaretçi yazı rengi
                                  )
                              )
                              )

            # # Grafiği görselleştirme
            # fig.show()

            # Grafiği görselleştirme
            # fig.show(renderer="browser")

            st.plotly_chart(fig)

            #####################################
            # SEÇİLİ BARAJIN SON BİR YILDAKİ AY SONLARI DOLULUK DEĞERLERİ (%)
            #####################################

            filtered_data = main_df[main_df['DATE_'] <= selected_date]
            # selected_date = pd.to_datetime(str(year)+"-"+str(month)+"-"+str(day))

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
                <div class='background'><h2 style="text-align: center; color: white; font-size: 20px;">{last_day_new} - {first_day_new} Tarihleri Arasındaki {dam_name} Barajı Doluluk Seviyeleri</h2></div>
                """,
                unsafe_allow_html=True)


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
                xaxis_title="Tarih",
                yaxis_title=f"{dam_name} Değeri",
                barmode="group",
                width=704,
                height=500,
                plot_bgcolor="rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
                paper_bgcolor="rgba(180, 180, 180, 0.8)",  # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
                xaxis=dict(
                    title=dict(
                        text="Tarih",
                        font=dict(
                            color="black"  # X ekseni yazı rengi
                        )
                    ),
                    tickfont=dict(
                        color="black"  # X ekseni işaretçi yazı rengi
                    )
                ),
                yaxis=dict(
                    title=dict(
                        text="Baraj Doluluk [m3]",
                        font=dict(
                            color="black"  # Y ekseni yazı rengi
                        )
                    ),
                    tickfont=dict(
                        color="black"  # Y ekseni işaretçi yazı rengi
                    )
                )
            )

            st.plotly_chart(fig)


elif visual_method == "Tahmin Sonuçları":

    st.sidebar.markdown("<h2 style='text-align: center; color: white;'>Tahmin Verisi Seçenekleri: </h2>",
                unsafe_allow_html=True)

    full_data = st.sidebar.selectbox("Veri Tipi: ", {"Baraj Doluluk"})

    min_date = pd.to_datetime("2023-03-31")  # Bugünden bir yıl önce
    max_date = pd.to_datetime("2025-12-24")  # Bugünden bir yıl sonra
    default_date = datetime(2023, 3, 31)  # Varsayılan tarih

    # Tarih girdisini alın
    selected_date = st.sidebar.date_input("Tarih Seçin", value=default_date, min_value=min_date, max_value=max_date)

    # Seçilen tarihi formatlayın
    selected_date = datetime.combine(selected_date, datetime.min.time())

    #####################################
    # 1 aylık baraj doluluk oranı tahmini.
    #####################################

    # labels = filtered_df['DATE_']
    new_date = selected_date + timedelta(weeks=4)
    filtered_data = pred_df[(pred_df['DATE_'] <= new_date) & (pred_df['DATE_'] >= selected_date)]

    first_day_new = selected_date.strftime("%d-%m-%Y")
    last_day = new_date.strftime("%d-%m-%Y")

    st.markdown(
        "<div class='background'><h2 style='text-align: center; color: white;'>Geleceğe Dönük Toplam Baraj Doluluk Hacmi Tahminleme</h2></div>",
        unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background-color: rgba(0, 0, 0, 0.30); padding: 10px; border-radius: 5px;">
            <h2 style="text-align: center;color: white; font-size: 20px;">{first_day_new} - {last_day} Tarihleri Arasındaki Baraj Doluluk Seviyeleri</h2>
        </div>
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
    fig.update_layout(
        xaxis_title='Tarih',
        yaxis_title='Baraj Doluluk [m3]',
        width=704,
        height=500,
        plot_bgcolor="rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
        paper_bgcolor="rgba(180, 180, 180, 0.8)",  # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
        xaxis=dict(
            title=dict(
                text="Tarih",
                font=dict(
                    color="black"  # X ekseni yazı rengi
                )
            ),
            tickfont=dict(
                color="black"  # X ekseni işaretçi yazı rengi
            )
        ),
        yaxis=dict(
            title=dict(
                text="Baraj Doluluk [m3]",
                font=dict(
                    color="black"  # Y ekseni yazı rengi
                )
            ),
            tickfont=dict(
                color="black"  # Y ekseni işaretçi yazı rengi
            )
        )
    )

    st.plotly_chart(fig)

    #####################################
    # Main_df ile pred_df'i birleştireceğiz.
    #####################################


    st.markdown(
        f"""
       
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='background'> <h2 style="text-align: center; color: white; font-size: 20px;">Baraj Doluluk Değerleri 2011-2025</h2></div>
        """,
        unsafe_allow_html=True)

    # Veriye uygun bir başlangıç noktası belirleme
    main_data = main_df[["DATE_","BARAJ_DOLULUK"]]
    pred_data = pred_df[["DATE_", "BARAJ_DOLULUK"]]
    trace1 = go.Scatter(x=main_data["DATE_"], y=main_data["BARAJ_DOLULUK"], name="Orijinal Veri")
    trace2 = go.Scatter(x=pred_data["DATE_"], y=pred_data["BARAJ_DOLULUK"], name="Tahmin Edilen Veri")

    data = [trace1, trace2]

    layout = go.Layout(
        xaxis=dict(
            title="Tarih",
            titlefont=dict(
                color="black"  # X ekseni yazı rengi
            ),
            tickfont=dict(
                color="black"  # X ekseni işaretçi yazı rengi
            )
        ),
        yaxis=dict(
            title="Baraj Doluluk [m3]",
            titlefont=dict(
                color="black"  # Y ekseni yazı rengi
            ),
            tickfont=dict(
                color="black"  # Y ekseni işaretçi yazı rengi
            )
        ),
        width=704,  # Genişlik değerini istediğiniz gibi ayarlayın
        height=500,  # Yükseklik değerini istediğiniz gibi ayarlayın
        plot_bgcolor = "rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
        paper_bgcolor = "rgba(180, 180, 180, 0.8)",  # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
    )

    fig = go.Figure(data=data, layout=layout)

    st.plotly_chart(fig)

    #####################################
    # SEÇİLİ BARAJIN SON BİR YILDAKİ AY SONLARI DOLULUK DEĞERLERİ (%)
    #####################################

    # Son bir yıldaki aylık veriye denk gelen ayın son günlerini seçme
    son_bir_yil_once = selected_date - timedelta(days=365)

    secilen_gunler = pd.date_range(son_bir_yil_once, periods=13, freq='M') + pd.offsets.MonthEnd()

    first_day_new = secilen_gunler[0].strftime("%d-%m-%Y")
    last_day_new = secilen_gunler[-1].strftime("%d-%m-%Y")

    st.markdown(
        f"""
        <div style="background-color: rgba(0, 0, 0, 0.5); padding: 10px; border-radius: 5px;">
            <h2 style="text-align: center;color: white; font-size: 20px;">{first_day_new} - {last_day_new} Tarihleri Arasındaki Toplam Doluluk Değerleri </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    # "dam_name" e göre filtreleme yapma
    filtered_data = pred_df[["DATE_", "BARAJ_DOLULUK"]]

    # Seçilen günleri içeren verileri filtreleme
    filtered_data = filtered_data[filtered_data["DATE_"].isin(secilen_gunler)]

    # Bar grafiği oluşturma
    fig = go.Figure(data=[
        go.Bar(x=filtered_data["DATE_"], y=filtered_data["BARAJ_DOLULUK"], marker_color='rgb(0, 128, 128)')
    ])

    # Grafik düzenlemeleri
    fig.update_layout(
        xaxis_title="Tarih",
        yaxis_title="Baraj Doluluk [m3]",
        barmode="group",
        showlegend=False,
        width=704,
        height=500,
        plot_bgcolor = "rgba(180, 180, 180, 0.8)",  # Arka plan rengi ve transparanlık seviyesi
        paper_bgcolor = "rgba(180, 180, 180, 0.8)",  # Kağıt arka plan rengi (şeffaf olarak ayarlandı)
        xaxis = dict(
            title=dict(
                text="Tarih",
                font=dict(
                    color="black"  # X ekseni yazı rengi
                )
            ),
            tickfont=dict(
                color="black"  # X ekseni işaretçi yazı rengi
            )
        ),
        yaxis = dict(
            title=dict(
                text="Baraj Doluluk [m3]",
                font=dict(
                    color="black"  # Y ekseni yazı rengi
                )
            ),
            tickfont=dict(
                color="black"  # Y ekseni işaretçi yazı rengi
            )
        )
    )

    # Grafiği görüntüleme
    st.plotly_chart(fig)

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)
