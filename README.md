
---

# Summary Pengetesan API Blog Django

Dokumentasi ini berisi panduan untuk mengetes fungsionalitas API. Beberapa poin yang telah diuji meliputi otentikasi JWT, operasi CRUD untuk user, post, like, dan comment, serta fitur detail post untuk owner.

## Atur virtual environtment
Agar dependency dari project TestAPI ini tidak konflik dengan dependency ayng telah terinstall di komputer tester, dianjurkan untuk mengaktifkan virtual environtment. Dalam hal ini penulis menggunakan `venv`.

```bash
cd <porject folder>
python -m venv venv
. venv/bin/activate
```

## Persiapan Awal

1.  **Pastikan semua dependensi terinstal:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Buat superuser (admin) dan beberapa user biasa:**
    ```bash
    python manage.py createsuperuser # Buat admin
    python manage.py shell
    # Di shell:
    from users.models import CustomUser
    user1 = CustomUser.objects.create_user(username='user1', email='user1@example.com', password='password123')
    user2 = CustomUser.objects.create_user(username='user2', email='user2@example.com', password='password123')
    user3 = CustomUser.objects.create_user(username='user3', email='user3@example.com', password='password123')
    exit()
    ```
3.  **Jalankan migrasi:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
4.  **Jalankan server Django:**
    ```bash
    python manage.py runserver
    ```
5.  **Akses Swagger UI** di `http://127.0.0.1:8000/api/schema/swagger-ui/` untuk pengetesan interaktif.

---

## Data Dump Awal

Berikut adalah beberapa data contoh yang akan digunakan dalam pengetesan. Anggap ID berikut sudah ada setelah operasi `POST`.

* **User Admin**:
    * `username`: `admin`
    * `password`: `admin123` (sesuai yang Anda buat)
* **User Biasa**:
    * `username`: `user1`, `user2`, `user3`
    * `password`: `password123`

---

## Skenario Pengetesan & Contoh Respons

Untuk setiap skenario, **login terlebih dahulu** di Swagger UI menggunakan endpoint `/api/login/` untuk mendapatkan token `access` dan masukkan ke otorisasi `Bearer Auth`.

### 1. User Authentication

#### **Endpoint:** `/api/login/` (POST)
* **Tujuan:** Mendapatkan token akses JWT.
* **Data Request:**
    ```json
    {
        "username": "user1",
        "password": "password123"
    }
    ```
