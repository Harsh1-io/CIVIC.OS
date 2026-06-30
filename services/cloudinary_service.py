import os
import cloudinary
import cloudinary.uploader


def init_cloudinary():
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True,
    )


async def upload_image(file_bytes: bytes, filename: str) -> tuple[str, str]:
    """Upload image bytes to Cloudinary. Returns (secure_url, public_id)."""
    result = cloudinary.uploader.upload(
        file_bytes,
        folder="civic_os/reports",
        public_id=filename,
        overwrite=False,
        resource_type="image",
    )
    return result["secure_url"], result["public_id"]
