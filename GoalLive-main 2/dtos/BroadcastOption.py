class BroadcastOption:
    def __init__(self, broadcast_option_name: str, broadcast_url: str, broadcast_logo: str ) -> None:
        '''
        :param broadcast_option_name:
        :param broadcast_url: this contains the complete CDN link
        :param broadcast_logo:
        '''
        self.broadcast_option_name: str = broadcast_option_name
        self.broadcast_url: str = broadcast_url
        self.broadcast_logo: str = broadcast_logo