* **Contoh Respons (Sukses):**
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxODE3MzIwMywiaWF0IjoxNzE4MDg2ODAzLCJqdGkiOiJjNzM4N2U1YzYzZjU0ZTUwODkxOTg0MWNlMjMzYjFjZCIsInVzZXJfaWQiOjJ9.C_w4B_t_1R_X_p_0P_o_5j_A_3_G_2_0_0_0",
        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE4MDg3NDAzLCJpYXQiOjE3MTgwODY4MDMsImp0aSI6ImZiMzcwMjQ4OTM4OTQ1YmY5MjU4MTg4NTFjZGUyZjNhIiwidXNlcl9pZCI6Mn0.X_y_z_A_b_C_D_E_F_G_H_I_J_K_L_M_N_O_P_Q_R_S_T_U_V_W_X_Y_Z"
    }
    ```
* **Langkah Lanjut:** Salin `access` token dan masukkan ke tombol `Authorize` di Swagger UI dengan format `Bearer <token>`.

#### **Endpoint:** `/api/register/` (POST)
* **Tujuan:** Membuat user baru.
* **Data Request:**
    ```json
    {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepassword",
        "password2": "securepassword"
    }
    ```
* **Contoh Respons (Sukses):**
    ```json
    {
        "message": "Berhasil registrasi",
        "user_id": 4,
        "username": "newuser",
        "email": "newuser@example.com"
    }
    ```

---

### 2. User Management (Admin Only)

#### **Endpoint:** `/api/users/` (GET)
* **Tujuan:** Melihat daftar semua user.
* **Persyaratan:** Login sebagai **admin**.
* **Contoh Respons (Sukses):**
    ```json
    [
        {
            "id": 1,
            "username": "admin",
            "email": "admin@example.com",
            "is_staff": true,
            "date_joined": "2024-05-25T17:00:00Z"
        },
        {
            "id": 2,
            "username": "user1",
            "email": "user1@example.com",
            "is_staff": false,
            "date_joined": "2024-05-25T17:01:00Z"
        }
    ]
    ```

#### **Endpoint:** `/api/users/{id}/` (GET)
* **Tujuan:** Melihat detail user tertentu.
* **Persyaratan:** Login sebagai **admin**.
* **Contoh Respons (Sukses, untuk user1):**
    ```json
    {
        "id": 2,
        "username": "user1",
        "email": "user1@example.com",
        "is_staff": false,
        "date_joined": "2024-05-25T17:01:00Z"
    }
    ```

---

### 3. Post Management

#### **Endpoint:** `/api/posts/` (POST)
* **Tujuan:** Membuat post baru.
* **Persyaratan:** Login sebagai **user biasa** (misal user1).
* **Data Request:**
    ```json
    {
        "title": "My First Post",
        "content": "This is the content of my first post."
    }
    ```
* **Contoh Respons (Sukses):**
    ```json
    {
        "id": 1,
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "author": "user1",
        "created_at": "2024-05-25T17:05:00Z",
        "updated_at": "2024-05-25T17:05:00Z",
        "likes_count": 0
    }
    ```

#### **Endpoint:** `/api/posts/` (GET)
* **Tujuan:** Melihat daftar semua post.
* **Persyaratan:** Dapat diakses tanpa login (public).
* **Contoh Respons (Sukses):**
    ```json
    [
        {
            "id": 1,
            "title": "My First Post",
            "content": "This is the content of my first post.",
            "author": "user1",
            "created_at": "2024-05-25T17:05:00Z",
            "updated_at": "2024-05-25T17:05:00Z",
            "likes_count": 0
        },
        {
            "id": 2,
            "title": "Another Post by User2",
            "content": "Hello from User2!",
            "author": "user2",
            "created_at": "2024-05-25T17:06:00Z",
            "updated_at": "2024-05-25T17:06:00Z",
            "likes_count": 0
        }
    ]
    ```

#### **Endpoint:** `/api/posts/{id}/` (GET - Owner vs Non-Owner)
* **Tujuan:** Melihat detail post tertentu.
* **Persyaratan:**
    * **Sebagai non-owner (user2 melihat post user1):** Login sebagai user2.
    * **Sebagai owner (user1 melihat postnya sendiri):** Login sebagai user1.
* **Contoh Respons (Non-Owner - ID Post 1, dibuat oleh user1):**
    ```json
    {
        "id": 1,
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "author": "user1",
        "created_at": "2024-05-25T17:05:00Z",
        "updated_at": "2024-05-25T17:05:00Z",
        "likes_count": 0,
        "liked_by": null,       <-- Null karena bukan owner
        "comments": null        <-- Null karena bukan owner
    }
    ```
* **Contoh Respons (Owner - ID Post 1, dibuat oleh user1, setelah ada like dan comment):**
    * *Asumsi:* `user2` like Post ID 1, `user3` comment Post ID 1 ("Great post!").
    ```json
    {
        "id": 1,
        "title": "My First Post",
        "content": "This is the content of my first post.",
        "author": "user1",
        "created_at": "2024-05-25T17:05:00Z",
        "updated_at": "2024-05-25T17:05:00Z",
        "likes_count": 1,
        "liked_by": ["user2"],
        "comments": [
            {
                "id": 1,
                "user": "user3",
                "content": "Great post!",
                "created_at": "2024-05-25T17:10:00Z",
                "updated_at": "2024-05-25T17:10:00Z"
            }
        ]
    }
    ```

#### **Endpoint:** `/api/posts/{id}/` (PUT/PATCH)
* **Tujuan:** Mengupdate post.
* **Persyaratan:** Login sebagai **owner post**.
* **Data Request (PUT - ID Post 1):**
    ```json
    {
        "title": "Updated First Post",
        "content": "The content has been updated."
    }
    ```
* **Contoh Respons (Sukses):** Mirip dengan GET detail, tapi dengan data yang diupdate.

#### **Endpoint:** `/api/posts/{id}/` (DELETE)
* **Tujuan:** Menghapus post.
* **Persyaratan:** Login sebagai **owner post**.
* **Contoh Respons (Sukses):** HTTP 204 No Content.

---

### 4. Like Management

#### **Endpoint:** `/api/posts/{post_id}/likes/` (POST)
* **Tujuan:** Memberikan like pada post.
* **Persyaratan:** Login sebagai **user biasa** (misal user2, like post ID 1).
* **Data Request:** (Body kosong atau `{}` jika required by Swagger UI)
    ```json
    {}
    ```
* **Contoh Respons (Sukses):**
    ```json
    {
        "id": 1,
        "user": "user2",
        "post": 1,
        "created_at": "2024-05-25T17:07:00Z"
    }
    ```
* **Catatan:** Jika user yang sama mencoba like lagi, akan ada `ValidationError` "You have already liked this post."

#### **Endpoint:** `/api/posts/{post_id}/likes/` (GET)
* **Tujuan:** Melihat daftar like pada post tertentu.
* **Persyaratan:** Dapat diakses tanpa login (public).
* **Contoh Respons (Sukses - Post ID 1, setelah user2 like):**
    ```json
    [
        {
            "id": 1,
            "user": "user2",
            "post": 1,
            "created_at": "2024-05-25T17:07:00Z"
        }
    ]
    ```

#### **Endpoint:** `/api/posts/{post_id}/likes/{id}/` (DELETE)
* **Tujuan:** Menghapus like dari post.
* **Persyaratan:** Login sebagai **user yang memberikan like tersebut** (misal user2, hapus like ID 1 pada Post ID 1).
* **Contoh Respons (Sukses):** HTTP 204 No Content.

---

### 5. Comment Management

#### **Endpoint:** `/api/posts/{post_id}/comments/` (POST)
* **Tujuan:** Membuat komentar pada post.
* **Persyaratan:** Login sebagai **user biasa** (misal user3, comment post ID 1).
* **Data Request:**
    ```json
    {
        "content": "This is a great post!"
    }
    ```
* **Contoh Respons (Sukses):**
    ```json
    {
        "id": 1,
        "user": "user3",
        "post": 1,
        "content": "This is a great post!",
        "created_at": "2024-05-25T17:10:00Z",
        "updated_at": "2024-05-25T17:10:00Z"
    }
    ```

#### **Endpoint:** `/api/posts/{post_id}/comments/` (GET)
* **Tujuan:** Melihat daftar komentar pada post tertentu.
* **Persyaratan:** Dapat diakses tanpa login (public).
* **Contoh Respons (Sukses - Post ID 1, setelah user3 comment):**
    ```json
    [
        {
            "id": 1,
            "user": "user3",
            "post": 1,
            "content": "This is a great post!",
            "created_at": "2024-05-25T17:10:00Z",
            "updated_at": "2024-05-25T17:10:00Z"
        }
    ]
    ```

#### **Endpoint:** `/api/posts/{post_id}/comments/{id}/` (PUT/PATCH)
* **Tujuan:** Mengupdate komentar.
* **Persyaratan:** Login sebagai **user yang membuat komentar tersebut**.
* **Data Request (PATCH - Comment ID 1, Post ID 1):**
    ```json
    {
        "content": "Updated comment content."
    }
    ```
* **Contoh Respons (Sukses):** Mirip dengan GET detail, tapi dengan data yang diupdate.

#### **Endpoint:** `/api/posts/{post_id}/comments/{id}/` (DELETE)
* **Tujuan:** Menghapus komentar.
* **Persyaratan:** Login sebagai **user yang membuat komentar tersebut**.
* **Contoh Respons (Sukses):** HTTP 204 No Content.

---
