import pyodbc


async def connectionSet(applicationConfig):
    # creating connection Object which will contain MySQL Connection
    connection = None
    if applicationConfig['ENV'] == 'default':
        connection = pyodbc.connect(
            DRIVER=applicationConfig['connection'].driver,
            SERVER=applicationConfig['connection'].server,
            DATABASE=applicationConfig['database'].name,
            TRUSTED_CONNECTION=applicationConfig['connection'].trusted_connection,
            UID=applicationConfig['connection'].uid,
            PASSWORD=applicationConfig['connection'].pwd,
            MARS_Connection="YES",
            encrypt="NO",
            trust_server_certificate="YES"
            # TrustedServerCertificate="YES"
        )
    return connection
