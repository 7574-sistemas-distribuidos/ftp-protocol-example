# FTP client example

## alpine_ftp (Server)
Uses a lightweight server by installing **vsftpd** in **alpine**. A minimum FTP configuration is provided in **vsftpd.conf** to enable local users.

## alpine_client
Provides a development environment to connect to the server.

## Usage
Start the server and client containers:
* ```docker-compose up```

Jump into the client:
* ```docker-compose exec client ash```

Within the client, execute the **list.py** sequence:
* ```python3 list.py```

Also, you can test the FTP commands by your own using **netcat**:
* ```nc ftpserver 21```

Finally, try some changes:
* Update the content of the mounted volume at alpine_ftp/ftpfolder.
* Execute again the sequence in the client.

