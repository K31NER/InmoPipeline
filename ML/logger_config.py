import logging

def logger_startup():
    """
    Configura el logger general para el resto del archivos
    """
    logging.basicConfig(filename="ML/logs/Inmopipeline.log",
                        filemode="a",
                        level=logging.INFO,
                        format='%(asctime)s | %(levelname)s | %(message)s')

