import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Sistem Nilai Mahasiswa", layout="wide")

# --- IDATA DUMMY ---
if 'data_mahasiswa' not in st.session_state:
    st.session_state.data_mahasiswa = [
        {"Nama": "Bagas Dzaki", "NIM": "2313010636", "Kelas": "6.I", "Tugas": 85, "UTS": 80, "UAS": 90},
        {"Nama": "Ahmad Samhan", "NIM": "2313010642", "Kelas": "6.I", "Tugas": 75, "UTS": 75, "UAS": 85},
        {"Nama": "Khoris Najda", "NIM": "2313010623", "Kelas": "6.I", "Tugas": 60, "UTS": 60, "UAS": 55},
    ]

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# --- FUNGSI LOGIKA ---
def hitung_nilai_akhir(tugas, uts, uas):
    # Bobot: Tugas 30%, UTS 30%, UAS 40%
    return (tugas * 0.3) + (uts * 0.3) + (uas * 0.4)

def tentukan_grade(nilai):
    if nilai >= 85: return "A"
    elif nilai >= 70: return "B"
    elif nilai >= 55: return "C"
    else: return "D"

def get_dataframe():
    df = pd.DataFrame(st.session_state.data_mahasiswa)
    if not df.empty:
        df['Nilai Akhir'] = df.apply(lambda row: hitung_nilai_akhir(row['Tugas'], row['UTS'], row['UAS']), axis=1)
        df['Grade'] = df['Nilai Akhir'].apply(tentukan_grade)
    return df

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔐 Akses Sistem")
    st.subheader("login : admin/12345") 
    if not st.session_state.is_admin:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "admin" and password == "12345":
                st.session_state.is_admin = True
                st.rerun()
            else:
                st.error("Akun salah!")
    else:
        st.success("Mode: Admin")
        if st.button("Logout"):
            st.session_state.is_admin = False
            st.rerun()

# --- HALAMAN UTAMA ---
st.title("🎓 Sistem Informasi Nilai Mahasiswa AMIKOM Surakarta")

# Tampilan Tabel (Public/Index)
st.subheader("Data Nilai Mahasiswa")
df_display = get_dataframe()
if not df_display.empty:
    st.dataframe(df_display, use_container_width=True)
else:
    st.info("Belum ada data mahasiswa.")

# --- FITUR CRUD (KHUSUS ADMIN) ---
if st.session_state.is_admin:
    st.divider()
    st.subheader("Panel Kontrol Admin")
    
    tab1, tab2, tab3 = st.tabs(["Tambah Data", "Edit Data", "Hapus Data"])

    # 1. CREATE (Tambah)
    with tab1:
        with st.form("tambah_form"):
            col1, col2 = st.columns(2)
            nama_baru = col1.text_input("Nama Mahasiswa")
            nim_baru = col2.text_input("NIM")
            kelas_baru = col1.text_input("Kelas")
            tgs = col2.number_input("Nilai Tugas", 0, 100, 0)
            uts = col1.number_input("Nilai UTS", 0, 100, 0)
            uas = col2.number_input("Nilai UAS", 0, 100, 0)
            
            if st.form_submit_button("Simpan Data"):
                if nama_baru and nim_baru:
                    st.session_state.data_mahasiswa.append({
                        "Nama": nama_baru, "NIM": nim_baru, "Kelas": kelas_baru,
                        "Tugas": tgs, "UTS": uts, "UAS": uas
                    })
                    st.success("Data berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Nama dan NIM wajib diisi!")

    # 2. UPDATE (Edit)
    with tab2:
        if not df_display.empty:
            list_nim = df_display['NIM'].tolist()
            nim_edit = st.selectbox("Pilih NIM yang akan diedit", list_nim)
            
            # Ambil data lama
            idx = next(i for i, item in enumerate(st.session_state.data_mahasiswa) if item["NIM"] == nim_edit)
            data_lama = st.session_state.data_mahasiswa[idx]
            
            with st.form("edit_form"):
                col1, col2 = st.columns(2)
                nama_upd = col1.text_input("Nama", value=data_lama["Nama"])
                kelas_upd = col2.text_input("Kelas", value=data_lama["Kelas"])
                tgs_upd = col1.number_input("Tugas", 0, 100, data_lama["Tugas"])
                uts_upd = col2.number_input("UTS", 0, 100, data_lama["UTS"])
                uas_upd = col1.number_input("UAS", 0, 100, data_lama["UAS"])
                
                if st.form_submit_button("Update Data"):
                    st.session_state.data_mahasiswa[idx] = {
                        "Nama": nama_upd, "NIM": nim_edit, "Kelas": kelas_upd,
                        "Tugas": tgs_upd, "UTS": uts_upd, "UAS": uas_upd
                    }
                    st.success("Data berhasil diperbarui!")
                    st.rerun()
        else:
            st.write("Tidak ada data untuk diedit.")

    # 3. DELETE (Hapus)
    with tab3:
        if not df_display.empty:
            nim_hapus = st.selectbox("Pilih NIM yang akan dihapus", df_display['NIM'].tolist(), key="del")
            if st.button("Hapus Data Mahasiswa", type="primary"):
                st.session_state.data_mahasiswa = [item for item in st.session_state.data_mahasiswa if item["NIM"] != nim_hapus]
                st.error(f"Data dengan NIM {nim_hapus} telah dihapus.")
                st.rerun()
else:
    st.caption("Silakan login di sidebar untuk mengakses fitur edit data.")
