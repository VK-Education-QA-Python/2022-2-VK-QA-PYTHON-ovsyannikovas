## Python scripting

Результаты экспортируются в файл `results.txt` или `results.json`
## Bash scripting

### 1. Общее количество запросов

* Команда

  `awk '{print NR}' access.log | wc -l`
* Результат выполнения

  ```
  225133
  ```

### 2. Общее количество запросов по типу, например: GET - 20, POST - 10 и т.д.

* Команда

  `awk '{print $6}' access.log | awk '! /[0-9]/' | sort | uniq -c`
* Результат выполнения

    ```
   122095 "GET
      528 "HEAD
   102503 "POST
        6 "PUT
  ```

### 3. Топ 10 самых частых запросов

* Команда

  `awk '{print $7}' access.log | sort | uniq -c | sort -n -r | head -10`
* Результат выполнения

    ```
   103932 /administrator/index.php
    26336 /apache-log/access.log
     6940 /
     4980 /templates/_system/css/general.css
     3199 /robots.txt
     2356 http://almhuette-raith.at/administrator/index.php
     2201 /favicon.ico
     1644 /wp-login.php
     1563 /administrator/
     1287 /templates/jp_hotel/css/template.css
  ```

### 4. Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой

* Команда

  `awk '$9 ~ /4./' access.log | awk '{print $7, $9, $10, $1}' | sort -n -r -k 3 | head -5`
* Результат выполнения

    ```
  /index.php?option=com_phocagallery&view=category&id=7806&Itemid=53 404 1417 189.217.45.73
  /index.php?option=com_phocagallery&view=category&id=4025&Itemid=53 404 1417 189.217.45.73
  /index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%289168%3D4696%29%20THEN%209168%20ELSE%209168%2A%28SELECT%209168%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53 404 1417 189.217.45.73
  /index.php?option=com_phocagallery&view=category&id=%28SELECT%20%28CASE%20WHEN%20%281753%3D1753%29%20THEN%201753%20ELSE%201753%2A%28SELECT%201753%20FROM%20INFORMATION_SCHEMA.CHARACTER_SETS%29%20END%29%29&Itemid=53 404 1417 189.217.45.73
  /?view=videos&type=member&user_id=1%20and%201=0%20union%20select%201,2,3,4,5,6,7,8,9,10,11,12,concat%280x3c757365723e,username,0x3c757365723e3c706173733e,password,0x3c706173733e%29,14,15,16,17,18,19,20,21,22,23,24,25,26,27%20from+jos_users+where+gid=25+limit+0,1--&option=com_jomtube 404 1397 5.206.77.93
  ```

### 5. Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой

* Команда

  `awk '$9 ~ /5./' access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -5`
* Результат выполнения

  ```
    225 189.217.45.73
      4 82.193.127.15
      3 91.210.145.36
      2 198.38.94.207
      2 195.133.48.198
  ```
