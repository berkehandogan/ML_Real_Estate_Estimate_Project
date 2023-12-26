import streamlit as st
import pandas as pd
import joblib

# Önceden eğitilmiş modelin yüklenmesi
model = joblib.load("../Algoritmalar/gbm_model.pkl")

# Streamlit uygulamasının oluşturulması
def main():
    st.title('Emlak Fiyat Tahmini')
    st.markdown('Bu uygulama, kullanıcının istediği özelliklere dayanarak ev fiyat tahmini yapar.')

    balkon_durumu_sozluk = {'Var': 0, 'Yok': 1}
    esya_durumu_sozluk = {'Boş': 0, 'Eşyalı': 1}
    isitma_tipi_sozluk = {'Doğalgaz': 0, 'Isıtma Yok': 1, 'Merkezi Kömür': 2}
    tip_sozluk = {'Bina': 0, 'Daire': 1, 'Residence': 2, 'Villa': 3}
    site_sozluk = {'Evet': 0, 'Hayır': 1}

    # Kullanıcıdan özellik girişlerinin alınması
    selected_balkon_durumu_name = st.selectbox('Balkon', list(balkon_durumu_sozluk.keys()))
    selected_balkon_durumu_index = balkon_durumu_sozluk[selected_balkon_durumu_name]

    banyo_sayisi = st.number_input('Banyo Sayısı', min_value=1, max_value=20, key='banyo_sayisi')
    bina_kat_sayisi = st.number_input('Bina Kat Sayısı', min_value=1, max_value=50, key='bina_kat_sayisi')
    bina_yasi = st.number_input('Bina Kaç Yaşında', min_value=0, max_value=60, key='bina_yasi')
    kat = st.number_input('Kaçıncı Kat', min_value=1, max_value=50, key='kat')

    selected_esya_durumu_name = st.selectbox('Eşya Durumu', list(esya_durumu_sozluk.keys()))
    selected_esya_durumu_index = esya_durumu_sozluk[selected_esya_durumu_name]

    selected_isitma_tipi_name = st.selectbox('Isıtma Tipi', list(isitma_tipi_sozluk.keys()))
    selected_isitma_tipi_index = isitma_tipi_sozluk[selected_isitma_tipi_name]

    net_metrekare = st.number_input('Metrekare', min_value=1, max_value=1000, key='net_metrekare')
    oda_sayisi = st.number_input('Oda Sayısı', min_value=1, max_value=20, key='oda_sayisi')

    selected_tip_name = st.selectbox('Ev tipi', list(tip_sozluk.keys()))
    selected_tip_index = tip_sozluk[selected_tip_name]

    selected_site_name = st.selectbox('Site İçerisinde mi ?', list(site_sozluk.keys()))
    selected_site_index = site_sozluk[selected_site_name]

    # Tahmin yapma
    if st.button('Fiyatı Tahmin Et'):
        veri_girisi = {'balkon_durumu': selected_balkon_durumu_index,
                      'banyo_sayisi': banyo_sayisi,
                      'bina_kat_sayisi': bina_kat_sayisi,
                      'bina_yasi': bina_yasi,
                      'kat': kat,
                      'esya_durumu': selected_esya_durumu_index,
                      'isitma_tipi': selected_isitma_tipi_index,
                      'net_metrekare': net_metrekare,
                      'oda_sayisi': oda_sayisi,
                      'site': selected_site_index,
                      'tip': selected_tip_index}

        girilen_veri = pd.DataFrame([veri_girisi])
        tahmin = model.predict(girilen_veri)

        st.success(f"Tahmini Fiyat: {tahmin[0]:,.2f} TL")

if __name__ == "__main__":
    main()
