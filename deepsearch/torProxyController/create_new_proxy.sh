#!/bin/bash
if [ -z "$1" ]; then
  echo "Использование: $0 <порт>"
  exit 1
fi
PORT=$1
if ! command -v tor &> /dev/null; then
  echo "Tor не установлен. Устанавливаем..."
  sudo apt-get update
  sudo apt-get install -y tor
fi
CONFIG_FILE="/etc/tor/torrc.$PORT"
echo "Создаем конфигурационный файл для порта $PORT..."
echo "SocksPort $PORT" > $CONFIG_FILE
echo "RunAsDaemon 1" >> $CONFIG_FILE
echo "DataDirectory /var/lib/tor$PORT" >> $CONFIG_FILE
sudo mkdir -p /var/lib/tor$PORT
sudo chown debian-tor:debian-tor /var/lib/tor$PORT
echo "Запускаем Tor на порту $PORT..."
sudo -u debian-tor tor -f $CONFIG_FILE &
echo "Tor прокси успешно запущен на порту $PORT."