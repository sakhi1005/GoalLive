class ImageUtil:

    CDN_BASE = "https://goal.com"

    @staticmethod
    def get_cdn_url(image_url: str) -> str:
        return ImageUtil.CDN_BASE + image_url