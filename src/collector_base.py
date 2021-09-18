class CollectorService(object):
    def is_service_active(self) -> bool:
        """
        Checks if the service is alive or not
        :return: if the service is alive or not
        """
        raise NotImplementedError

    def collect_data(self) -> str:
        """
        Collects data from a services
        :return: Data from the service in a json form
        """
        raise NotImplementedError

    def disconnect_from_service(self) -> bool:
        """
        Disconnects from the service
        :return: If the disconnection was successful or not
        """
        raise NotImplementedError
