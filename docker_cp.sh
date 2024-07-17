#!/bin/bash

# # Yil, oy va kunni olish
year_month_day=$(date +"%Y%m%d%H%M%S")

# Docker komandasini ishga tushurish
PGPASSWORD='Qwerty!3124' docker exec sifato-postgres pg_dump -U postgres -d sifato-backend > /docker/volume/sifato/db/sifato_$year_month_day.sql
PGPASSWORD='Qwerty!3124' docker exec sifato-postgres pg_dump -U postgres -d turayeva > /docker/volume/sifato/db/turayeva_$year_month_day.sql

# Faylni Telegram bot orqali yuborish
#telegram-send --file /docker/volume/sifato/db/sifato_$year_month_day.sql
for file in /docker/volume/sifato/db/*; do
    telegram-send --file "$file"
done

# Faylni o'chirish
#rm /docker/volume/sifato/db/sifato_$year_month_day.sql
rm -rf /docker/volume/sifato/db/*

rm -rf /docker/volume/sifato/backup_media/*

zip -r /docker/volume/sifato/backup_media/media_$year_month_day.zip /docker/volume/sifato/media

split -d -b 45M /docker/volume/sifato/backup_media/media_$year_month_day.zip /docker/volume/sifato/backup_media/sifato_

rm /docker/volume/sifato/backup_media/media_$year_month_day.zip

for file in /docker/volume/sifato/backup_media/*; do
    telegram-send --file "$file"
done

rm -rf /docker/volume/sifato/backup_media/*
