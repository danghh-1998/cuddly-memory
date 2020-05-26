# OCR for Business

> Đồ án các công nghệ xây dựng hệ thống thông tin, trường đại học Bách Khoa Hà Nội

[![Requirements Status](https://requires.io/github/danghh-1998/cuddly-memory/requirements.svg?branch=master)](https://requires.io/github/danghh-1998/cuddly-memory/requirements/?branch=master) ![Languages](https://img.shields.io/github/languages/count/danghh-1998/cuddly-memory)  ![Top language](https://img.shields.io/github/languages/top/danghh-1998/cuddly-memory)  [![CodeFactor](https://www.codefactor.io/repository/github/danghh-1998/cuddly-memory/badge/master)](https://www.codefactor.io/repository/github/danghh-1998/cuddly-memory/overview/master)

---

## Table of content

- [Installation](#installation)
  - [Clone](#clone)
  - [Setup](#setup)
    - [Anaconda](#anaconda)
    - [Mysql](#mysql)
    - [SendGrid](#sendgrid)
    - [Backend](#backend)
    - [Nvm](#nvm)
    - [Frontend](#frontend)
- [Contributing](#contributing)
- [Team](#team)

---

## Installation

### Clone

- Clone repo theo đướng dẫn https://gitlab.com/is_soict/it4434_20192/7_trinhvt.git

### Setup

#### Anaconda

```bash
cd /tmp
sudo apt install curl -y
curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
chmod +x Anaconda3-2020.02-Linux-x86_64.sh
./Anaconda3-2020.02-Linux-x86_64.sh
```

- In order to continue the installation process, please review the license agreement. __Enter__
- Do you approve the license terms? [yes|no] __yes__
- Anaconda3 will now be installed into this location: __Enter__
- Do you wish the installer to prepend the Anaconda3 install location to PATH in your /home/{your user}/.bashrc ? [yes|no] __yes__

```bash
source ~/.bashrc
conda create --n backend python=3.7
conda activate backend
```

---

#### Mysql

```bash
sudo apt install build-essential libreadline-dev libxml2-dev libxslt1-dev \
libcurl4-openssl-dev libmysqlclient-dev
sudo apt install mysql-server -y
```

- Nếu gặp lỗi `access denied for user 'root'@'localhost` hoặc `cannot connect to mysql through socket` thì đặt lại mật khẩu cho mysql như sau

```bash
sudo service mysql stop
sudo mkdir -p /var/run/mysqld
sudo chown mysql:mysql /var/run/mysqld
sudo /usr/sbin/mysqld --skip-grant-tables --skip-networking &
mysql -u root
```

- Đặt lại mật khẩu root

```mysql
USE mysql;
UPDATE user SET authentication_string=PASSWORD("12345678") WHERE User='root';
-- "12345678" la mat khau root
UPDATE user SET plugin="mysql_native_password" WHERE User='root';
quit
```

- Khởi động lại tiến trình mysql

```bash
sudo pkill mysqld
sudo service mysql start
```

Tạo database

```mysql
mysql -uroot -p12345678
-- "12345678" là mật khẩu root
CREATE DATABASE project CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
```

---

#### SendGrid

- Đăng ký tài khoản SendGrid tại <https://app.sendgrid.com/>
- Trong phần __Settings__ vào mục __API Keys__ sau đó nhấn vào nút __Create API Key__ phía trên bên phải

![Create Key](https://raw.githubusercontent.com/danghh-1998/cuddly-memory/danghh_5/screenshots/sendgrid-create-api-key.png)

- Điền đây đủ thông thông tin sau đó chọn __Create & View__

![Review key](https://raw.githubusercontent.com/danghh-1998/cuddly-memory/danghh_5/screenshots/sendgrid-review-api-key.png)

- Lưu lại __API Key__ sau đó chọn __Done__

---

#### Backend

- Di chuyển vào thư mục đã clone code

```bash
cd 7_trinhvt/backend
```

- Tạo file .env với nội dung như sau

```yaml
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=12345678
DB_NAME=project
TOKEN_EXPIRED_AFTER_SECONDS=86400
DEFAULT_FROM_EMAIL=example@gmail.com
SENDGRID_API_KEY=send_grid_api
```

- Chạy server backend

```bash
echo "export DJANGO_ENV=development" >> ~/.bashrc
source ~/.bashrc
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

- Mặc định server chạy ở __localhost:8000__

---

#### Nvm

- Tải script và cài đặt nvm

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.3/install.sh | bash
```

- Cấu hình nvm chạy khi bật terminal

```bash
echo 'export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> ~/.bashrc
```

- Cài đặt node

```bash
nvm install 12.16.1
```

---

#### Frontend

```bash
cd 7_trinhvt/frontend
npm install
npm run serve
```

- Mặc định frontend chạy ở __localhost:8080__
- Mở trình duyệt, truy cập __localhost:8080__

![Auth](https://raw.githubusercontent.com/danghh-1998/cuddly-memory/danghh_5/screenshots/auth.png)

---

## Contributing

- Fork repo hoặc clone
- Hack away!
- Tạo pull request

---

## Team

- [ Hoàng Hải Đăng ] : <https://github.com/danghh-1998>
- [ Nguyễn Ngọc Hải ] : <https://gitlab.com/ngoc_hai_nguyen>
- [ Trần Thị Đỗ Hải ] : <https://gitlab.com/dohai>
- [ Bành Lê Đức ] : <https://gitlab.com/20081998> 