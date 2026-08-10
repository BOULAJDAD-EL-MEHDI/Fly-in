class NbDronesError(Exception):
    """Raised when a nb_drones entry is invalid."""
    pass

class HubError(Exception):
    """Raised when a hub entry is invalid."""
    pass

class StartHubError(Exception):
    """Raised when a start_hub entry is invalid."""
    pass

class EndHubError(Exception):
    """Raised when an end_hub entry is invalid."""
    pass

class ConnectionsError(Exception):
    """Raised when a connection entry is invalid."""
    pass

class ParsingKeyError(Exception):
    """Raised when a configuration file contains an invalid key or structure."""
    pass
